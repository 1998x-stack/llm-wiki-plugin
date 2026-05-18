---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, computer-vision, vision-transformer, 机器学习]
aliases: [Dosovitskiy et al. 2021, ViT 论文]
relates_to:
  - target: Alexey Dosovitskiy
    relation: authored_by
  - target: Vision Transformer（ViT）
    relation: introduced
  - target: Transformer
    relation: applied
supersedes: null
---

# An Image is Worth 16x16 Words: Transformers for Image Recognition (2021 论文)

## 概述
提出 [[Vision Transformer（ViT）]]的论文，首次证明纯 [[Transformer 架构]]可以在图像分类上达到 SOTA。

## 关键内容

1. **图像分块**：将图像分割为 16×16 的 patch 序列，线性嵌入后输入 [[Transformer]] 编码器。
2. **无卷积设计**：完全依赖[[自注意力机制]]捕获全局依赖，不依赖 [[卷积神经网络（CNN）]] 的局部归纳偏置。
3. **大数据需求**：ViT 需要大规模预训练数据才能超越 CNN，证明了数据规模对 [[Transformer]] 视觉应用的关键性。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[Alexey Dosovitskiy]] — authored_by
- [[Vision Transformer（ViT）]] — introduced
- [[Transformer]] — applied
- [[卷积神经网络（CNN）]] — compares_to
