---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, computer-vision, CNN, inception]
aliases: [Szegedy et al. 2014, GoogLeNet 论文]
relates_to:
  - target: Christian Szegedy
    relation: authored_by
  - target: GoogLeNet / Inception
    relation: introduced
supersedes: null
---

# Going Deeper with Convolutions (2014 论文)

## 概述
提出 [[Inception Network|GoogLeNet]]/[[Inception Network|Inception]] 架构的论文，通过多尺度卷积核并行处理实现高效的特征提取。

## 关键内容

1. **[[GoogLeNet: Inception|Inception 模块]]**：在同一层并行使用 1×1、3×3、5×5 卷积核和池化，捕获多尺度特征。
2. **1×1 卷积降维**：使用 1×1 卷积减少通道数，大幅降低[[计算]]量，使深层网络训练可行。
3. **[[ImageNet]] 冠军**：[[Inception Network|GoogLeNet]] 以仅 22 层深度赢得 2014 年 [[ImageNet]] 挑战赛，参数量远少于 [[VGGNet]]。

## 来源
- [[ai_papers_timeline.md]] — 2014 年时间线条目

## 相关
- [[Christian Szegedy]] — authored_by
- [[GoogLeNet / Inception]] — introduced
- [[VGGNet]] — compares_to
