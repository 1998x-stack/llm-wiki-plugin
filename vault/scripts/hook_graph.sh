#!/bin/bash
# PostToolUse hook: rebuild graph.json after Write/Edit on wiki/ files
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

RESULT=$(cd "$VAULT_DIR" && python3 scripts/build_graph.py 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] GRAPH rebuild — OK" >> "$LOG"
else
    echo "[$TIMESTAMP] GRAPH rebuild — error: $(echo "$RESULT" | head -c 200)" >> "$LOG"
fi
