#!/bin/bash
# Script to list all active ingest loops in the tmp directory

VAULT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

echo "Active Claude Engine Ingest Loops:"
CLAUDE_LOOPS=($(find "$VAULT_DIR/tmp/" -name "ingest-loop.local.*.md" 2>/dev/null))
if [ ${#CLAUDE_LOOPS[@]} -eq 0 ]; then
    echo "  None"
else
    for loop_file in "${CLAUDE_LOOPS[@]}"; do
        counter=$(echo "$loop_file" | sed 's/.*ingest-loop\.local\.\([0-9]*\)\.md/\1/')
        current_index=$(grep "current_index:" "$loop_file" | cut -d':' -f2 | tr -d ' ')
        total=$(grep "total:" "$loop_file" | cut -d':' -f2 | tr -d ' ')
        source_path=$(grep "source_path:" "$loop_file" | sed 's/source_path: "\(.*\)"/\1/' | sed 's/^ *//;s/ *$//')
        echo "  Loop #$counter: $current_index/$total - Source: $source_path"
    done
fi

echo ""
echo "Active Qwen Engine Ingest Loops:"
QWEN_LOOPS=($(find "$VAULT_DIR/tmp/" -name "ingest-loop-qwen.*.local.md" 2>/dev/null))
if [ ${#QWEN_LOOPS[@]} -eq 0 ]; then
    echo "  None"
else
    for loop_file in "${QWEN_LOOPS[@]}"; do
        counter=$(echo "$loop_file" | sed 's/.*ingest-loop-qwen\.\([0-9]*\)\.local\.md/\1/')
        current_index=$(grep "current_index:" "$loop_file" | cut -d':' -f2 | tr -d ' ')
        total=$(grep "total:" "$loop_file" | cut -d':' -f2 | tr -d ' ')
        source_path=$(grep "source_path:" "$loop_file" | sed 's/source_path: "\(.*\)"/\1/' | sed 's/^ *//;s/ *$//')
        echo "  Loop #$counter: $current_index/$total - Source: $source_path"
    done
fi

echo ""
echo "Legacy (non-concurrent) Ingest Loops (will not be managed by new system):"
echo "  (Note: Legacy system no longer used - all loops now stored in tmp/ directory)"