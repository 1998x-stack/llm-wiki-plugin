#!/bin/bash
# PostToolUse hook: rebuild graph.json after Write/Edit on wiki/ files
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')
FILE_PATH="$1"

if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/build_graph.py 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] GRAPH rebuild — OK" >> "$LOG"
else
    echo "[$TIMESTAMP] GRAPH rebuild — error: $(echo "$RESULT" | head -c 200)" >> "$LOG"
fi
