#!/bin/bash
# Test: wiki:graph — runs build_graph.py --full
set -e
VAULT_DIR="$(cd "$(dirname "$0")/../../vault" && pwd)"
STATIC_DIR="$(cd "$(dirname "$0")/../.." && pwd)/static"
echo "=== wiki:graph test ==="
cd "$VAULT_DIR"
RESULT=$(python3 scripts/build_graph.py --output "$STATIC_DIR/graph.json" --full 2>/dev/null)
echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Nodes: {d[\"nodes\"]}')
print(f'Edges: {d[\"edges\"]}')
print(f'Orphans: {d[\"orphans\"]}')
print(f'Components: {d[\"components\"]}')
# Verify outputs exist
import os
for f in ['$STATIC_DIR/graph.json', '$STATIC_DIR/graph-statistics.json', '$STATIC_DIR/wiki/index.html']:
    status = 'OK' if os.path.exists(f) else 'MISSING'
    print(f'  {status}: {f}')
print('PASS' if d['status'] == 'ok' else 'FAIL')
"
