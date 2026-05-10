---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["机器学习", "深度学习", "计算机视觉", "数据预处理"]
aliases: ["Data Augmentation", "数据扩充", "数据增广"]
relates_to: ["AlexNet", "过拟合", "深度学习", "计算机视觉"]
supersedes: null
---

# 数据增强（Data Augmentation）

## 概述 (50-200字符)
数据增强通过对训练样本施加随机变换（裁剪、翻转、色彩扰动等）人工扩展数据集，增加模型泛化能力。[[AlexNet]] 将 120 万 [[ImageNet]] 样本等效扩展至数十亿。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心思想**：在训练过程中对输入数据施加随机但合理的变换，使模型看到"新"样本，从而学习到对变换不变的特征表示。这本质上是一种正则化技术——通过增加训练数据的多样性来减少[[过拟合]]。
2. **[[AlexNet]] 的增强策略**：(1) **随机裁剪**：从 256×256 原图中随机提取 224×224 区域，每个训练样本可产生多个不同裁剪，等效扩展 2048 倍；(2) **随机水平翻转**：左右镜像翻转，扩展 2 倍；(3) **PCA 色彩扰动**：对 RGB 通道施加基于主成分分析的随机偏移，改变图像亮度和对比度而不改变语义内容。三者组合将 120 万样本等效扩展至数十亿。
3. **为什么有效**：数据增强迫使模型学习语义不变性——猫无论出现在图像左侧还是右侧、无论亮一些还是暗一些，都应该被识别为猫。这比单纯增加参数量或训练轮数更有效地提升泛化性能。
4. **现代演进**：从 [[AlexNet]] 的几何+色彩增强，发展到 AutoAugment（自动搜索增强策略）、RandAugment（简化搜索空间）、MixUp/CutMix（样本间混合）、以及针对特定任务的领域特定增强（如医学影像的弹性形变）。数据增强已成为[[深度学习]]标准训练流程的必备组件。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — AlexNet 论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — used_in
- [[过拟合]] — prevents
- [[深度学习]] — standard_technique
- [[计算机视觉]] — widely_used_in
- [[Dropout]] — complementary_to
