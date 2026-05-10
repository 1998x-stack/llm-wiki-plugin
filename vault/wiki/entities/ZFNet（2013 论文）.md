---
type: entity
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["论文", "计算机视觉", "深度学习", "CNN"]
aliases: ["ZFNet", "Zeiler Fergus Network", "Visualizing and Understanding Convolutional Networks (2013 论文)"]
relates_to: ["AlexNet", "ImageNet Classification with Deep Convolutional Neural Networks (2012 论文)", "卷积神经网络（CNN）", "计算机视觉", "卷积核可视化", "ILSVRC（ImageNet大规模视觉识别挑战赛）"]
supersedes: null
---

# ZFNet（2013 论文）

## 概述
[[ZFNet]] 是 Matthew Zeiler 和 Rob Fergus 于 2013 年提出的卷积网络，通过可视化分析 [[AlexNet]] 各层特征并优化架构，获得 [[ILSVRC]] 2013 冠军。

## 关键内容

1. **[[AlexNet]] 的可视化与改进**：[[ZFNet]] 使用反卷积（deconvolution）技术可视化了 [[AlexNet]] 各卷积层学到的特征，揭示了第一层学习边缘和颜色检测器、深层学习抽象物体部件的层次化特征表示。基于可视化分析，[[ZFNet]] 调整了 [[AlexNet]] 的卷积核尺寸和步长。
2. **[[ILSVRC]] 2013 冠军**：改进后的架构在 2013 年 [[ILSVRC]] 竞赛中夺冠，将 [[Top-5 错误率]]从 [[AlexNet]] 的 16.4% 进一步降至 11.7%。
3. **历史地位**：[[ZFNet]] 是 [[AlexNet]] 的直接后续工作，证明了[[卷积核可视化]]对于理解网络内部表征的价值。它开启了 CNN 可解释性研究的先河，为后续的网络架构设计（[[VGGNet]]、[[Inception Network|GoogLeNet]]、[[残差网络（ResNet）|ResNet]]）提供了重要洞察。
4. **论文全称**：该论文正式标题为 "Visualizing and Understanding Convolutional Networks"，强调了对卷积网络内部工作机制的理解和可视化分析。

## 来源
- [raw/articles/ai-papers/ai-papers/foundations/paper_03_alexnet.md] — 源文件中提及
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — extends
- [[卷积核可视化]] — pioneered
- [[卷积神经网络（CNN）]] — implements
- [[计算机视觉]] — research_field
- [[VGGNet]] — preceded
- [[ILSVRC（ImageNet大规模视觉识别挑战赛）]] — won_in_2013
