---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 4
tags: [计算复杂度理论, 算法理论, NP完全性]
aliases: ["NP-Completeness", "NP完全问题", "NP完备性"]
relates_to:
  - target: "[[Cook定理]]"
    type: defined_by
    confidence: 0.9
  - target: "[[P vs NP问题]]"
    type: central_to
    confidence: 0.9
  - target: "[[多项式时间归约]]"
    type: relies_on
    confidence: 0.9
  - target: "[[Stephen Cook]]"
    type: pioneered_by
    confidence: 0.9
supersedes: null
---

# NP完全性

## 概述
NP完全性是计算复杂度理论中的核心概念，指的是一类在NP中的"最难"问题。这类问题具有一个特殊性质：如果其中任何一个存在多项式时间算法，那么所有NP问题都存在多项式时间算法。

## 关键内容
1. **定义**：一个问题L是NP完全的，如果：(1) L ∈ NP（属于NP类）；(2) 对于NP中的每一个问题L'，都有L' ≤ₚ L（NP中所有问题都可以多项式时间归约到L）。

2. **历史意义**：NP完全性概念由Stephen Cook于1971年在其开创性论文中定义，并通过Cook定理证明了布尔可满足性问题(SAT)是NP完全的，从而建立了整个理论框架。

3. **重要性**：NP完全性揭示了大量看似无关的组合优化问题（来自逻辑学、图论、数论、运筹学等不同领域）在计算复杂度上是等价的。这意味着这些问题要么都有高效的多项式时间算法，要么都没有（假设P ≠ NP）。

4. **现实影响**：NP完全性理论彻底改变了算法研究的方法论。研究者不再盲目寻找精确的多项式时间算法，而是先证明问题的复杂度，再选择合适的策略（近似算法、启发式方法或特殊情况下的高效算法）。

## 来源
- [[08-cook-np-completeness]] — 概念起源与发展
- [[Cook定理]] — 定义与证明
- [[Stephen Cook]] — 创始人
- [[多项式时间归约]] — 核心工具

## 相关
- [[Cook定理]] — defined by
- [[P vs NP问题]] — central to
- [[多项式时间归约]] — relies on
- [[布尔可满足性问题]] — first example
- [[计算复杂度理论]] — field of study