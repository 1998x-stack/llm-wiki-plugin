---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, computer-vision, segmentation]
aliases: [Ronneberger et al. 2015]
relates_to:
  - target: U-Net
    relation: introduced
  - target: 卷积神经网络（CNN）
    relation: applied_to
supersedes: null
---

# U-Net: Convolutional Networks for Biomedical Image Segmentation (2015 论文)

## 概述
提出 [[U-Net]] 架构的论文，专为生物医学图像分割设计，成为语义分割领域的经典架构。

## 关键内容

1. **U 型架构**：编码器（下采样）捕获上下文信息，解码器（上采样）实现精确定位，中间通过[[跳跃连接（Skip Connection）|跳跃连接]]融合多尺度特征。
2. **小样本学习**：设计用于数据稀缺的生物医学场景，通过数据增强和弹性形变实现少量样本下的高精度分割。
3. **广泛影响**：[[U-Net]] 成为医学图像分割的标准架构，其[[跳跃连接（Skip Connection）|跳跃连接]]思想影响了后续的 [[残差连接（Residual Connection）]] 设计。

## 来源
- [[ai_papers_timeline.md]] — 2015 年时间线条目

## 相关
- [[U-Net]] — introduced
- [[残差连接（Residual Connection）]] — relates_to
