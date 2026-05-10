---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [person, computer-vision, multimodal]
aliases: [Aditya Ramesh]
relates_to:
  - target: OpenAI
    relation: affiliated_with
  - target: DALL-E
    relation: contributed_to
supersedes: null
---

# Aditya Ramesh

## 概述
[[OpenAI]] 研究员，[[DALL-E]] 文生图模型的主要作者，开创了 AI 生成图像的新领域。

## 关键内容

1. **[[DALL-E]] 论文（2021）**：发表《Zero-Shot Text-to-Image Generation》，提出将文本和图像统一为 token 序列，通过 [[Transformer]] 生成图像。
2. **文生图[[规范化理论|范式]]**：[[DALL-E]] 首次展示了 AI 可以根据自然语言描述生成前所未有的图像组合，开创了 AI 艺术创作的新领域。
3. **技术路线**：使用离散 VAE 将图像编码为 token，与文本 token 拼接后训练 [[Transformer]]，为后续的 [[Stable Diffusion]] 和 [[DALL-E]] 2 奠定基础。

## 来源
- [[ai_papers_timeline.md]] — 2021 年时间线条目

## 相关
- [[OpenAI]] — affiliated_with
- [[DALL-E]] — contributed_to
- [[Stable Diffusion]] — compares_to
