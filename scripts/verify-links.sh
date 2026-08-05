#!/usr/bin/env bash
# verify-links.sh — 双仓互链验证：A/F 两侧互链相对路径均有效
# 用法: ./scripts/verify-links.sh
# 互链清单与 COLLAB.md「双仓同步协议」保持一致；新增互链时同步更新两处

set -euo pipefail

FORGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
ATLAS_ROOT="${ATLAS_ROOT:-$FORGE_ROOT/../Atlas}"  # CI 可用环境变量覆盖（checkout 到别的路径）

fail=0

check() {  # $1=仓根  $2=来源文件（仓根相对）  $3=链接相对路径（相对来源文件所在目录）
  local root="$1" from="$2" link="$3"
  local base="$root/$(dirname "$from")"
  if (cd "$base" && [[ -e $link ]]) 2>/dev/null; then
    echo "✅ $from → $link"
  else
    echo "❌ $from → $link（目标缺失）"
    fail=1
  fi
}

if [[ ! -d "$ATLAS_ROOT/.git" ]]; then
  echo "⚠️ Atlas 不在 $ATLAS_ROOT（期望为 Forge 的兄弟目录）" >&2
  exit 1
fi

echo "=== A → F 链接 ==="
check "$ATLAS_ROOT" "README.md" "../Forge"
check "$ATLAS_ROOT" "tech-plans/4week-awakening.md" "../../Forge/w1/README.md"
check "$ATLAS_ROOT" "plan/courses.md" "../../Forge/w1/README.md"
check "$ATLAS_ROOT" "plan/courses.md" "../../Forge/w1/architecture/00-system-overview.md"

echo "=== F → A 链接 ==="
check "$FORGE_ROOT" "README.md" "../Atlas/tech-plans/ROADMAP.md"
check "$FORGE_ROOT" "w1/README.md" "../../Atlas/tech-plans/4week-awakening.md"
check "$FORGE_ROOT" "w1/architecture/00-system-overview.md" "../../../Atlas/plan/courses.md"
check "$FORGE_ROOT" "w1/architecture/00-system-overview.md" "../../../Atlas/tech-plans/4week-awakening.md"

if [[ $fail -eq 0 ]]; then
  echo "✅ 全部互链有效"
else
  echo "❌ 存在失效链接（见上）" >&2
  exit 1
fi
