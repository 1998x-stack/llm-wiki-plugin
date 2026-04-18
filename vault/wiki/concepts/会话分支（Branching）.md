---
type: concept
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["对话分支", "Fork Session", "会话分支"]
relates_to:
  - target: "[[Checkpoints 与 Rewind]]"
    type: depends_on
    confidence: 0.85
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# 会话分支（Branching）

## 概述
[[Claude Code]] 的会话分支功能允许从当前对话创建新会话分支（`/branch`，v2.1.77 中 `/fork` 更名为 `/branch`），保留完整对话历史，探索替代方案而不丢失原始上下文。

## 关键内容

1. **核心功能**：从当前对话的任意点创建新分支，新分支继承完整的消息历史、文件状态和上下文，但之后的修改互不影响。

2. **使用场景**：
   - 探索不同的实现方案
   - 在重大修改前创建安全分支
   - 对比多种设计选择
   - 实验性重构

3. **与 [[Checkpoints 与 Rewind|Checkpoints]] 的关系**：[[Checkpoints 与 Rewind|Checkpoints]] 是同一会话内的快照和回退，分支是创建独立的新会话。分支适合长期并行探索，[[Checkpoints 与 Rewind|Checkpoints]] 适合短期回退。

4. **命令**：`/branch [name]` 创建命名分支，`/fork` 是旧版别名（v2.1.77 已更名为 `/branch`）。

## 来源
- [[01-slash-commands/README.md]] — Claude HowTo 斜杠命令参考
- [[08-checkpoints/README.md]] — Claude HowTo Checkpoints 指南

## 相关
- [[Checkpoints 与 Rewind]] — depends_on
- [[斜杠命令（Slash Commands）]] — uses
