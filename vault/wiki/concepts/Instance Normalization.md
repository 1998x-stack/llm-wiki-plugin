---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 归一化, 风格迁移, CNN, 机器学习]
aliases: [实例归一化, InstanceNorm, IN]
relates_to:
  - target: Batch Normalization
    relation: compares_to
  - target: Layer Normalization
    relation: compares_to
  - target: Group Normalization
    relation: compares_to
supersedes: null
---

# Instance Normalization

## 概述
对单个样本的单个通道内的空间维度（H, W）做归一化，每个样本每个通道独立[[计算]]统计量，不依赖 batch 维度，主要用于风格迁移任务。

## 关键内容

1. **归一化维度**：在 N×C×H×W 的张量中，Instance Norm 沿 H 和 W 方向归一化，即对每个样本的每个通道独立[[计算]]均值和方差。与 [[Batch Normalization]] 沿 N 方向、[[Layer Normalization]] 沿 C×H×W 方向不同。

2. **为什么适合风格迁移**：风格迁移任务中，每张图像的对比度和亮度差异很大，batch 统计会混合不同图像的风格信息。Instance Norm 对每张图独立归一化，保留了图像自身的风格特征，避免 batch 内样本间的相互干扰。

3. **不依赖 batch size**：与 Batch Norm 不同，Instance Norm 完全不需要 batch 维度，batch size = 1 时也能正常工作，适合在线推理和单样本场景。

4. **公式**：对单个样本 n 的单个通道 c，$\mu_{nc} = \frac{1}{HW}\sum_{h,w} x_{nchw}$，$\sigma_{nc}^2 = \frac{1}{HW}\sum_{h,w}(x_{nchw} - \mu_{nc})^2$，归一化后同样有可学习的 γ 和 β。

## 来源

- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化（归一化变体章节）

## 相关

- [[Batch Normalization]] — compares_to（BN 沿 batch 维度归一化，IN 沿空间维度归一化）
- [[Layer Normalization]] — compares_to（LN 对所有通道归一化，IN 对每个通道独立归一化）
- [[Group Normalization]] — compares_to（GN 是 IN 的泛化，按通道组归一化）
