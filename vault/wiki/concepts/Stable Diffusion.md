---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [generative models, text-to-image, diffusion models]
aliases: ["Stable Diffusion", "Latent Diffusion", "SD", "LDM"]
relates_to:
  - target: "[[High-Resolution Image Synthesis with Latent Diffusion Models (2022 论文)]]"
    type: described_in
  - target: "[[Robin Rombach]]"
    type: created_by
  - target: "[[Stability AI]]"
    type: developed_at
  - target: "[[Latent Diffusion Models]]"
    type: instance_of
  - target: "[[DALL-E]]"
    type: compares_to
  - target: "[[DDPM]]"
    type: improves_upon
  - target: "[[Text-to-Image Synthesis]]"
    type: exemplifies
  - target: "[[扩散模型]]"
    type: part_of
supersedes: null
---

# Stable Diffusion

## 概述
Stable Diffusion是一种基于潜在空间的[[扩散模型]]，用于高质量文本到图像生成，具有高效性和可控性。

## 关键内容

1. **[[潜在扩散模型]]**：在预训练的自动编码器的潜在空间中执行扩散过程，大幅降低了[[计算]]复杂度，使得高分辨率图像生成变得可行。

2. **交叉[[注意力机制（Attention Mechanism）|注意力机制]]**：通过交叉[[注意力机制（Attention Mechanism）|注意力机制]]将文本条件信息注入扩散过程，实现精确的文本到图像生成控制。

3. **开源生态**：作为开源模型，Stable Diffusion激发了大量的社区开发和创新应用，推动了文本到图像生成领域的快速发展。

4. **潜在空间扩散**：使用预训练 VAE 将图像压缩到潜在空间，在该空间进行扩散过程，大幅降低[[计算]]成本。

5. **条件生成**：通过交叉[[注意力机制（Attention Mechanism）|注意力机制]]将文本条件注入扩散过程，实现文本到图像的生成。

6. **开源影响**：Stable Diffusion 的开源发布推动了 AI 生成图像的民主化，催生了庞大的社区生态。

## 来源
- [[ai_papers_timeline.md]] — 2022年Stable Diffusion提出
- [[High-Resolution Image Synthesis with Latent Diffusion Models (2022 论文)]] — Robin Rombach等人在Stability AI的研究

## 相关
- [[High-Resolution Image Synthesis with Latent Diffusion Models (2022 论文)]] — described_in
- [[Robin Rombach]] — created_by
- [[Stability AI]] — developed_at
- [[Latent Diffusion Models]] — instance_of
- [[DALL-E]] — compares_to
- [[DDPM]] — improves_upon
- [[Text-to-Image Synthesis]] — exemplifies
- [[扩散模型]] — part_of