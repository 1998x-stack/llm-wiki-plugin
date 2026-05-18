---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [神经网络, 深度学习, 梯度优化, LSTM, 机器学习]
aliases: ["Constant Error Carousel", "CEC", "常误差流", "恒定误差轮播"]
relates_to:
  - target: "[[LSTM]]"
    type: implemented_in
    confidence: 0.95
  - target: "[[梯度消失]]"
    type: solves
    confidence: 0.95
  - target: "[[梯度爆炸]]"
    type: solves
    confidence: 0.95
  - target: "[[Sepp Hochreiter]]"
    type: invented_by
    confidence: 0.9
  - target: "[[Jurgen Schmidhuber]]"
    type: invented_by
    confidence: 0.9
  - target: "[[记忆细胞]]"
    type: core_component_of
    confidence: 0.95
supersedes: null
---

# 常误差流（Constant Error Carousel）

## 概述
常误差流（Constant Error Carousel, CEC）是 LSTM 架构中的核心技术机制，通过自连接权重恒为 1 的设计，确保误差信号在[[反向传播]]时不被缩放，从而从根本上解决[[梯度消失]]和[[梯度爆炸|梯度爆炸问题]]。

## 关键内容
1. **核心机制**：
   - [[记忆细胞]]内部的状态更新采用自连接权重为 1 的设计
   - 误差信号在[[记忆细胞]]中通过加法路径传递，而不是通过乘法
   - 确保梯度在长[[Time Series Analysis|时间序列]]中能够保持恒定不变地流动

2. **解决梯度问题**：
   - 通过自连接权重恒为 1，误差信号在[[反向传播]]时不会被缩放
   - 避免了传统 RNN 中梯度随时间步呈指数级衰减或膨胀的问题
   - 使网络能够学习跨越数百甚至数千个时间步的长期依赖关系

3. **数学原理**：
   - 误差在[[记忆细胞]]中的传递为加法形式而非乘法形式
   - [[记忆细胞]]状态的梯度 ∂Cₜ/∂Cₜ₋₁ = fₜ（[[遗忘门]]值），当[[遗忘门]]接近 1 时，梯度无损传递
   - 对比传统 RNN：梯度需要乘以小于 1 的权重[[矩阵]]，导致连乘后指数衰减

4. **历史意义**：
   - 由 Hochreiter 和 Schmidhuber 在 1997 年的 LSTM 论文中首次提出
   - 是第一个从根本上解决 RNN [[梯度消失]]问题的机制
   - 为后续的深度学习序列建模奠定了基础

## 来源
- [[12-hochreiter-1997-lstm.md]] — CEC 概念和机制详解

## 相关
- [[LSTM]] — implemented_in
- [[梯度消失]] — solves
- [[梯度爆炸]] — solves
- [[Sepp Hochreiter]] — invented_by
- [[Jurgen Schmidhuber]] — invented_by
- [[记忆细胞]] — core_component_of