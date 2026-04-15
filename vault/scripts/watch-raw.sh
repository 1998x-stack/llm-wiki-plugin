#!/usr/bin/env bash
# watch-raw.sh — 监控 raw/ 目录，新文件自动触发 ingest
#
# 依赖: fswatch (brew install fswatch)
# 用法: ./scripts/watch-raw.sh
# 停止: Ctrl+C

set -euo pipefail

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Watching $VAULT_DIR/raw/ for new files..."
echo "Press Ctrl+C to stop."

fswatch -0 --event Created "$VAULT_DIR/raw/" | while IFS= read -r -d '' file; do
  basename="$(basename "$file")"
  if [[ "$basename" == .* ]]; then
    continue
  fi

  echo "[$(date '+%Y-%m-%d %H:%M:%S')] New file detected: $file"

  rel_path="${file#$VAULT_DIR/raw/}"

  echo "Triggering ingest for: $rel_path"
  cd "$VAULT_DIR" && claude -p "/wiki:ingest $rel_path" 2>&1 | tail -5

  echo "---"
done
