---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [computer-vision, vision-transformer, 机器学习]
aliases: [ViT, Vision Transformer]
relates_to:
  - target: Alexey Dosovitskiy
    relation: relates_to
  - target: Transformer
    relation: uses
  - target: 卷积神经网络（CNN）
    relation: compares_to
supersedes: null
---

# Vision Transformer（ViT）

## 概述
将 [[Transformer 架构]]直接应用于图像识别的模型，证明纯[[自注意力机制]]可以处理视觉数据。

## 关键内容

1. **图像分块**：将图像分割为 16×16 的 patch 序列，线性嵌入后输入 [[Transformer]] 编码器。
2. **无卷积设计**：完全依赖[[Self-Attention机制|自注意力]]捕获全局依赖，不依赖 [[卷积神经网络（CNN）]] 的局部归纳偏置。
3. **大数据需求**：ViT 需要大规模预训练数据才能超越 CNN，证明了数据规模对 [[Transformer]] 视觉应用的关键性。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[Alexey Dosovitskiy]] — relates_to
- [[Transformer]] — uses
- [[卷积神经网络（CNN）]] — compares_to
