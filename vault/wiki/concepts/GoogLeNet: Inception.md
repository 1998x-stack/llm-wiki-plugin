---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [computer-vision, CNN, architecture, inception, 机器学习]
aliases: [GoogLeNet, Inception, Inception 模块]
relates_to:
  - target: Christian Szegedy
    relation: relates_to
  - target: 卷积神经网络（CNN）
    relation: part_of
  - target: VGGNet
    relation: compares_to
supersedes: null
---

# GoogLeNet / Inception

## 概述
使用 [[Inception Network|Inception]] 模块的深度[[卷积神经网络（CNN）|卷积神经网络]]，通过多尺度卷积核并行处理实现高效特征提取。

## 关键内容

1. **[[Inception Network|Inception]] 模块**：在同一层并行使用 1×1、3×3、5×5 卷积核和池化，捕获多尺度特征。
2. **1×1 卷积降维**：使用 1×1 卷积减少通道数，大幅降低[[计算]]量。
3. **[[ImageNet]] 冠军**：[[Inception Network|GoogLeNet]] 以 22 层深度赢得 2014 年 [[ImageNet]] 挑战赛，参数量远少于 [[VGGNet]]。

## 来源
- [[ai_papers_timeline.md]] — 2014 年时间线条目

## 相关
- [[Christian Szegedy]] — relates_to
- [[卷积神经网络（CNN）]] — part_of
- [[VGGNet]] — compares_to
