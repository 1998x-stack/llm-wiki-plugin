---
type: entity
entity_type: tool
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, AI, 工具与框架, Agent系统]
aliases:
  - goose
  - Block Goose
relates_to:
  - target: "[[claude-cli-tools|Claude CLI 工具生态]]"
    type: part_of
    confidence: 0.9
  - target: "[[Claude-Code]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# Goose

## 概述

Goose 是由 Block（Jack Dorsey 旗下公司）开源的通用 AI Agent CLI 工具，定位为不限于编程的通用自动化平台。支持多后端模型（含 [[Claude_Code|Claude]]），具备插件生态，但在纯[[代码生成]]评测中准确率偏低（约 7%），不推荐纯编程场景。

## 关键内容

1. **通用 Agent 定位**：不专注于编程，适合通用自动化任务（文件操作、网络请求、工作流等）
2. **多后端模型支持**：可[[Configuration|配置]]为使用 [[Claude_Code|Claude]]、GPT 等各类 LLM 后端
3. **代码能力较弱**：2025 Q4 评测前端准确率仅 10%，后端 3.1%，不适合专业编码场景

### 安装

```bash
curl -fsSL https://github.com/block/goose/releases/... | sh
```

### 性能评测（2025 Q4）

| 指标 | Goose |
|------|-------|
| 综合准确率 | ~7% |
| 前端准确率 | 10.0% |
| 后端准确率 | 3.1% |

> 基础执行能力存在问题，纯编程场景不推荐。

## 来源

- [[raw/articles/programming/cli-tools/claude-cli-tools.md]] — Claude CLI 工具全景图 2026

## 相关

- [[claude-cli-tools|Claude CLI 工具生态]] — part_of
- [[Claude-Code]] — compares_to
