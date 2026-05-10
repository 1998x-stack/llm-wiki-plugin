---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-agent, architecture, design-pattern]
aliases: ["Context Parity", "Context-Parity"]
relates_to:
  - target: "[[Agent-Native-Architecture]]"
    type: part_of
    confidence: 0.9
  - target: "[[AI-Agent]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Context Parity

## 概述
Context Parity 是 [[Agent-Native-Architecture|Agent-Native Architecture]] 的核心概念之一，指 AI Agent 应看到与人类开发者同样丰富的上下文信息。

## 关键内容

1. **定义**：
   - Agent 看到的上下文与人类一样丰富
   - 确保 AI Agent 获取完整的项目上下文信息

2. **实现方式**：
   - 提供完整的代码库视图
   - 传递必要的项目文档和约定
   - 共享设计决策和历史信息

3. **重要性**：
   - 确保 Agent 基于充分信息做出决策
   - 避免因上下文不足导致的错误

## 来源
- [[raw/articles/ai-engineering/prompt-context/compound-engineering-deep-analysis]]
- [[EveryInc/compound-engineering-plugin]]

## 相关
- [[Agent-Native-Architecture]] — part_of
- [[Action-Parity]] — relates_to
- [[AI-Agent]] — relates_to