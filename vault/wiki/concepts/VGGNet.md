---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [深度学习, 计算机视觉, CNN, 架构, 论文]
aliases: [VGG, VGG-16, VGG-19, Very Deep Convolutional Networks, Very Deep Convolutional Networks for Large-Scale Image Recognition]
relates_to:
  - target: "[[卷积神经网络（CNN）]]"
    type: part_of
    confidence: 0.95
  - target: "[[AlexNet]]"
    type: extends
    confidence: 0.9
  - target: "[[GoogLeNet: Inception]]"
    type: compares_to
    confidence: 0.85
  - target: "[[残差网络（ResNet）]]"
    type: compares_to
    confidence: 0.9
  - target: "[[迁移学习（Transfer Learning）]]"
    type: uses
    confidence: 0.95
  - target: "[[University of Oxford]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[Karen Simonyan]]"
    type: created_by
    confidence: 0.95
  - target: "[[Andrew Zisserman]]"
    type: created_by
    confidence: 0.95
  - target: "[[3×3卷积核]]"
    type: uses
    confidence: 0.95
  - target: "[[感受野]]"
    type: optimizes_for
    confidence: 0.9
  - target: "[[Top-5 错误率]]"
    type: measures_performance
    confidence: 0.9
  - target: "[[ILSVRC]]"
    type: evaluated_on
    confidence: 0.9
supersedes: null
---

# VGGNet

## 概述
VGGNet 是由 [[Karen Simonyan]] 和 [[Andrew Zisserman]] 在 2014 年提出的深度[[卷积神经网络（CNN）|卷积神经网络]]架构，统一使用 3×3 [[3×3卷积核|小卷积核]]验证了网络深度对性能的关键影响。以其极简设计和出色的性能，VGGNet 成为 [[ILSVRC]] 2014 分类亚军和检测冠军，至今仍是[[迁移学习]]中最常用的骨干网络之一。

## 关键内容

1. **核心设计思想**：只使用 3×3 卷积核，通过不断叠加来增加网络深度。两个 3×3 卷积的[[感受野]]等同于一个 5×5 卷积，三个 3×3 等同于一个 7×7 卷积，但参数量更少（27C² vs 49C²），且增加了两次非线性激活，效果更佳。

2. **VGG 家族架构**：系统测试了 A-E 六种深度[[Configuration|配置]]，其中 VGG-16（13卷积+3全连接层，共16层，138M参数）和 VGG-19（16卷积+3全连接层，共19层，144M参数）最为经典。深度提升性能，但边际效应递减（19层比16层仅提升0.1%）。

3. **竞赛表现**：在 [[ILSVRC]] 2014 中，VGG-16 单模型取得了 7.32% 的 [[Top-5 错误率]]，仅次于 [[Inception Network|GoogLeNet]] 的 6.67%，获得分类亚军；在目标检测任务中获得冠军。

4. **参数效率问题**：VGGNet 最大的问题是全连接层参数量巨大（占总参数的 89.4%，约 123.6M 参数），相比之下 [[Inception Network|GoogLeNet]] 采用全局平均池化（GAP）替代全连接层，参数量仅 6.8M，是 VGGNet 的 1/20。

5. **[[迁移学习]]基石**：由于其结构简单、特征质量高且各层特征可解释（浅层检测边缘特征，深层捕获语义特征），VGGNet 成为[[迁移学习]]最广泛使用的预训练模型，为各类下游视觉任务提供了高质量的特征提取能力。

## 来源
- [[Very Deep Convolutional Networks for Large-Scale Image Recognition (2014 论文)]] — 原始论文
- [[ai_papers_timeline.md]] — 2014 年时间线条目
- [[raw/articles/ai-papers/foundations/paper_11_vggnet.md]] — 全文精读

## 相关
- [[卷积神经网络（CNN）]] — part_of
- [[AlexNet]] — extends
- [[GoogLeNet: Inception]] — compares_to
- [[残差网络（ResNet）]] — compares_to
- [[迁移学习（Transfer Learning）]] — uses
- [[University of Oxford]] — affiliated_with
- [[Karen Simonyan]] — created_by
- [[Andrew Zisserman]] — created_by
- [[Top-5 错误率]] — measures_performance
- [[ILSVRC]] — evaluated_on
