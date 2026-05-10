---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, generative-models, diffusion]
aliases: [Ho et al. 2020, DDPM 论文]
relates_to:
  - target: Jonathan Ho
    relation: authored_by
  - target: DDPM
    relation: introduced
  - target: 扩散模型
    relation: introduced
  - target: GAN
    relation: compares_to
supersedes: null
---

# Denoising Diffusion Probabilistic Models (2020 论文)

## 概述
提出 DDPM 的论文，开创了[[扩散模型]]生成图像的新[[规范化理论|范式]]，在生成质量上媲美 GAN。

## 关键内容

1. **前向加噪与反向去噪**：通过逐步添加高斯噪声将数据破坏，然后训练神经网络学习反向去噪过程。
2. **训练稳定性**：相比 [[GAN]] 的[[对抗训练]]，[[扩散模型]]训练更稳定，不易出现 [[模式崩塌]]。
3. **后续影响**：DDPM 直接催生了 [[Stable Diffusion]]、[[DALL-E]] 2 等应用，成为图像生成的主流路线。

## 来源
- [[ai_papers_timeline.md]] — 2020 年时间线条目

## 相关
- [[Jonathan Ho]] — authored_by
- [[DDPM]] — introduced
- [[扩散模型]] — introduced
- [[GAN]] — compares_to
- [[Stable Diffusion]] — influenced
