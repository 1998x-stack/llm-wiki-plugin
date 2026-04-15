#!/bin/bash
# Test: wiki:lint — runs lint_wiki.py and checks output
set -e
VAULT_DIR="$(cd "$(dirname "$0")/../../vault" && pwd)"
echo "=== wiki:lint test ==="
cd "$VAULT_DIR"
RESULT=$(python3 scripts/lint_wiki.py --json 2>&1) || true
echo "$RESULT" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Files: {d[\"total_files\"]}')
print(f'Errors: {d[\"errors\"]}')
print(f'Warnings: {d[\"warnings\"]}')
from collections import Counter
c = Counter(ch['check'] for ch in d['checks'])
for k, v in c.most_common():
    print(f'  {k}: {v}')
print('PASS' if d['errors'] == 0 else 'FAIL')
"
