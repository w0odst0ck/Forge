"""
两阶段匹配引擎：硬约束过滤 → 软评分排序。

核心流程:
  1. 加载场景库 TOML
  2. 对每个场景: 硬约束检查 → 通过后软评分 → Gap 分析
  3. 输出排序后的 MatchReport
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.scene_model import (
    DimensionScore,
    GapItem,
    HardConstraintItem,
    MatchReport,
    MatchResult,
    Product,
    SceneDefinition,
    SceneDimension,
)


class SceneLoader:
    """加载场景库 TOML 文件。"""

    def __init__(self, scene_dir: str | Path):
        self.scene_dir = Path(scene_dir)

    def load_all(self) -> List[SceneDefinition]:
        scenes: List[SceneDefinition] = []
        if not self.scene_dir.exists():
            return scenes
        for f in sorted(self.scene_dir.glob("*.toml")):
            raw = f.read_text(encoding="utf-8")
            data = tomllib.loads(raw)
            scenes.append(SceneDefinition(**data))
        return scenes

    def load_by_id(self, scene_id: str) -> Optional[SceneDefinition]:
        for scene in self.load_all():
            if scene.scene.get("id") == scene_id:
                return scene
        return None


class HardConstraintChecker:
    """硬约束检查器。"""

    def check(self, product: Product, constraint: HardConstraintItem) -> bool:
        val = product.get_field(constraint.field)
        op = constraint.op
        target = constraint.value

        if val is None:
            return False

        try:
            if op == "eq":
                return _eq(val, target)
            elif op == "ne":
                return not _eq(val, target)
            elif op == "gte":
                return float(val) >= float(target)
            elif op == "lte":
                return float(val) <= float(target)
            elif op == "gt":
                return float(val) > float(target)
            elif op == "lt":
                return float(val) < float(target)
            elif op == "in":
                return val in target if isinstance(target, (list, tuple)) else val == target
            elif op == "not_in":
                return val not in target if isinstance(target, (list, tuple)) else val != target
            elif op == "contains":
                if isinstance(val, list):
                    return target in val
                return target in str(val)
            elif op == "contains_any":
                if isinstance(val, list):
                    return any(v in val for v in target)
                return any(v in str(val) for v in target)
            else:
                return False
        except (TypeError, ValueError):
            return False


class SoftScorer:
    """软评分器：按场景定义的评分逻辑计算匹配度。"""

    def __init__(self):
        self._checker = HardConstraintChecker()

    def score(self, product: Product, scene: SceneDefinition,
              gap_items: List[GapItem]) -> List[DimensionScore]:
        results: List[DimensionScore] = []
        scoring = scene.soft_scoring

        for dim_name, dim in scoring.dimensions.items():
            try:
                score, reasoning = self._evaluate_dimension(
                    product, dim, gap_items, dim_name)
            except Exception as e:
                score = 0.0
                reasoning = f"评分异常: {e}"

            results.append(DimensionScore(
                name=dim_name,
                score=round(score, 4),
                weight=dim.weight,
                reasoning=reasoning,
            ))

        return results

    def _evaluate_dimension(
        self, product: Product, dim: SceneDimension,
        gap_items: List[GapItem], dim_name: str,
    ) -> tuple[float, str]:
        scoring = dim.scoring
        score_type = scoring.get("type", "enum_exact")
        field = scoring.get("field", "")
        val = product.get_field(field)

        if score_type == "enum_exact":
            mapping = scoring.get("mapping", {})
            norm_mapping = {_nk(k): v for k, v in mapping.items()}
            v = _nk(val)
            matched = norm_mapping.get(v, 0.0)
            return matched, f"值 '{val}' → 映射得分 {matched}"

        elif score_type == "enum_intersect":
            mapping = scoring.get("mapping", {})
            norm_mapping = {_nk(k): v for k, v in mapping.items()}
            ideal = scoring.get("ideal", [])
            mode = scoring.get("mode", "max")

            if isinstance(val, list):
                scores = []
                norm_ideal = [_nk(i) for i in ideal]
                for v in val:
                    if _nk(v) in norm_ideal:
                        scores.append(norm_mapping.get(_nk(v), 0.5))
                if not scores:
                    return 0.0, f"无匹配项，值: {val}"
                final = max(scores) if mode == "max" else sum(scores) / max(len(ideal), 1)
                return final, f"交集得分 {final} (值: {val}, 理想: {ideal})"
            else:
                matched = norm_mapping.get(_nk(val), 0.0)
                return matched, f"值 '{val}' → 映射得分 {matched}"

        elif score_type == "enum_match_count":
            mapping = scoring.get("mapping", {})
            norm_mapping = {_nk(k): v for k, v in mapping.items()}
            ideal = scoring.get("ideal", [])
            mode = scoring.get("mode", "sum_normalized")

            if isinstance(val, list):
                total = 0.0
                for v in val:
                    total += norm_mapping.get(_nk(v), 0.0)
                if mode == "sum_normalized" and ideal:
                    max_possible = sum(
                        norm_mapping.get(_nk(i), 1.0) for i in ideal)
                    total = total / max_possible if max_possible > 0 else 0.0
                return min(total, 1.0), f"多协议匹配得分 {min(total, 1.0):.2f}"
            return 0.0, "值不是数组"

        elif score_type == "range":
            ideal_min = scoring.get("ideal_min", 0)
            ideal_max = scoring.get("ideal_max", 999)
            slope = scoring.get("slope", 10)

            try:
                num_val = float(val) if val is not None else 0
            except (TypeError, ValueError):
                return 0.0, f"无法转为数值: {val}"

            if ideal_min <= num_val <= ideal_max:
                return 1.0, f"{num_val} 在理想区间 [{ideal_min}, {ideal_max}]"
            elif num_val < ideal_min:
                deficit = ideal_min - num_val
                score = max(0.0, 1.0 - deficit / slope) if slope > 0 else 0.0
                gap_items.append(GapItem(
                    aspect=dim_name, severity="warning" if score < 0.6 else "info",
                    message=f"值 {num_val} 低于理想最小值 {ideal_min}，偏差 {deficit}",
                    current_value=str(num_val), required_value=f"\u2265{ideal_min}",
                ))
                return round(score, 4), f"{num_val} < {ideal_min}, 偏差 {deficit}, 得分 {score:.2f}"
            else:
                excess = num_val - ideal_max
                score = max(0.0, 1.0 - excess / slope) if slope > 0 else 0.0
                if score < 0.8:
                    gap_items.append(GapItem(
                        aspect=dim_name, severity="info",
                        message=f"值 {num_val} 高于理想最大值 {ideal_max}，超出 {excess}",
                        current_value=str(num_val), required_value=f"\u2264{ideal_max}",
                    ))
                return round(score, 4), f"{num_val} > {ideal_max}, 超出 {excess}, 得分 {score:.2f}"

        elif score_type == "boolean_fields":
            fields = scoring.get("fields", [])
            score_per = scoring.get("score_per_match", 1.0)
            matched_count = sum(1 for f in fields if product.get_field(f))
            score = min(1.0, matched_count * score_per / max(len(fields), 1))
            return score, f"布尔字段匹配 {matched_count}/{len(fields)}"

        elif score_type == "feature_check":
            required = scoring.get("required_features", [])
            score_all = scoring.get("score_all", 1.0)
            score_partial = scoring.get("score_partial", 0.5)

            if isinstance(val, list):
                matched = sum(1 for f in required if f in val)
                if matched == len(required):
                    return score_all, f"全部特性匹配 {matched}/{len(required)}"
                elif matched > 0:
                    return score_partial, f"部分特性匹配 {matched}/{len(required)}"
                return 0.0, "无特性匹配"
            return 0.0, "特性字段不是数组"

        elif score_type == "ip_minimum":
            minimum_ip = scoring.get("minimum_ip", "IP54")
            score_per = scoring.get("score_per_level_above", 0.05)

            if isinstance(val, list):
                best = _ip_score(max(val, key=_ip_numeric))
            else:
                best = _ip_score(str(val)) if val else 0

            required = _ip_score(minimum_ip)
            if best >= required:
                excess = best - required
                score = min(1.0, 1.0 + excess * score_per)
                return score, f"IP {val} \u2265 {minimum_ip}, 得分 {score:.2f}"
            else:
                gap_items.append(GapItem(
                    aspect=dim_name, severity="critical",
                    message=f"IP 防护等级 {val} 低于需求 {minimum_ip}",
                    current_value=str(val), required_value=minimum_ip,
                ))
                return 0.0, f"IP {val} < {minimum_ip}, 不满足"

        return 0.0, f"未知评分类型: {score_type}"


def _ip_score(ip_str: str) -> float:
    try:
        return float(int(ip_str.replace("IP", "")))
    except (ValueError, AttributeError):
        return 0.0


def _ip_numeric(ip_str: str) -> int:
    try:
        return int(ip_str.replace("IP", ""))
    except (ValueError, AttributeError):
        return 0


def _eq(a: Any, b: Any) -> bool:
    """宽松相等比较。"""
    if type(a) == type(b):
        return a == b
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return str(a).lower().strip() == str(b).lower().strip()


def _nk(val: Any) -> str:
    """标准化键名：统一小写并将 - 转为 _。"""
    return str(val).lower().replace("-", "_").replace(" ", "_")


class Matcher:
    """两阶段匹配引擎入口。"""

    def __init__(self, scene_loader: SceneLoader):
        self.loader = scene_loader
        self._constraint_checker = HardConstraintChecker()
        self._soft_scorer = SoftScorer()

    def match(self, product: Product) -> MatchReport:
        scenes = self.loader.load_all()
        results: List[MatchResult] = []

        for scene in scenes:
            result = self._match_single(product, scene)
            results.append(result)

        results.sort(key=lambda r: r.total_score, reverse=True)

        return MatchReport(
            product_name=product.name,
            matched_scenes=results,
            top_scene=results[0] if results else None,
            summary_stats={
                "total_scenes_evaluated": len(results),
                "passed_hard_constraints": sum(
                    1 for r in results if r.passed_hard_constraints),
                "average_score": round(
                    sum(r.total_score for r in results) / max(len(results), 1), 4),
            },
        )

    def _match_single(self, product: Product, scene: SceneDefinition) -> MatchResult:
        result = MatchResult(
            scene_id=scene.scene.get("id", "unknown"),
            scene_name=scene.scene.get("name", "未知场景"),
        )

        # Stage 1: 硬约束
        failed: List[HardConstraintItem] = []
        for constraint in scene.hard_constraints.items:
            if not self._constraint_checker.check(product, constraint):
                failed.append(constraint)

        if failed:
            result.failed_constraints = failed
            result.passed_hard_constraints = False
            return result

        result.passed_hard_constraints = True

        # Stage 2: 软评分 + Gap
        gap_items: List[GapItem] = []
        dim_scores = self._soft_scorer.score(product, scene, gap_items)
        total_score = sum(ds.score * ds.weight for ds in dim_scores)
        result.dimension_scores = dim_scores
        result.total_score = round(total_score, 4)
        result.gaps = gap_items

        if total_score >= 0.8:
            result.recommendation = "recommended"
        elif total_score >= 0.4:
            result.recommendation = "conditional"
        else:
            result.recommendation = "not_recommended"

        return result
