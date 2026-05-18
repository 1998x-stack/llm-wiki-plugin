---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [generative-models, image-generation, 深度学习]
aliases: [DDPM, Denoising Diffusion Probabilistic Models]
relates_to:
  - target: Jonathan Ho
    relation: relates_to
  - target: 扩散模型
    relation: part_of
  - target: GAN
    relation: compares_to
supersedes: null
---

# DDPM

## 概述
去噪扩散概率模型，[[扩散模型]]的开创性实现，在生成质量上媲美 GAN。

## 关键内容

1. **[[算法]]设计**：通过[[马尔可夫链]]逐步加噪和去噪，训练网络预测每一步的噪声。
2. **生成质量**：DDPM 在图像生成质量上首次媲美 [[GAN]]，且训练更稳定。
3. **[[计算]]成本**：[[AR 模型（自回归模型）|自回归]]生成过程[[计算]]成本高，后续的 [[Stable Diffusion]] 通过潜在空间扩散部分解决。

## 来源
- [[ai_papers_timeline.md]] — 2020 年时间线条目

## 相关
- [[Jonathan Ho]] — relates_to
- [[扩散模型]] — part_of
- [[GAN]] — compares_to
- [[Stable Diffusion]] — extends_to
