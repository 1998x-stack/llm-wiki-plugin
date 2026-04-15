# Gotchas & Known Issues

This document tracks known issues, workarounds, and lessons learned from running LLM Wiki operations.

## Qwen API Integration

### Issue: Model Name Mismatch
**Date**: 2026-04-15  
**Command**: `wiki:ingest-loop-qwen`  
**Error**: `The model 'qwen3-plus' does not exist or you do not have access to it.`

**Root Cause**: 
The `scripts/qwen_ingest.py` script was configured to use model `qwen3-plus`, but this model does not exist in the DashScope API. Available models include:
- `qwen3.5-plus` (working replacement)
- `qwen3.6-plus`
- `qwen3.5-flash`

**Fix Applied**:
Changed line 240 in `scripts/qwen_ingest.py`:
```python
# Before:
model="qwen3-plus"

# After:
model="qwen3.5-plus"
```

**Validation**:
- All 3 files processed successfully with `qwen3.5-plus`
- API calls completed without authentication errors
- Output quality maintained

**Recommendation**:
Periodically verify model names against DashScope API:
```bash
curl -s -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  https://dashscope.aliyuncs.com/api/v1/models | grep -i qwen
```

---

## General Patterns

### Pattern: Lint Warnings on Generated Content
**Issue**: Qwen-generated pages often exceed overview length limits (200 chars)  
**Impact**: Non-blocking warnings in lint output  
**Action**: Manual review and editing required for optimization  
**Example**: `claude-cli-tools.md` generated overview with 341 chars

---

## Environment Setup

### Python Dependencies
Ensure all required packages are installed:
```bash
pip install -r requirements.txt
```

Key packages:
- `openai` (for Qwen API access)
- `pyyaml` (for frontmatter parsing)
- `jieba`, `rank_bm25` (for search indexing)
