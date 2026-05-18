---
type: project
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [计算机视觉, 数据集, 图像分类, AI工程]
aliases: ["CIFAR-10", "Canadian Institute For Advanced Research 10", "CIFAR10"]
relates_to: ["残差网络（ResNet）", "卷积神经网络（CNN）", "ILSVRC"]
supersedes: null
---

# CIFAR-10 数据集

## 概述
包含10个类别共6万张32×32彩色图像的基准图像分类数据集，广泛用于评估和比较图像分类模型的性能。

## 关键内容
1. **数据结构**：CIFAR-10 包含60,000张32×32的彩色图像，分为10个类别（飞机、汽车、鸟、猫、鹿、狗、蛙、马、船、卡车），每类6,000张。其中50,000张用于训练，10,000张用于测试。
2. **在 [[残差网络（ResNet）|ResNet]] 研究中的角色**：[[残差网络（ResNet）]]的原始论文使用 CIFAR-10 进行了关键的[[Ablation Study|消融实验]]。在 CIFAR-10 上，Plain Network（无残差）在56层以上开始退化，而 [[残差网络（ResNet）|ResNet]]（有残差）即使到1202层依然能有效训练，这是证明[[残差连接（Residual Connection）]]有效性的最直接证据。
3. **CIFAR-10 vs [[ILSVRC]]**：CIFAR-10 图像分辨率低（32×32）、类别少（10类），适合快速原型验证和[[算法]]比较；[[ILSVRC]]/[[ImageNet]] 分辨率高（224×224+）、类别多（1000类），适合评估模型的最终性能。两者互补使用是研究的标准做法。
4. **CIFAR-100 扩展**：CIFAR-100 是同一数据集的100类别版本，每类600张图像，提供了更具挑战性的分类任务。[[Deep Residual Learning for Image Recognition (2016 论文)|ResNet 论文]]也在 CIFAR-100 上验证了结果。
5. **历史意义**：CIFAR-10 由 [[Alex Krizhevsky]]、Vinod Nair 和 [[Geoffrey E. Hinton|Geoffrey Hinton]] 收集，是深度学习时代最具影响力的基准数据集之一。几乎所有图像分类新架构都会在 CIFAR-10 上报告结果。

## 来源
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — 实验部分，CIFAR-10 上的退化现象验证与残差连接对比实验

## 相关
- [[残差网络（ResNet）]] — compares_to（关键验证数据集）
- [[ILSVRC]] — compares_to（互补基准）
- [[卷积神经网络（CNN）]] — uses
- [[退化问题（Degradation Problem）]] — compares_to（在 CIFAR-10 上首次验证）
