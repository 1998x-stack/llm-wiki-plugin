---
type: project
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [项目, 深度学习, 计算机视觉, CNN, 机器学习]
aliases: ["ZFNet", "Zeiler-Fergus Net", "Zeiler and Fergus Network"]
relates_to: ["AlexNet", "VGGNet", "GoogLeNet: Inception", "残差网络（ResNet）", "卷积神经网络（CNN）"]
supersedes: null
---

# ZFNet

## 概述
ZFNet（Zeiler & Fergus Net）是 2013 年 [[ILSVRC]] 冠军网络，通过可视化并微调 [[AlexNet]] 架构取得进一步改进，是 [[AlexNet]] 的直接后继者。

## 关键内容

1. **与 [[AlexNet]] 的关系**：ZFNet 由 Matthew Zeiler 和 Rob Fergus 提出，本质上是 [[AlexNet]] 的改进版。通过可视化技术（反卷积网络）分析 [[AlexNet]] 各层学到的特征，发现第一层卷积核过大（11×11）导致信息丢失，将其缩小为 7×7，并调整中间层通道数。
2. **2013 年 [[ILSVRC]] 冠军**：ZFNet 在 2013 年竞赛中夺冠，[[Top-5 错误率]]进一步从 [[AlexNet]] 的 16.4% 降至约 11.2%。这证明了 [[AlexNet]] 架构的可改进性和深度学习方向的持续潜力。
3. **可视化贡献**：ZFNet 最重要的贡献不是架构本身，而是其可视化方法——通过反卷积（deconvolution）将卷积层激活映射回像素空间，直观展示网络各层学到的特征。这增强了深度学习模型的可解释性。
4. **演化路径**：[[AlexNet]]（2012）→ ZFNet（2013）→ [[VGGNet]]（2014，全 3×3 卷积）→ [[GoogLeNet: Inception]]（2014，[[GoogLeNet: Inception|Inception 模块]]）→ [[残差网络（ResNet）]]（2015，[[残差连接]]）。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — extends
- [[VGGNet]] — precedes
- [[GoogLeNet: Inception]] — precedes
- [[残差网络（ResNet）]] — precedes
- [[卷积神经网络（CNN）]] — implements
- [[ILSVRC]] — won_2013
