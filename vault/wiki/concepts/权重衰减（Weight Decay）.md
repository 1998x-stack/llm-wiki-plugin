---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 优化, 正则化, 训练技巧, 机器学习]
aliases: ["Weight Decay", "权重衰减", "L2 正则化"]
relates_to: ["过拟合（Overfitting）", "随机梯度下降（SGD）", "AlexNet", "Adam（自适应矩估计）", "深度学习（Deep Learning）"]
supersedes: null
---

# 权重衰减（Weight Decay）

## 概述
权重衰减是一种 L2 正则化技术，通过在损失函数中添加权重的平方和惩罚项，限制模型复杂度，防止[[过拟合（Overfitting）|过拟合]]。[[AlexNet]] 使用 0.0005 的权重衰减系数。

## 关键内容

1. **数学原理**：权重衰减在原始损失 L 上添加 L2 惩罚项：L_total = L + (λ/2)·Σw²。梯度更新时，这等价于每次更新后将权重乘以 (1 - λ)，即"衰减"权重。[[AlexNet]] 使用 λ = 0.0005。
2. **在 [[AlexNet]] 中的应用**：[[AlexNet]] 有约 6000 万参数，极易[[过拟合（Overfitting）|过拟合]]。权重衰减与 [[Dropout（随机失活）]]、[[数据增强（Data Augmentation）]] 共同构成其正则化策略。训练使用 [[随机梯度下降（SGD）]] + [[Momentum（动量）]]（0.9）+ 权重衰减（0.0005）。
3. **为什么有效**：权重衰减倾向于让权重趋向较小的值，这等价于偏好"更平滑"的函数，降低了模型的有效容量。小权重对输入扰动的敏感度更低，提升了泛化能力。
4. **与 Adam 的关系**：标准 [[Adam（自适应矩估计）]] 优化器中的 L2 正则化并不等价于权重衰减（因为自适应学习率的缩放效应）。[[AdamW]] 修正了这一问题，使权重衰减在自适应优化器中正确生效。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[过拟合（Overfitting）]] — prevents
- [[随机梯度下降（SGD）]] — used_with
- [[AlexNet]] — used_in
- [[Dropout（随机失活）]] — complementary_to
- [[数据增强（Data Augmentation）]] — complementary_to
- [[AdamW]] — corrected_in
