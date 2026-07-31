#!/usr/bin/env bash
# verify_engine.sh — 本地引擎自检（不依赖 Atlas，用内置示例）
# 用法: ./scripts/verify_engine.sh

set -euo pipefail

FORGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="${PY:-/home/l/venvs/gputest/bin/python}"
if [[ ! -x "$PY" ]]; then PY="python3"; fi

echo "=== 引擎自检（示例 BOM）==="
if [[ -d "$FORGE_ROOT/../Atlas/scene-library/scenes" ]]; then
  (cd "$FORGE_ROOT/engine" && "$PY" -m src.cli match examples/bom_sample.toml \
    --scene-dir "$FORGE_ROOT/../Atlas/scene-library/scenes" --output-dir /tmp/forge_verify)
else
  echo "⚠️ 未找到 Atlas 场景库，用内置示例（仅验证不崩）"
  (cd "$FORGE_ROOT/engine" && "$PY" -m src.cli match examples/bom_sample.toml --output-dir /tmp/forge_verify)
fi

echo "=== 语法检查 ==="
"$PY" -m py_compile "$FORGE_ROOT"/engine/src/*.py
echo "✅ 引擎自检通过"
