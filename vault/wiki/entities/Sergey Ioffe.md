---
type: entity
status: active
confidence: 0.90
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [person, deep-learning, normalization, google, 机器学习]
aliases: [Sergey Ioffe]
relates_to:
  - target: Batch Normalization
    relation: contributed_to
  - target: Christian Szegedy
    relation: collaborates_with
  - target: Google
    relation: part_of
  - target: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift (2015 论文)"
    relation: authored_by
supersedes: null
---

# Sergey Ioffe

## 概述
深度学习研究者，[[Google]] 研究员，与 [[Christian Szegedy]] 共同提出 [[Batch Normalization]]，彻底改变了深度神经网络的训练方式。

## 关键内容

1. **[[Batch Normalization]] 论文（2015）**：与 [[Christian Szegedy]] 共同发表《[[Batch Normalization]]: Accelerating Deep Network Training by Reducing [[内部协变量偏移|Internal Covariate Shift]]》，提出在每一层输出上做归一化以解决[[内部协变量偏移]]问题，使训练速度提升 14 倍。
2. **[[内部协变量偏移]]概念**：首次提出"[[内部协变量偏移|Internal Covariate Shift]]"概念——神经网络训练过程中，随着前面层权重更新，每一层看到的输入分布不断变化，导致后面层需要不断适应新分布。
3. **可学习归一化参数**：在归一化公式中引入可学习的缩放参数 γ 和平移参数 β，让网络自行决定每一层需要的分布形态，保留了网络的表达能力。

4. **训练/推理双模式设计**：BN 在训练时使用当前 batch 统计量（引入正则化噪声），推理时使用训练过程中累积的滑动平均统计量（running_mean, running_var），这一设计成为后续所有归一化方法的标准[[规范化理论|范式]]。

5. **实验验证**：在 MNIST 上实现 14 倍训练加速，在 [[ImageNet]] 上 BN-[[Inception Network|Inception]] [[Top-5 错误率]]降至 4.82%，超越当时人类表现（5.1%）。

## 来源
- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化

## 相关
- [[Batch Normalization]] — contributed_to
- [[Christian Szegedy]] — collaborates_with
- [[Google]] — part_of
