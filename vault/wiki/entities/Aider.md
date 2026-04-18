---
type: entity
entity_type: tool
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, AI, 工具与框架, AI工程]
aliases:
  - aider-chat
  - Aider CLI
relates_to:
  - target: "[[claude-cli-tools|Claude CLI 工具生态]]"
    type: part_of
    confidence: 0.95
  - target: "[[Claude-Code]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Codex CLI]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# Aider

## 概述

Aider 是由 Paul Gauthier 开源的 Git 原生 AI 结对编程 CLI 工具，支持 Claude、GPT-4o、[[Gemini CLI|Gemini]] 及本地模型。以极高的 Token 效率著称（综合测试仅消耗 126k tokens），是 Claude CLI 生态中性价比最高的工具之一。

## 关键内容

1. **Git 原生集成**：所有改动自动 commit，保持清晰的 Git 历史，架构最轻量
2. **Token 效率冠军**：2025 Q4 评测中，平均 Token 消耗 126k，约为 [[Claude Code]]（397k）的三分之一
3. **多模型支持**：除 Claude 外，兼容 GPT-4o、[[Gemini CLI|Gemini]]、本地模型，跨平台可选

### 安装与基础用法

```bash
uv tool install aider-chat

aider --model claude-sonnet-4-5              # 指定模型
aider --message "重构认证模块" src/auth.py   # 非交互单次执行
aider --yes                                  # 自动确认所有更改
aider --no-git                               # 不使用 git
```

### 性能评测（2025 Q4）

| 指标 | Aider | [[Claude Code]] |
|------|-------|-------------|
| 综合准确率 | 52.7% | 55.5% |
| Token 消耗 | 126k | 397k |
| 前端准确率 | — | 95.0% |

> Aider 适合需要频繁提交、注重成本控制的开源项目或长上下文任务。

## 来源

- [[raw/articles/programming/cli-tools/claude-cli-tools.md]] — Claude CLI 工具全景图 2026

## 相关

- [[claude-cli-tools|Claude CLI 工具生态]] — part_of
- [[Claude-Code]] — compares_to
- [[Codex CLI]] — compares_to
