---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [context-engineering, memory-system, ai-architecture, AI工程]
aliases: ["分层上下文记忆", "Hierarchical Context Memory", "HCM"]
relates_to:
  - {target: "[[Context-Design]]", type: implements, confidence: 0.9}
  - {target: "[[Context-Engineering]]", type: relates_to, confidence: 0.7}
  - {target: "[[Memory-Management]]", type: part_of, confidence: 0.8}
  - {target: "[[Zipf-定律]]", type: implements, confidence: 0.7}
  - {target: "[[Pareto-原理]]", type: implements, confidence: 0.7}
supersedes: null
---

# Hierarchical-Context-Memory

## 概述
[[分层记忆架构|分层上下文]]记忆(Hierarchical Context Memory, HCM)是一种[[Context Management|上下文管理]]架构，将有限上下文分为多个层次，每层有动态的token预算，以实现高效的上下文利用和管理。

## 关键内容

1. **分层架构**：
   HCM采用五层内存结构：L0(不可变前缀)、L1(会话合约)、L2(工作上下文)、L3(情景记忆)、L4([[语义记忆]])，每层分配不同比例的动态token预算。

2. **热/温/冷分层**：
   基于Zipf/Pareto定律，绝大多数价值来自少数热点上下文，因此将上下文分为热/温/冷三层，而非所有历史平权处理。热数据频繁访问，冷数据归档存储。

3. **预算分配策略**：
   典型分配方案为：10-15%用于静态前缀，8-12%用于会话合约，20-30%用于工作集，其余用于证据和预留空间。整体使用65-75%的完整上下文以留出输出和推理空间。

## 来源
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 概念提出
- [[MemGPT]] — 分层记忆实践

## 相关
- [[Context-Design]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Memory-Management]] — relates_to
- [[Zipf-定律]] — relates_to
- [[Pareto-原理]] — relates_to