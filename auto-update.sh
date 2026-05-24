#!/bin/bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
LOG_DIR="$REPO_DIR/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== 开始自动更新 ==="

cd "$REPO_DIR"

log "拉取最新代码..."
git pull --rebase || true

log "执行 price-grep..."
uv run price-grep 2>&1 | tee -a "$LOG_FILE"

log "执行 news-read..."
uv run news-read 2>&1 | tee -a "$LOG_FILE"

if git diff --quiet; then
  log "无数据变更，跳过提交"
else
  log "检测到数据变更，提交并推送..."
  git add -A
  git commit -m "update data $(date +%Y-%m-%d)"
  git push
  log "推送完成"
fi

log "=== 更新结束 ==="
