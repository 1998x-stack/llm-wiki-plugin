#!/bin/bash
# Script to cancel/remove specific ingest loop instances

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

show_usage() {
    echo "Usage: $0 <loop_type> <instance_number>"
    echo "  loop_type: claude or qwen"
    echo "  instance_number: the number of the instance to cancel"
    echo ""
    echo "Example: $0 claude 1  (removes tmp/ingest-loop.local.1.md)"
    echo "Example: $0 qwen 2   (removes tmp/ingest-loop-qwen.2.local.md)"
    echo ""
    echo "To see active loops: bash scripts/list-ingest-loops.sh"
}

if [ $# -ne 2 ]; then
    show_usage
    exit 1
fi

LOOP_TYPE="$1"
INSTANCE_NUM="$2"

# Validate inputs
if [ "$LOOP_TYPE" != "claude" ] && [ "$LOOP_TYPE" != "qwen" ]; then
    echo "Error: loop_type must be 'claude' or 'qwen'"
    show_usage
    exit 1
fi

if ! [[ "$INSTANCE_NUM" =~ ^[0-9]+$ ]]; then
    echo "Error: instance_number must be a positive integer"
    show_usage
    exit 1
fi

# Construct file path based on type
if [ "$LOOP_TYPE" = "claude" ]; then
    FILE_PATH="$VAULT_DIR/tmp/ingest-loop.local.$INSTANCE_NUM.md"
else
    FILE_PATH="$VAULT_DIR/tmp/ingest-loop-qwen.$INSTANCE_NUM.local.md"
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found: $FILE_PATH"
    echo "Available files:"
    find "$VAULT_DIR/tmp/" -name "*ingest-loop*" -type f
    exit 1
fi

echo "Attempting to cancel $LOOP_TYPE ingest loop instance #$INSTANCE_NUM"
echo "File: $FILE_PATH"
read -p "Are you sure you want to delete this file? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm "$FILE_PATH"
    echo "Successfully cancelled $LOOP_TYPE ingest loop instance #$INSTANCE_NUM"
else
    echo "Operation cancelled."
fi