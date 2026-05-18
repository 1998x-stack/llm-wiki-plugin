---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["generative models", multimodal, text-to-image, AI工程]
aliases: ["DALL-E", "DALL·E", "DALL-E 1"]
relates_to:
  - target: "[[Zero-Shot Text-to-Image Generation (2021 论文)]]"
    type: described_in
  - target: "[[Aditya Ramesh]]"
    type: created_by
  - target: "[[OpenAI]]"
    type: developed_at
  - target: "[[CLIP]]"
    type: builds_on
  - target: "[[Variational Autoencoders]]"
    type: uses
  - target: "[[Text-to-Image Synthesis]]"
    type: exemplifies
  - target: "[[GPT-3]]"
    type: conceptually_similar_to
  - target: "[[Stable Diffusion]]"
    type: compares_to
supersedes: null
---

# DALL-E

## 概述
DALL-E是[[OpenAI]]开发的文本到图像生成模型，能够根据文本描述生成多样化的图像内容。

## 关键内容

1. **离散VAE架构**：DALL-E使用离散变分自编码器将图像压缩为离散的潜在表示，然后使用类似GPT的方法根据文本描述生成图像。

2. **文本理解能力**：模型能够理解复杂的文本描述，包括抽象概念、颜色、材质等，并将其转化为对应的视觉元素。

3. **创造性生成**：DALL-E展现了创造新概念的能力，例如"熊猫骑自行车"或"立体派风格的猫"等，显示了模型的创造性潜力。

4. **离散 VAE + [[Transformer]]**：使用离散 VAE 将图像编码为 token，与文本 token 拼接后训练 [[Transformer]] 生成图像。

5. **组合泛化**：可以生成训练集中从未出现过的概念组合，如"穿宇航服的骑马"。

6. **AI 艺术开创**：开启了 AI 生成图像的新领域，后续的 [[Stable Diffusion]] 和 DALL-E 2 均受其启发。

## 来源
- [[ai_papers_timeline.md]] — 2021年DALL-E提出
- [[Zero-Shot Text-to-Image Generation (2021 论文)]] — Aditya Ramesh等人在OpenAI的研究

## 相关
- [[Zero-Shot Text-to-Image Generation (2021 论文)]] — described_in
- [[Aditya Ramesh]] — created_by
- [[OpenAI]] — developed_at
- [[CLIP]] — builds_on
- [[Variational Autoencoders]] — uses
- [[Text-to-Image Synthesis]] — exemplifies
- [[GPT-3]] — conceptually_similar_to
- [[Stable Diffusion]] — compares_to