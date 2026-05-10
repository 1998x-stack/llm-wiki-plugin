---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, theory, machine-learning]
aliases: [Hornik 1989, 万能近似定理论文]
relates_to:
  - target: 万能近似定理
    relation: introduced
  - target: 多层感知机
    relation: analyzed
supersedes: null
---

# Multilayer Feedforward Networks are Universal Approximators (1989 论文)

## 概述
证明具有单个隐藏层的[[多层感知机（MLP）|前馈神经网络]]可以以任意精度近似任何连续函数的理论论文。

## 关键内容

1. **[[万能近似定理]]**：证明只要隐藏层有足够多的神经元，前馈网络可以近似任何从紧致子集到实数的连续函数。
2. **理论意义**：为神经网络的表达能力提供了严格的数学保证，解释了为什么神经网络可以拟合复杂的数据分布。
3. **局限性**：定理只保证存在性，不涉及如何找到这些权重（训练问题），这留给了 [[反向传播（Backpropagation）]] 等[[算法]]。

## 来源
- [[ai_papers_timeline.md]] — 1989 年时间线条目

## 相关
- [[万能近似定理]] — introduced
- [[多层感知机]] — analyzed
- [[反向传播（Backpropagation）]] — relates_to
