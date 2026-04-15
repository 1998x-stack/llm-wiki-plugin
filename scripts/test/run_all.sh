#!/bin/bash
# Master test runner for wiki commands via Claude SDK
# Usage: bash scripts/test/run_all.sh
set -e

PROJ_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
TEST_DIR="$PROJ_DIR/scripts/test"
LOG_DIR="$TEST_DIR/logs"
mkdir -p "$LOG_DIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H%M')

echo "=== Wiki Command Test Suite ==="
echo "Project: $PROJ_DIR"
echo "Timestamp: $TIMESTAMP"
echo ""

COMMANDS=(lint graph reindex query)

for cmd in "${COMMANDS[@]}"; do
    script="$TEST_DIR/run_${cmd}.sh"
    log="$LOG_DIR/${cmd}_${TIMESTAMP}.log"
    
    if [ ! -f "$script" ]; then
        echo "SKIP: $script not found"
        continue
    fi
    
    echo "--- Testing wiki:${cmd} ---"
    if bash "$script" > "$log" 2>&1; then
        echo "PASS: wiki:${cmd} (log: $log)"
    else
        echo "FAIL: wiki:${cmd} (exit $?, log: $log)"
    fi
    echo ""
done

echo "=== Done ==="
