"""
输出渲染器：将 MatchReport 转为 Markdown 报告或 JSON。

支持：
- MD: 用于人工阅读，可对接 solutions/ 方案库
- JSON: 用于程序消费
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Literal

from src.scene_model import MatchReport, MatchResult


def render_markdown(
    report: MatchReport,
    include_raw_scores: bool = False,
    include_reasoning: bool = True,
    output_path: str | Path | None = None,
) -> str:
    """渲染为 Markdown 报告。"""
    lines: list[str] = []

    # 标题
    lines.append(f"# BOM 场景匹配报告")
    lines.append(f"")
    lines.append(f"**产品**: {report.product_name}")
    lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    # 摘要
    lines.append(f"## 📊 摘要")
    lines.append(f"")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|------|-----|")
    total = report.summary_stats.get("total_scenes_evaluated", 0)
    passed = report.summary_stats.get("passed_hard_constraints", 0)
    avg = report.summary_stats.get("average_score", 0)
    lines.append(f"| 评估场景数 | {total} |")
    lines.append(f"| 通过硬约束 | {passed} |")
    lines.append(f"| 平均匹配分 | {avg:.2%} |")
    lines.append(f"")

    # 顶部推荐
    if report.top_scene:
        lines.append(f"## 🏆 最佳匹配")
        lines.append(f"")
        lines.append(f"**{report.top_scene.scene_name}** — {report.top_scene.total_score:.1%}")
        if report.top_scene.recommendation == "recommended":
            lines.append(f"> ✅ 强烈推荐用于此场景")
        elif report.top_scene.recommendation == "conditional":
            lines.append(f"> ⚠️ 条件适配（见 Gap 分析）")
        lines.append(f"")

    # 各场景详情
    lines.append(f"## 📋 场景匹配详情")
    lines.append(f"")

    for i, result in enumerate(report.matched_scenes):
        lines.append(f"### {i+1}. {result.scene_name}")
        lines.append(f"")

        if not result.passed_hard_constraints:
            lines.append(f"**❌ 未通过硬约束** — 此场景不推荐")
            for c in result.failed_constraints:
                lines.append(f"- `{c.field}` 要求 `{c.op} {c.value}`，BOM 不满足")
                if c.comment:
                    lines.append(f"  - {c.comment}")
            lines.append(f"")
            continue

        # 推荐标签
        tag = {"recommended": "✅ 推荐", "conditional": "⚠️ 条件适配", "not_recommended": "❌ 不推荐"}
        lines.append(f"**{tag.get(result.recommendation, '未知')}** — 匹配分: **{result.total_score:.1%}**")
        lines.append(f"")

        # 各维度评分
        if include_raw_scores or include_reasoning:
            lines.append(f"**维度评分:**")
            lines.append(f"")
            lines.append(f"| 维度 | 得分 | 权重 | 加权分 |")
            lines.append(f"|------|------|------|--------|")
            for ds in result.dimension_scores:
                weighted = ds.score * ds.weight
                lines.append(f"| {ds.name} | {ds.score:.2%} | {ds.weight:.0%} | {weighted:.2%} |")
            lines.append(f"")

            if include_reasoning:
                for ds in result.dimension_scores:
                    lines.append(f"- **{ds.name}**: {ds.reasoning}")
                lines.append(f"")

        # Gap 分析
        if result.gaps:
            lines.append(f"**Gap 分析:**")
            lines.append(f"")
            for gap in result.gaps:
                icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}
                lines.append(f"  - {icon.get(gap.severity, '•')} **{gap.aspect}**: {gap.message}")
                if gap.current_value and gap.required_value:
                    lines.append(f"    当前: `{gap.current_value}` | 需求: `{gap.required_value}`")
            lines.append(f"")

        lines.append(f"---")
        lines.append(f"")

    # 写入文件
    md = "\n".join(lines)
    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(md, encoding="utf-8")

    return md


def render_json(report: MatchReport, output_path: str | Path | None = None) -> str:
    """渲染为 JSON。"""
    data = report.model_dump()
    data["generated_at"] = datetime.now().isoformat()
    j = json.dumps(data, ensure_ascii=False, indent=2)

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(j, encoding="utf-8")

    return j
