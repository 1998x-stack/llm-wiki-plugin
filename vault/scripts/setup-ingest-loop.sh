#!/bin/bash
# Setup script for wiki:ingest-loop ralph-loop mechanism with concurrent support
set -e

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
INPUT_PATH="$1"

if [ -z "$INPUT_PATH" ]; then
    echo "Error: No input path provided."
    echo "Usage: bash scripts/setup-ingest-loop.sh <folder_or_file_path>"
    exit 1
fi

if [[ "$INPUT_PATH" != /* ]]; then
    # First check if path exists as-is relative to vault
    FULL_PATH="$VAULT_DIR/$INPUT_PATH"
    if [ ! -e "$FULL_PATH" ]; then
        # If not found, try adding raw/ prefix (for wiki:ingest-loop compatibility)
        FULL_PATH="$VAULT_DIR/raw/$INPUT_PATH"
        if [ ! -e "$FULL_PATH" ]; then
            echo "Error: Path not found: $VAULT_DIR/$INPUT_PATH or $VAULT_DIR/raw/$INPUT_PATH"
            exit 1
        fi
        # Update INPUT_PATH to reflect the actual path used
        INPUT_PATH="raw/$INPUT_PATH"
    fi
else
    FULL_PATH="$INPUT_PATH"
    if [ ! -e "$FULL_PATH" ]; then
        echo "Error: Path not found: $FULL_PATH"
        exit 1
    fi
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

# Find the first available numbered state file
COUNTER=1
while [ -f "$VAULT_DIR/tmp/ingest-loop.local.$COUNTER.md" ]; do
    COUNTER=$((COUNTER + 1))
done
STATE_FILE="$VAULT_DIR/tmp/ingest-loop.local.$COUNTER.md"

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

echo "=== Ingest Loop Setup (Concurrent Instance #$COUNTER) ==="
echo "Source: $INPUT_PATH"
echo "Files to process: $TOTAL"
echo "State file: $STATE_FILE"
echo ""
echo "To cancel: delete $STATE_FILE"
echo ""
echo "Completion promise: ALL_FILES_INGESTED"
echo "Output <promise>ALL_FILES_INGESTED</promise> ONLY when all files are done."
