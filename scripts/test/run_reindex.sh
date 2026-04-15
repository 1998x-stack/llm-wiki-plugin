#!/bin/bash
# Test: wiki:reindex — runs snapshot_index.py check + update
set -e
VAULT_DIR="$(cd "$(dirname "$0")/../../vault" && pwd)"
echo "=== wiki:reindex test ==="
cd "$VAULT_DIR"
RESULT=$(python3 scripts/snapshot_index.py 2>&1)
echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Wiki pages: {d[\"total_wiki\"]}')
print(f'Indexed: {d[\"total_indexed\"]}')
print(f'Missing: {len(d[\"missing\"])}')
print(f'Orphaned: {len(d[\"orphaned\"])}')
print('PASS' if d['ok'] else 'FAIL')
"
