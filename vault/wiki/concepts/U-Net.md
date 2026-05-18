---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [computer-vision, segmentation, architecture, 机器学习]
aliases: [U-Net, U 型网络]
relates_to:
  - target: 卷积神经网络（CNN）
    relation: part_of
  - target: 残差连接（Residual Connection）
    relation: relates_to
supersedes: null
---

# U-Net

## 概述
专为图像分割设计的 U 型[[卷积神经网络（CNN）|卷积神经网络]]，通过[[跳跃连接（Skip Connection）|跳跃连接]]融合多尺度特征。

## 关键内容

1. **U 型架构**：编码器（下采样）捕获上下文，解码器（上采样）实现精确定位。
2. **[[跳跃连接（Skip Connection）|跳跃连接]]**：将编码器的特征图直接与解码器对应层拼接，保留空间细节。
3. **应用领域**：最初用于生物医学图像分割，后扩展到通用语义分割任务。

## 来源
- [[ai_papers_timeline.md]] — 2015 年时间线条目

## 相关
- [[卷积神经网络（CNN）]] — part_of
- [[残差连接（Residual Connection）]] — relates_to
