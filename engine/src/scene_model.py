"""
数据模型层：BOM 产品、场景定义、匹配结果的 Pydantic 模型。

所有外部输入（TOML）落地为此处定义的结构体，
匹配引擎在数据模型层面工作，不直接操作 TOML 文本。
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# ================================================================
# BOM 产品模型
# ================================================================


class PowerSpec(BaseModel):
    nominal: float
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    unit: str = "W"


class CctSpec(BaseModel):
    min: int
    max: int
    unit: str = "K"


class EfficacySpec(BaseModel):
    value: float
    unit: str = "LM/W"


class DimmingRange(BaseModel):
    min: float
    max: float


class DetectionRadius(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None


class ProtocolDistance(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None
    unit: str = "m"


class Protocols(BaseModel):
    industrial: Optional[List[str]] = None
    iot: Optional[List[str]] = None
    distance: Optional[ProtocolDistance] = None


class TempRange(BaseModel):
    min: float
    max: float
    unit: str = "C"


class Environment(BaseModel):
    temp_range: TempRange
    ip_ratings: Optional[List[str]] = None


class Product(BaseModel):
    """完整的产品 BOM 模型。"""

    name: str
    schema_id: str
    description: Optional[str] = None

    # 基本规格
    product_specs: Dict[str, Any] = Field(default_factory=dict)

    # 模组
    light_module: Optional[Dict[str, Any]] = None
    power_module: Optional[Dict[str, Any]] = None
    sensor_module: Optional[Dict[str, Any]] = None
    communication_module: Optional[Dict[str, Any]] = None
    control_module: Optional[Dict[str, Any]] = None
    environment: Optional[Environment] = None
    certification: Optional[Dict[str, Any]] = None

    def get_field(self, field_path: str) -> Any:
        """
        通过点号分隔的路径获取任意字段值。
        例如: "sensor_module.type" → product.sensor_module["type"]
              "product_specs.efficacy.value" → product.product_specs["efficacy"]["value"]
        """
        parts = field_path.split(".")
        obj: Any = self
        for part in parts:
            if isinstance(obj, dict):
                obj = obj.get(part)
            elif isinstance(obj, BaseModel):
                obj = getattr(obj, part, None)
            elif isinstance(obj, list):
                try:
                    idx = int(part)
                    obj = obj[idx] if 0 <= idx < len(obj) else None
                except (ValueError, IndexError):
                    return None
            else:
                return None
            if obj is None:
                return None
        return obj


# ================================================================
# 场景硬约束
# ================================================================


class HardConstraintItem(BaseModel):
    """单条硬约束。"""

    field: str
    op: Literal["eq", "ne", "gte", "lte", "gt", "lt", "in", "not_in",
                 "contains", "contains_any"]
    value: Any
    comment: Optional[str] = None


class HardConstraints(BaseModel):
    description: Optional[str] = None
    items: List[HardConstraintItem] = Field(default_factory=list)


# ================================================================
# 场景软评分
# ================================================================


class SceneDimension(BaseModel):
    weight: float
    comment: Optional[str] = None
    scoring: Dict[str, Any]


class SoftScoring(BaseModel):
    description: Optional[str] = None
    dimensions: Dict[str, SceneDimension]


class SceneDefinition(BaseModel):
    """场景定义：描述一个典型应用场景及匹配规则。"""

    scene: Dict[str, Any]
    hard_constraints: HardConstraints
    soft_scoring: SoftScoring


# ================================================================
# 匹配结果
# ================================================================


class DimensionScore(BaseModel):
    name: str
    score: float
    weight: float
    reasoning: str


class GapItem(BaseModel):
    aspect: str
    severity: Literal["critical", "warning", "info"]
    message: str
    current_value: Optional[str] = None
    required_value: Optional[str] = None


class MatchResult(BaseModel):
    """单场景的匹配结果。"""

    scene_id: str
    scene_name: str
    passed_hard_constraints: bool = False
    failed_constraints: List[HardConstraintItem] = Field(default_factory=list)
    dimension_scores: List[DimensionScore] = Field(default_factory=list)
    total_score: float = 0.0
    gaps: List[GapItem] = Field(default_factory=list)
    recommendation: Literal["recommended", "conditional", "not_recommended"] = "not_recommended"


class MatchReport(BaseModel):
    """完整匹配报告。"""

    product_name: str
    matched_scenes: List[MatchResult]
    top_scene: Optional[MatchResult] = None
    summary_stats: Dict[str, Any] = Field(default_factory=dict)
