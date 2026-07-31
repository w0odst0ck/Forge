"""
BOM 解析器：将 TOML 格式的 BOM 文件解析为 Product 模型。

支持标准字段提取和宽松模式（允许结构不严格匹配 schema 的 BOM）。
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any, Dict

from src.scene_model import Environment, Product, TempRange


def parse_bom(path: str | Path) -> Product:
    """
    解析 TOML BOM 文件，返回 Product 模型。

    Args:
        path: TOML 文件路径

    Returns:
        Product 实例

    Raises:
        FileNotFoundError: 文件不存在
        tomllib.TOMLDecodeError: TOML 格式错误
        ValueError: 必要字段缺失
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"BOM 文件不存在: {path}")

    raw = path.read_text(encoding="utf-8")
    data = tomllib.loads(raw)

    return _build_product(data)


def parse_bom_dict(data: Dict[str, Any]) -> Product:
    """
    从字典解析 BOM（供 CLI 或程序内使用）。
    """
    return _build_product(data)


def _build_product(data: Dict[str, Any]) -> Product:
    """从 TOML 解析的 dict 构建 Product 对象。"""
    product_data = data.get("product", data)
    product_specs = product_data.get("product_specs", {})

    # 环境模型
    env: Environment | None = None
    env_raw = product_data.get("environment")
    if env_raw:
        temp = env_raw.get("temp_range", {})
        env = Environment(
            temp_range=TempRange(
                min=temp.get("min", -20),
                max=temp.get("max", 50),
                unit=temp.get("unit", "C"),
            ),
            ip_ratings=env_raw.get("ip_ratings"),
        )

    product = Product(
        name=product_data.get("name", "未命名产品"),
        schema_id=product_data.get("schema_id", "generic"),
        description=product_data.get("description"),
        product_specs=_deep_clean(product_specs),
        light_module=_deep_clean(product_data.get("light_module")),
        power_module=_deep_clean(product_data.get("power_module")),
        sensor_module=_deep_clean(product_data.get("sensor_module")),
        communication_module=_deep_clean(product_data.get("communication_module")),
        control_module=_deep_clean(product_data.get("control_module")),
        certification=_deep_clean(product_data.get("certification")),
        environment=env,
    )
    return product


def _deep_clean(obj: Any) -> Any:
    """递归清理 TOML 中可能的多余控制字段。"""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return {k: _deep_clean(v) for k, v in obj.items()
                if not k.startswith("_") and v is not None}
    return obj
