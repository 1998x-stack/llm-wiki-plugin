---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "计算机视觉", "数据集", "深度学习"]
aliases: ["ImageNet", "ILSVRC", "ImageNet Large Scale Visual Recognition Challenge", "ImageNet 大规模视觉识别挑战赛"]
relates_to: ["AlexNet", "卷积神经网络（CNN）", "深度学习"]
supersedes: null
---

# ImageNet

## 概述 (50-200字符)
ImageNet 是包含 120 万张、1000 个类别的大规模图像分类数据集，其年度挑战赛（[[ILSVRC]]）是[[计算]]机视觉最权威竞赛，2012 年 [[AlexNet]] 的突破性表现标志着深度学习时代的开启。

## 关键内容 (≥300字符, 用[[双链]])
1. **规模与结构**：ImageNet 包含超过 1400 万张手工[[标注]]图像，覆盖 2 万多个类别。[[ILSVRC]]（ImageNet Large Scale Visual Recognition Challenge）使用其中 120 万张训练图像、1000 个类别作为标准分类任务，是衡量视觉模型能力的黄金基准。
2. **[[ILSVRC]] 历史转折**：2010-2011 年冠军采用传统方法（[[特征工程（Feature Engineering）|手工特征]]如 SIFT/HOG + [[支持向量机]]），[[Top-5 错误率]]约 25-26%。2012 年[[AlexNet]]以 15.3% 的 [[Top-5 错误率]]夺冠，领先第二名 10 个百分点，这是跨越式突破。此后错误率持续下降：2014 年 Goog[[卷积神经网络（CNN）|LeNet]] 6.7%，2015 年 [[残差网络（ResNet）|ResNet]] 3.57%，2017 年达到 2.25%（超越人类水平）。
3. **对 AI 产业的推动**：[[ILSVRC|ImageNet 竞赛]]为深度学习提供了大规模标准化评测平台，证明了数据驱动方法优于[[手工特征工程]]。竞赛结果直接推动了 [[NVIDIA]] GPU 需求爆发、[[Google]] Brain/[[DeepMind]] 扩张、以及自动驾驶、医疗影像、人脸识别等商业应用的兴起。
4. **后续影响**：ImageNet 预训练模型成为[[迁移学习]]的标准起点，"ImageNet moment"成为 AI 领域突破性进展的代名词。竞赛于 2017 年停办（因模型性能已超越人类），但其影响力延续至今——现代视觉模型（ViT、ConvNeXt 等）仍以 ImageNet 作为核心基准。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — 原始论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件

## 相关
- [[AlexNet]] — evaluated_on
- [[卷积神经网络（CNN）]] — benchmark_for
- [[深度学习]] — catalyzed
- [[支持向量机]] — competed_with
- [[LeNet-5]] — benchmark_successor
