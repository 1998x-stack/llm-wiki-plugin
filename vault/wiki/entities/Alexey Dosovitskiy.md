---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [person, computer-vision, vision-transformer]
aliases: [Alexey Dosovitskiy]
relates_to:
  - target: Vision Transformer（ViT）
    relation: contributed_to
  - target: Transformer
    relation: applied_to
supersedes: null
---

# Alexey Dosovitskiy

## 概述
[[计算]]机视觉研究者，[[Vision Transformer（ViT）]]的主要作者，将 [[Transformer 架构]]成功应用于图像识别。

## 关键内容

1. **[[An Image is Worth 16x16 Words: Transformers for Image Recognition (2021 论文)|ViT 论文]]（2021）**：发表《An Image is Worth 16x16 Words: [[Transformer]]s for Image Recognition》，首次证明纯 [[Transformer 架构]]（无卷积）可以在图像分类任务上达到 SOTA。
2. **图像分块策略**：将图像分割为 16×16 的 patch 序列，直接输入 [[Transformer]] 编码器，证明了[[自注意力机制]]可以处理视觉数据。
3. **影响**：ViT 开启了视觉 [[Transformer]] 的研究热潮，后续的 Swin [[Transformer]]、DETR 等工作均受其启发。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[Vision Transformer（ViT）]] — contributed_to
- [[Transformer]] — applied_to
