#!/bin/bash
# Setup script for wiki:ingest-loop ralph-loop mechanism
set -e

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
STATE_FILE="$VAULT_DIR/.claude/ingest-loop.local.md"
INPUT_PATH="$1"

if [ -z "$INPUT_PATH" ]; then
    echo "Error: No input path provided."
    echo "Usage: bash scripts/setup-ingest-loop.sh <folder_or_file_path>"
    exit 1
fi

if [[ "$INPUT_PATH" != /* ]]; then
    FULL_PATH="$VAULT_DIR/$INPUT_PATH"
else
    FULL_PATH="$INPUT_PATH"
fi

if [ ! -e "$FULL_PATH" ]; then
    echo "Error: Path not found: $FULL_PATH"
    exit 1
fi

if [ -f "$FULL_PATH" ]; then
    echo "Single file detected. No loop setup needed."
    echo "SINGLE_FILE=$INPUT_PATH"
    exit 0
fi

FILES=()
while IFS= read -r -d '' file; do
    rel=$(python3 -c "import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))" "$file" "$VAULT_DIR")
    FILES+=("$rel")
done < <(find "$FULL_PATH" -type f \( -name "*.md" -o -name "*.jsonl" \) -print0 | sort -z)

TOTAL=${#FILES[@]}

if [ "$TOTAL" -eq 0 ]; then
    echo "Error: No processable files found in $INPUT_PATH"
    exit 1
fi

FILES_YAML=""
for f in "${FILES[@]}"; do
    FILES_YAML="$FILES_YAML  - \"$f\"\n"
done

STARTED=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
SESSION_ID=$(uuidgen 2>/dev/null || python3 -c "import uuid; print(uuid.uuid4())")

cat > "$STATE_FILE" << STATEEOF
---
active: true
source_path: "$INPUT_PATH"
files:
$(echo -e "$FILES_YAML")
current_index: 0
total: $TOTAL
completed: []
failed: []
started_at: "$STARTED"
session_id: "$SESSION_ID"
completion_promise: "ALL_FILES_INGESTED"
---

# Ingest Loop State

This file tracks the progress of batch ingest. Do not edit manually.
STATEEOF

echo "=== Ingest Loop Setup ==="
echo "Source: $INPUT_PATH"
echo "Files to process: $TOTAL"
echo "State file: $STATE_FILE"
echo ""
echo "To cancel: delete $STATE_FILE"
echo ""
echo "Completion promise: ALL_FILES_INGESTED"
echo "Output <promise>ALL_FILES_INGESTED</promise> ONLY when all files are done."
