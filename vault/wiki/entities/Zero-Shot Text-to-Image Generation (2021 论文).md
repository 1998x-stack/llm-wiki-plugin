---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, generative-models, text-to-image, AI工程]
aliases: [Ramesh et al. 2021, DALL-E 论文]
relates_to:
  - target: Aditya Ramesh
    relation: authored_by
  - target: DALL-E
    relation: introduced
  - target: CLIP
    relation: relates_to
supersedes: null
---

# Zero-Shot Text-to-Image Generation (2021 论文)

## 概述
提出 [[DALL-E]] 文生图模型的论文，首次展示 AI 可以根据自然语言描述生成前所未有的图像。

## 关键内容

1. **离散 VAE + [[Transformer]]**：使用离散 VAE 将图像编码为 token，与文本 token 拼接后训练 [[Transformer]] 生成图像。
2. **组合泛化**：[[DALL-E]] 可以生成训练集中从未出现过的概念组合，如"穿宇航服的骑马"。
3. **AI 艺术开创**：开启了 AI 生成图像的新领域，后续的 [[Stable Diffusion]] 和 [[DALL-E]] 2 均受其启发。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[Aditya Ramesh]] — authored_by
- [[DALL-E]] — introduced
- [[CLIP]] — relates_to
- [[Stable Diffusion]] — compares_to
