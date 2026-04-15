#!/bin/bash
# Test: wiki:query — runs bm25_index.py query
set -e
VAULT_DIR="$(cd "$(dirname "$0")/../../vault" && pwd)"
echo "=== wiki:query test ==="
cd "$VAULT_DIR"
RESULT=$(python3 scripts/bm25_index.py query "贝叶斯定理" -n 3 2>/dev/null)
echo "$RESULT" | python3 -c "
import sys, json
results = json.load(sys.stdin)
print(f'Results: {len(results)}')
for r in results:
    print(f'  {r[\"title\"]} (score: {r[\"score\"]})')
print('PASS' if len(results) > 0 else 'FAIL')
"
