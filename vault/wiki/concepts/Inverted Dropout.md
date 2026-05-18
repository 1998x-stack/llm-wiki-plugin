---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [Dropout, 正则化, 推理优化, 不确定性估计, 机器学习]
aliases: [Inverted Dropout, 反向 Dropout]
relates_to: [Dropout（随机失活）, Inverted Dropout, MC Dropout, 过拟合（Overfitting）]
supersedes: null
---

# Inverted Dropout

## 概述
[[Dropout]] 的现代实现方式，训练时缩放激活值，推理时不做任何操作，避免额外[[计算]]开销。

## 关键内容

1. **训练时缩放**：在训练阶段，随机将部分神经元置零后，将剩余激活值除以保留概率 p（即乘以 1/p），使得激活值的期望保持不变。
2. **推理时无操作**：由于训练时已经进行了缩放补偿，推理（测试）阶段可以直接使用所有神经元，无需乘以 p。这与原始 [[Dropout]] 的推理方式相反。
3. **实现优势**：Inverted [[Dropout]] 是主流框架（[[PyTorch]]、[[TensorFlow]]）的默认实现。它将额外的[[计算]]开销放在训练时（可容忍），而推理时零开销，这对部署场景至关重要。

原始 [[Dropout]] 在推理时需要乘以 p，而 Inverted [[Dropout]] 将缩放操作前置到训练阶段，是工程上更优的设计。

## 来源
- [[Dropout: A Simple Way to Prevent Neural Networks from Overfitting (2014 论文)]] — 原始提出
- [[Nitish Srivastava]] — 作者

## 相关
- [[Dropout（随机失活）]] — variant_of
- [[MC Dropout]] — compares_to
- [[过拟合（Overfitting）]] — solves
