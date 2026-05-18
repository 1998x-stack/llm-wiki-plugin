---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-engineering, architecture, design-pattern, AI工程]
aliases: ["Agent Native Architecture", "Agent-Native Architecture"]
relates_to:
  - target: "[[Compound-Engineering]]"
    type: implements
    confidence: 0.8
  - target: "[[AI-Agent]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Context-Parity]]"
    type: part_of
    confidence: 0.7
  - target: "[[Action-Parity]]"
    type: part_of
    confidence: 0.7
supersedes: null
---

# Agent-Native Architecture

## 概述
Agent-Native Architecture 是一种为 AI Agent 设计的软件架构方法，确保 Agent 能够执行人类能执行的所有操作，看到与人类一样丰富的上下文。

## 关键内容

1. **核心概念**：
   - [[Action-Parity|Action Parity]]：Agent 能执行人类能执行的所有操作
   - [[Context-Parity|Context Parity]]：Agent 看到的上下文与人类一样丰富

2. **设计理念**：
   - 防止构建出只能做部分动作的伪自主系统
   - 确保 AI Agent 具备完整的操作能力
   - 使 Agent 能够在代码库中执行完整的开发任务

3. **实施要素**：
   - Git worktrees 为 Agent 提供隔离的工作空间
   - 丰富的文件上下文（[[CLAUDE.md]]、docs/）
   - 结构化输出格式支持

## 来源
- [[raw/articles/ai-engineering/prompt-context/compound-engineering-deep-analysis]]
- [[EveryInc/compound-engineering-plugin]]

## 相关
- [[Compound-Engineering]] — relates_to
- [[AI-Agent]] — relates_to
- [[Action-Parity]] — relates_to
- [[Context-Parity]] — relates_to