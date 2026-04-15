#!/bin/bash
# PostToolUse hook: rebuild graph.json after Write/Edit on wiki/ files
# Receives JSON on stdin from Claude Code hooks system
# Includes 30s debounce to avoid rebuilding on rapid consecutive edits
VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
LOG="$VAULT_DIR/log.hook.md"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M')

# Read file_path from stdin JSON
FILE_PATH=$(cat | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get("tool_input",{}).get("file_path",""))' 2>/dev/null)

# Only process wiki content pages (not .claude/commands/wiki/)
if [[ -z "$FILE_PATH" ]] || [[ "$FILE_PATH" != *"wiki/"* ]] || [[ "$FILE_PATH" == *".claude/"* ]]; then
    exit 0
fi

# Debounce: skip if graph.json was rebuilt within last 30 seconds
GRAPH="$VAULT_DIR/graph.json"
if [ -f "$GRAPH" ]; then
    AGE=$(( $(date +%s) - $(stat -f %m "$GRAPH") ))
    if [ "$AGE" -lt 30 ]; then
        echo "[$TIMESTAMP] GRAPH skip — rebuilt ${AGE}s ago" >> "$LOG"
        exit 0
    fi
fi

RESULT=$(cd "$VAULT_DIR" && python3 scripts/build_graph.py 2>&1)
STATUS=$?

if [ $STATUS -eq 0 ]; then
    echo "[$TIMESTAMP] GRAPH rebuild — OK" >> "$LOG"
else
    echo "[$TIMESTAMP] GRAPH rebuild — error: $(echo "$RESULT" | head -c 200)" >> "$LOG"
fi
