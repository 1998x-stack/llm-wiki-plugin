---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, generative-models, stable-diffusion, 深度学习]
aliases: [Rombach et al. 2022, Stable Diffusion 论文]
relates_to:
  - target: Robin Rombach
    relation: authored_by
  - target: Stable Diffusion
    relation: introduced
  - target: 潜在扩散模型
    relation: introduced
  - target: DDPM
    relation: extends
supersedes: null
---

# High-Resolution Image Synthesis with Latent Diffusion Models (2022 论文)

## 概述
提出 [[Stable Diffusion]] 的论文，通过在潜在空间进行扩散实现高效的高分辨率图像生成。

## 关键内容

1. **潜在空间扩散**：使用预训练 VAE 将图像压缩到潜在空间，在该空间进行扩散过程，大幅降低[[计算]]成本。
2. **条件生成**：通过交叉[[注意力机制（Attention Mechanism）|注意力机制]]将文本条件注入扩散过程，实现文本到图像的生成。
3. **开源影响**：[[Stable Diffusion]] 的开源发布推动了 AI 生成图像的民主化，催生了庞大的社区生态。

## 来源
- [[ai_papers_timeline.md]] — 2022 年时间线条目

## 相关
- [[Robin Rombach]] — authored_by
- [[Stable Diffusion]] — introduced
- [[潜在扩散模型]] — introduced
- [[DDPM]] — extends
