---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["论文", "深度学习", "计算机视觉", "卷积神经网络"]
aliases: ["ImageNet Classification with Deep Convolutional Neural Networks", "AlexNet 论文", "Krizhevsky et al. 2012"]
relates_to: ["AlexNet", "Alex Krizhevsky", "Ilya Sutskever", "Geoffrey E. Hinton", "ImageNet", "NeurIPS"]
supersedes: null
---

# ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)

## 概述 (50-200字符)
2012 年 NeurIPS 发表的里程碑论文，介绍了 [[AlexNet]] 架构，在 [[ImageNet]] 竞赛中将 Top-5 错误率从 25.8% 降至 15.3%，开启了深度学习革命。

## 关键内容 (≥300字符, 用[[双链]])
1. **论文信息**：作者 [[Alex Krizhevsky]]、[[Ilya Sutskever]]、[[Geoffrey E. Hinton]]（多伦多大学），发表于 NeurIPS 2012（第 25 届）。论文提出了一个 8 层深度[[卷积神经网络（CNN）]]——[[AlexNet]]，在 [[ImageNet|ImageNet 大规模视觉识别挑战赛]]（[[ImageNet|ILSVRC]]）中取得突破性成绩。
2. **核心贡献**：(1) 证明了深度 CNN 在大规模视觉任务中的有效性；(2) 系统引入[[ReLU激活函数]]（训练速度快 6 倍）；(3) 使用双 GPU 并行训练（GTX 580，训练 5-6 天）；(4) 提出[[Dropout]]正则化（p=0.5，显著降低[[过拟合（Overfitting）|过拟合]]）；(5) 设计[[数据增强（Data Augmentation）]]策略（随机裁剪、翻转、PCA 色彩扰动）；(6) 使用[[局部响应归一化（LRN）]]提升泛化。
3. **实验结果**：Top-5 错误率 15.3%（2011 年冠军为 25.8%），领先第二名 10 个百分点。这是计算机视觉历史上最大的单年进步幅度，证明了数据驱动的深度学习远优于手工特征工程（SIFT/HOG + SVM）的传统[[规范化理论|范式]]。
4. **影响与引用**：该论文是深度学习领域被引用最多的论文之一（超过 10 万次引用），直接推动了 AI 产业投资浪潮。它标志着从"[[AI 寒冬]]"到"深度学习时代"的转折点，后续几乎所有视觉突破（VGGNet、[[残差网络（ResNet）|ResNet]]、ViT 等）都建立在此论文奠定的[[规范化理论|范式]]之上。

## 来源
- [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). ImageNet classification with deep convolutional neural networks. NeurIPS, 25.] — 原始论文
- [raw/articles/ai-papers/machine-learning/07_alexnet_2012.md] — 源文件

## 相关
- [[AlexNet]] — describes
- [[Alex Krizhevsky]] — authored_by
- [[Ilya Sutskever]] — authored_by
- [[Geoffrey E. Hinton]] — authored_by
- [[ImageNet]] — evaluated_on
- [[卷积神经网络（CNN）]] — implements
- [[LeNet-5]] — extends
- [[Gradient-Based Learning Applied to Document Recognition (1998 论文)]] — extends
