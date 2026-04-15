#!/bin/bash
# PostToolUse hook: lint wiki page after Write/Edit
# Receives JSON on stdin from Claude Code hooks system
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Read file_path from stdin JSON
FILE_PATH=$(cat | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null)

# Only process wiki content pages (not .claude/commands/wiki/)
if [[ -z "$FILE_PATH" ]] || [[ "$FILE_PATH" != *"wiki/"* ]] || [[ "$FILE_PATH" == *".claude/"* ]]; then
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
