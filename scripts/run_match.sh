#!/usr/bin/env bash
# run_match.sh — 一键仿真：pull Atlas → 跑引擎 → 报告回传 push
# 用法: ./scripts/run_match.sh <bom_file> [--scene-dir <dir>] [--output-dir <dir>]
# 默认: bom=engine/examples/bom_sample.toml, scene=../Atlas/scene-library/scenes, out=../Atlas/reports

set -euo pipefail

FORGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ATLAS_DIR="${ATLAS_DIR:-$FORGE_ROOT/../Atlas}"   # 可用环境变量覆盖
LOCK_FILE="${LOCK_FILE:-/tmp/run_match.lock}"

# 并发互斥锁：防止多实例同时操作 Atlas git 状态（stash/commit/push）
exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "❌ 已有 run_match.sh 在运行（$LOCK_FILE），退出" >&2
  exit 1
fi

BOM="${1:-$FORGE_ROOT/engine/examples/bom_sample.toml}"
shift || true
SCENE_DIR="$FORGE_ROOT/../Atlas/scene-library/scenes"
OUT_DIR="$FORGE_ROOT/../Atlas/reports"
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --scene-dir) SCENE_DIR="$2"; shift 2 ;;
    --output-dir) OUT_DIR="$2"; shift 2 ;;
    *) EXTRA_ARGS+=("$1"); shift ;;
  esac
done

PY="${PY:-/home/l/venvs/gputest/bin/python}"
if [[ ! -x "$PY" ]]; then PY="python3"; fi

echo "=== [1/4] pull Atlas 场景库 ==="
if [[ -d "$ATLAS_DIR/.git" ]]; then
  if ! git -C "$ATLAS_DIR" diff --quiet; then
    echo "⚠️  Atlas 有未提交改动，自动 stash"
    git -C "$ATLAS_DIR" stash push -m "run_match auto-stash"
    STASHED=1
  fi
  git -C "$ATLAS_DIR" pull --rebase || { echo "❌ Atlas pull 失败" >&2; [[ "${STASHED:-0}" == 1 ]] && git -C "$ATLAS_DIR" stash pop; exit 1; }
  if [[ "${STASHED:-0}" == 1 ]]; then
    git -C "$ATLAS_DIR" stash pop || echo "⚠️ stash pop 冲突，请手动处理" >&2
  fi
else
  echo "⚠️  Atlas 不在 $ATLAS_DIR，仅用本地缓存场景库" >&2
fi

echo "=== [2/4] 校验 BOM 与场景库 ==="
[[ -f "$BOM" ]] || { echo "❌ BOM 不存在: $BOM" >&2; exit 1; }
[[ -d "$SCENE_DIR" ]] || { echo "❌ 场景库不存在: $SCENE_DIR" >&2; exit 1; }

echo "=== [3/4] 跑 BOM 引擎 ==="
mkdir -p "$OUT_DIR"
(cd "$FORGE_ROOT/engine" && "$PY" -m src.cli match "$BOM" \
  --scene-dir "$SCENE_DIR" \
  --output-dir "$OUT_DIR" "${EXTRA_ARGS[@]}")

echo "=== [4/4] 报告回传 Atlas ==="
ATLAS_COMMIT="$(git -C "$ATLAS_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
REPORT_FILE="$OUT_DIR/bom_match_report.md"  # 引擎固定输出名
if [[ -f "$REPORT_FILE" ]]; then
  # 溯源：报告头标注场景库 commit
  if ! grep -q "scene-library commit" "$REPORT_FILE"; then
    sed -i "1i > 溯源: Atlas scene-library @ \`$ATLAS_COMMIT\`（run_match.sh 自动生成）\n" "$REPORT_FILE"
  fi
  echo "  报告: $REPORT_FILE (scene-library@$ATLAS_COMMIT)"
fi

if [[ -d "$ATLAS_DIR/.git" ]]; then
  # 只 add 本次生成的报告，避免误提交 reports/ 下无关文件
  if [[ -n "$REPORT_FILE" ]]; then
    git -C "$ATLAS_DIR" add -- "$REPORT_FILE" 2>/dev/null || true
  fi
  if ! git -C "$ATLAS_DIR" diff --cached --quiet; then
    git -C "$ATLAS_DIR" commit -m "report: BOM 场景匹配报告（scene-library@$ATLAS_COMMIT）"
    git -C "$ATLAS_DIR" pull --rebase && git -C "$ATLAS_DIR" push
    echo "✅ 已推送报告到 Atlas"
  else
    echo "ℹ️ 无新报告变更，跳过提交"
  fi
else
  echo "⚠️ Atlas 非 git 仓库，报告留在 $OUT_DIR"
fi

echo "=== 完成 ==="
