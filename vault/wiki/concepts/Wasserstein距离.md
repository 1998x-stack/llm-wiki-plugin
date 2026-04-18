---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "生成模型", "GAN", "度量理论"]
aliases: ["Wasserstein Distance", "Earth Mover's Distance", "推土机距离", "W距离"]
relates_to: ["生成对抗网络（GAN）", "模式崩塌", "对抗训练", "纳什均衡"]
supersedes: null
---

# Wasserstein距离

## 概述
一种衡量两个概率分布差异的度量，在 WGAN 中替代 JS 散度作为 GAN 的损失函数，显著改善训练稳定性。

## 关键内容
1. **定义**：[[Wasserstein距离]]（又称 Earth Mover's Distance，推土机距离）衡量将一个概率分布"搬运"到另一个分布所需的最小工作量（质量 × 距离）。形式上，W(P, Q) = inf_{γ∈Π(P,Q)} E_{(x,y)~γ}[||x - y||]，其中 Π(P, Q) 是所有边缘分布为 P 和 Q 的联合分布的集合。
2. **在 GAN 中的应用**：原始 GAN 使用 JS 散度作为隐式度量，当两个分布不重叠时 JS 散度恒为 log 2，导致 [[梯度消失]]。[[Wasserstein距离]] 即使在分布不重叠时也能提供有意义的梯度，使训练更加稳定。WGAN（2017）用 Wasserstein 距离替代原始 GAN 的损失函数。
3. **实现方式**：WGAN 通过限制[[判别器]]（称为 critic）的 1-Lipschitz 连续性来近似 Wasserstein 距离。实现方法包括权重裁剪（原始 WGAN）、[[梯度惩罚]]（WGAN-GP）、谱归一化（SNGAN）等。这些方法确保[[判别器]]不会过强，从而避免 [[模式崩塌]] 和[[梯度消失]]。
4. **效果**：使用 Wasserstein 距离的 GAN 训练更稳定、超参数更不敏感、生成的样本质量更高。WGAN 的理论分析表明 Wasserstein 距离与生成样本质量有更好的相关性，提供了更有意义的训练指标。

## 来源
- 10_gan_2014.md — 源文件，GAN 演化谱系中提及 WGAN
- Arjovsky, M., Chintala, S., & Bottou, L. (2017). Wasserstein GAN. arXiv:1701.07875.

## 相关
- [[生成对抗网络（GAN）]] — extends
- [[模式崩塌]] — extends
- [[对抗训练]] — extends
- [[纳什均衡]] — relates_to
- [[梯度消失]] — resolves
