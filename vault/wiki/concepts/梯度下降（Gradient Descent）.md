---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [优化算法, 深度学习, 数学]
aliases: ["Gradient Descent", "梯度下降法", "最速下降法", "GD"]
relates_to:
  - target: "[[反向传播（Backpropagation）]]"
    type: complement_algorithm
    confidence: 0.95
  - target: "[[随机梯度下降（SGD）]]"
    type: variant_of
    confidence: 0.9
  - target: "[[学习率]]"
    type: uses_parameter
    confidence: 0.95
  - target: "[[链式法则]]"
    type: works_with
    confidence: 0.85
  - target: "[[损失函数]]"
    type: optimizes
    confidence: 0.95
supersedes: null
---

# 梯度下降（Gradient Descent）

## 概述
梯度下降是最基础的优化[[算法]]，通过沿损失函数梯度的反方向迭代更新参数，逐步寻找损失的最小值，是所有神经网络训练的核心引擎。与[[反向传播（Backpropagation）]][[算法]]配合，共同完成神经网络的训练过程。

## 关键内容

1. **基本原理**：梯度指向函数增长最快的方向，因此沿梯度的反方向移动可以最快地降低函数值。参数更新公式为：θ ← θ - η∇L(θ)，其中η是学习率，∇L(θ)是损失函数的梯度。

2. **与[[反向传播]]的关系**：[[反向传播]]负责[[计算]]梯度（∂L/∂W），梯度下降负责使用梯度更新参数。两者配合完成一次训练迭代：前向传播 → [[计算]]损失 → [[反向传播]]求梯度 → 梯度下降更新权重。

3. **变体家族**：基础梯度下降使用全量数据[[计算]]梯度（Batch GD），[[计算]]成本高。[[随机梯度下降（SGD）]]每次用一个样本，[[Momentum（动量）]]引入惯性加速收敛，[[Adam（自适应矩估计）]]结合动量和自适应学习率，[[RMSProp]]自适应调整每参数学习率。这些变体构成了现代深度学习优化的工具链。

4. **在[[反向传播]]中的作用**：在1986年[[Learning Representations by Back-propagating Errors (1986 论文)]]中，梯度下降与[[反向传播]]结合使用，实现了多层神经网络的有效训练。论文展示了如何通过这种组合解决[[XOR问题]]等经典难题。

## 来源
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — 在反向传播论文中使用
- [[raw/articles/ai-papers/foundations/paper_02_backpropagation.md]] — 源文件
- [Stochastic Gradient Descent - a theoretical overview (Robbins & Monro, 1951)] — 理论基础

## 相关
- [[反向传播（Backpropagation）]] — complement_algorithm
- [[随机梯度下降（SGD）]] — variant_of
- [[Learning Representations by Back-propagating Errors (1986 论文)]] — used_with
- [[链式法则]] — works_with
- [[损失函数]] — optimizes
- [[学习率]] — uses_parameter
