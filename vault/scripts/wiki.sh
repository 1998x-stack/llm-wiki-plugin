#!/usr/bin/env bash
# wiki.sh — Wrapper for all wiki Python scripts.
#
# Handles CWD and PYTHONPATH so scripts work from any directory.
# Usage: bash scripts/wiki.sh <script_name> [args...]
#
# Examples:
#   bash scripts/wiki.sh build_graph --full
#   bash scripts/wiki.sh lint_wiki --json
#   bash scripts/wiki.sh snapshot_index --update
#   bash scripts/wiki.sh search_wiki "牛顿法" --top 10 --json
#   bash scripts/wiki.sh qwen_ingest --raw raw/file.md

set -euo pipefail

# Resolve symlinks to find the real script location
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
    DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
    SOURCE="$(readlink "$SOURCE")"
    [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
VAULT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ $# -lt 1 ]; then
    echo "Usage: bash scripts/wiki.sh <script_name> [args...]"
    echo ""
    echo "Available scripts:"
    for f in "$SCRIPT_DIR"/*.py; do
        name=$(basename "$f" .py)
        [ "$name" = "wiki_utils" ] && continue
        [ "$name" = "__init__" ] && continue
        echo "  $name"
    done
    exit 1
fi

SCRIPT_NAME="$1"
shift

TARGET="$SCRIPT_DIR/${SCRIPT_NAME}.py"

if [ ! -f "$TARGET" ]; then
    echo "Error: script not found: $TARGET" >&2
    exit 1
fi

cd "$VAULT_DIR"
export PYTHONPATH="${SCRIPT_DIR}:${PYTHONPATH:-}"
exec python3 "$TARGET" "$@"
