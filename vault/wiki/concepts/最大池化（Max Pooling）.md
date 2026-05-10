---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["深度学习", "CNN", "池化"]
aliases: ["Max Pooling", "最大池化层", "最大下采样"]
relates_to: ["AlexNet", "卷积神经网络（CNN）", "LeNet-5", "空间金字塔"]
supersedes: null
---

# 最大池化（Max Pooling）

## 概述
最大池化是一种下采样操作，在局部区域内取最大值作为输出，用于降低特征图空间分辨率、减少参数量，并引入一定程度的平移不变性。

## 关键内容

1. **操作方式**：最大池化使用一个滑动窗口（如 3×3，stride=2）在特征图上滑动，每个窗口内取最大值作为输出。例如，[[AlexNet]] 在 Conv1 后使用 3×3 窗口、stride=2 的最大池化，将 55×55 的特征图降至 27×27。
2. **作用**：(1) **降维**：减少特征图的空间尺寸，降低后续层的[[计算]]量和参数量；(2) **平移不变性**：最大值操作对小的位置偏移不敏感，使模型对输入图像的微小变化更鲁棒；(3) **扩大[[感受野]]**：池化后后续层的每个神经元能看到更大的输入区域。
3. **在 [[AlexNet]] 中的应用**：[[AlexNet]] 在 Conv1、Conv2、Conv5 之后都使用了最大池化（3×3，stride=2）。这是从 [[LeNet-5]] 继承的设计模式，但 [[AlexNet]] 的池化窗口更大、步长更大。
4. **与其他池化的对比**：平均池化（取区域平均值）在早期 CNN 中使用较多，但最大池化在实践中表现更好。现代架构中，使用 stride>1 的卷积替代池化层也是一种趋势（如 [[残差网络（ResNet）]]）。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — used_in
- [[卷积神经网络（CNN）]] — component_of
- [[LeNet-5]] — inherited_from
- [[残差网络（ResNet）]] — replaced_by_stride_conv
