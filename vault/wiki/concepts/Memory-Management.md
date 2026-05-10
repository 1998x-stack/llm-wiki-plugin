---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [context-engineering, memory-system, ai-architecture]
aliases: ["记忆管理", "Memory Management"]
relates_to:
  - {target: "[[Context-Design]]", type: relates_to, confidence: 0.7}
  - {target: "[[Hierarchical-Context-Memory]]", type: relates_to, confidence: 0.8}
  - {target: "[[Context-Engineering]]", type: relates_to, confidence: 0.7}
  - {target: "[[Agent-System]]", type: relates_to, confidence: 0.7}
  - {target: "[[Compression]]", type: relates_to, confidence: 0.8}
supersedes: null
---

# Memory-Management

## 概述
记忆管理是AI系统中对上下文、状态和知识进行有效组织、存储和检索的策略与技术，旨在在有限的[[上下文窗口]]内最大化信息的有效性和可用性。

## 关键内容

1. **压缩策略**：
   压缩的目标不是简单的文本缩减，而是将"历史噪音"转化为"未来可[[计算]]状态"。压缩应产出持久事实、已做决策、开放循环和源锚点四类对象，避免关键信息失真。

2. **状态外置**：
   对于工具密集型Agent，应将工具状态外置存储，仅回注必要结果到上下文中。这包括结果摘要、关键增量、错误信息和下一步所需最小证据。

3. **触发机制**：
   压缩触发条件应基于任务阶段切换、关键决策做出、工具返回超长结果或token预算逼近阈值，而非简单的消息数量阈值。

## 来源
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 概念描述
- [[Anthropic Context Engineering]] — 原理参考

## 相关
- [[Context-Design]] — relates_to
- [[Hierarchical-Context-Memory]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Agent-System]] — relates_to
- [[Compression]] — relates_to