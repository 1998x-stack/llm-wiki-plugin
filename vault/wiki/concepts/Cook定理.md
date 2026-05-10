---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [计算复杂度理论, 算法理论, NP完全性]
aliases: ["Cook's Theorem", "Cook-Levin理论"]
relates_to:
  - target: "[[NP完全性]]"
    type: extends
    confidence: 0.9
  - target: "[[布尔可满足性问题]]"
    type: proves_is_NP_complete
    confidence: 0.9
  - target: "[[Stephen Cook]]"
    type: developed_by
    confidence: 0.9
  - target: "[[计算复杂度理论]]"
    type: foundational_to
    confidence: 0.9
supersedes: null
---

# Cook定理

## 概述
Cook定理是计算复杂度理论中的核心定理，证明了布尔可满足性问题(SAT)是NP完全的，为NP完全性理论奠定了基础。

## 关键内容
1. **定理内容**：布尔可满足性问题(SAT)是NP完全的。这意味着SAT既属于NP类，又属于NP中最困难的问题——所有NP问题都可以在多项式时间内归约到SAT。

2. **证明方法**：Cook通过将非确定性图灵机的计算过程编码为布尔公式，展示了任何NP问题的求解可以转化为SAT问题的求解。具体来说，图灵机的计算表(计算过程的二维表示)被系统性地编码为一组布尔约束。

3. **重要意义**：这一定理首次确立了NP完全性的概念，揭示了大量看似无关的组合优化问题在计算复杂度上是等价的。它标志着计算复杂度理论进入了一个新纪元，成为理解计算难度的基石。

4. **历史背景**：该定理由Stephen Cook在1971年首次提出，随后Leonid Levin独立发现了类似结果。这一发现催生了整个NP完全性理论，影响了算法设计、密码学、人工智能等多个领域。

## 来源
- [[08-cook-np-completeness]] — 论文分析及证明细节
- [[Stephen Cook]] — 原始发现者
- [[Leonid Levin]] — 独立发现者

## 相关
- [[NP完全性]] — extends
- [[布尔可满足性问题]] — proves is NP-complete
- [[计算复杂度理论]] — foundational to
- [[多项式时间归约]] — proof technique
- [[非确定性图灵机]] — proof technique