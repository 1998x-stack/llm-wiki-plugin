#!/bin/bash
# PostToolUse hook: lint wiki page after Write/Edit
FILE_PATH="$1"
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

if [[ "$FILE_PATH" != *"wiki/"* ]]; then
    exit 0
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/lint_wiki.py --file "$FILE_PATH" --json 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] LINT $FILE_PATH — OK" >> "$LOG"
elif [ $STATUS -eq 1 ]; then
    WARNINGS=$(echo "$RESULT" | python3 -c 'import sys,json; r=json.load(sys.stdin); print(", ".join(c["message"] for c in r.get("checks",[])))' 2>/dev/null || echo "parse error")
    echo "[$TIMESTAMP] LINT $FILE_PATH — WARN: $WARNINGS" >> "$LOG"
else
    echo "[$TIMESTAMP] LINT $FILE_PATH — ERROR: $(echo "$RESULT" | head -c 200)" >> "$LOG"
fi
