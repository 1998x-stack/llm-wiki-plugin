#!/bin/bash
# PostToolUse hook: update BM25 index after Write/Edit on wiki/ files
FILE_PATH="$1"
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/bm25_index.py update "$FILE_PATH" 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] BM25 $FILE_PATH — indexed" >> "$LOG"
else
    echo "[$TIMESTAMP] BM25 $FILE_PATH — error: $(echo "$RESULT" | head -c 200)" >> "$LOG"
fi
