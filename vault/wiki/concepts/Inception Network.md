---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["computer vision", "convolutional neural networks", architecture, 机器学习]
aliases: ["GoogLeNet", "Inception Network", "Inception", "Inception-v1"]
relates_to:
  - target: "[[Going Deeper with Convolutions (2014 论文)]]"
    type: described_in
  - target: "[[Christian Szegedy]]"
    type: created_by
  - target: "[[Google]]"
    type: developed_by
  - target: "[[Convolutional Neural Networks]]"
    type: instance_of
  - target: "[[Multi-Scale Feature Extraction]]"
    type: implements
  - target: "[[1x1 Convolution]]"
    type: uses
supersedes: null
---

# Inception Network

## 概述
Inception网络（又称Goog[[卷积神经网络（CNN）|LeNet]]）是一种创新的[[卷积神经网络（CNN）|卷积神经网络]]架构，通过Inception模块实现了高效的多尺度特征提取。

## 关键内容

1. **Inception模块**：Inception模块同时使用不同尺寸的卷积核（1×1, 3×3, 5×5）和池化操作，在同一层级捕获不同[[感受野]]的特征，然后将输出在通道维度拼接。

2. **[[计算]]效率**：通过大量使用1×1卷积进行降维和升维，有效减少了参数量和[[计算]]复杂度，使得网络可以在保持性能的同时加深层数。

3. **深度设计**：Goog[[卷积神经网络（CNN）|LeNet]]达到了22层深度（包含池化层），展示了通过模块化设计实现深度网络的可能性，对后续的CNN架构产生了深远影响。

## 来源
- [[ai_papers_timeline.md]] — 2014年Inception提出
- [[Going Deeper with Convolutions (2014 论文)]] — Christian Szegedy等人在Google的工作

## 相关
- [[Going Deeper with Convolutions (2014 论文)]] — described_in
- [[Christian Szegedy]] — created_by
- [[Google]] — developed_by
- [[Convolutional Neural Networks]] — instance_of
- [[Multi-Scale Feature Extraction]] — implements
- [[1x1 Convolution]] — uses