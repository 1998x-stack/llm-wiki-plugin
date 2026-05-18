---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 归一化, 目标检测, CNN, 机器学习]
aliases: [组归一化, GroupNorm, GN]
relates_to:
  - target: Batch Normalization
    relation: compares_to
  - target: Layer Normalization
    relation: compares_to
  - target: Instance Normalization
    relation: extends
supersedes: null
---

# Group Normalization

## 概述
将通道分组后，在每组内的通道和空间维度上做归一化，完全摆脱对 batch size 的依赖，特别适合小 batch size 的目标检测等场景。

## 关键内容

1. **归一化维度**：在 N×C×H×W 的张量中，将 C 个通道分为 G 组，每组包含 C/G 个通道，然后在每组内沿 C/G×H×W 方向归一化。是 [[Instance Normalization]] 的泛化——当 G=C 时退化为 IN，当 G=1 时退化为 [[Layer Normalization]]。

2. **解决小 batch size 问题**：[[Batch Normalization]] 在 batch size 较小时（如目标检测中 batch=1 或 2）方差估计不准确，导致性能下降。Group Norm 完全不依赖 batch 维度，在 batch=1 时也能稳定工作。

3. **适用场景**：目标检测（[[R-CNN 系列|Faster R-CNN]]、Mask [[R-CNN 系列|R-CNN]] 等）、语义分割等需要高分辨率输入、batch size 受限的任务。在这些场景中，Group Norm 可以替代 Batch Norm 获得更稳定的训练效果。

4. **公式**：将通道分为 G 组，对每组 g 内的所有通道和空间位置[[计算]]均值 $\mu_g$ 和方差 $\sigma_g^2$，归一化后同样有可学习的 γ 和 β。

## 来源

- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化（归一化变体章节）

## 相关

- [[Batch Normalization]] — compares_to（BN 依赖大 batch size，GN 对 batch size 无要求）
- [[Layer Normalization]] — compares_to（LN 对所有通道归一化，GN 按组归一化，是更灵活的中间方案）
- [[Instance Normalization]] — extends（GN 是 IN 的泛化，IN 是 GN 在 G=C 时的特例）
