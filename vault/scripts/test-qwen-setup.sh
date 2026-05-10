#!/bin/bash
# Test script to verify the concurrent Qwen setup script works properly
echo "Testing Qwen concurrent setup script..."

# Check if DASHSCOPE_API_KEY is set, if not set a fake one for testing only
if [ -z "$DASHSCOPE_API_KEY" ]; then
    export DASHSCOPE_API_KEY="fake_test_key_for_setup_only"
fi

bash scripts/setup-ingest-loop-qwen.sh "raw/articles/programming"