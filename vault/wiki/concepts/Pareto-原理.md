---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [context-engineering, economics, power-laws]
aliases: ["帕累托原理", "二八定律", "Pareto Principle"]
relates_to: []
supersedes: null
---

# Pareto-原理

## 概述
[[帕累托]]原理（Pareto Principle），又称80/20法则或二八定律，指出在许多情况下，约80%的结果来自20%的原因。在Context Design中，Pareto原理被用来构建[[Context-Design|Pareto-aware Context OS]]，将上下文视为有限缓存而非聊天记录拼接器。

## 关键内容

1. **基本原理**：
   [[帕累托]]原理描述了不平衡分布现象，即大部分效果往往来自于小部分原因。这一原理不仅适用于经济学，在工程、科学和技术领域也有广泛应用。

2. **在Context Design中的应用**：
   在[[Context Engineering|上下文工程]]中，绝大多数价值来自少数热点上下文，所以需要做热/温/冷分层，而不是所有历史平权。这一原则引导构建了[[Context-Design|Pareto-aware Context OS]]。

3. **系统设计影响**：
   - 重点关注高价值上下文的优化
   - 实现分层存储策略
   - 优化资源分配效率

## 来源
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 在Context Design中的应用
- [[经济管理理论]] — 理论基础

## 相关
- [[Context Design]] — applies_to
- [[Zipf-定律]] — relates_to
- [[分层记忆]] — implements
- [[价值密度]] — relates_to