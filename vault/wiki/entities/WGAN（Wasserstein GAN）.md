---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["机器学习", "深度学习", "生成模型", "ICLR"]
aliases: ["WGAN", "Wasserstein GAN", "Wasserstein生成对抗网络"]
relates_to: 
  - target: "[[生成对抗网络（GAN）]]"
    type: extends
    confidence: 0.9
  - target: "[[Generative Adversarial Nets (2014 论文)]]"
    type: improves
    confidence: 0.9
  - target: "[[Wasserstein距离]]"
    type: uses
    confidence: 1.0
  - target: "[[Martin Arjovsky]]"
    type: author
    confidence: 0.9
  - target: "[[Soumith Chintala]]"
    type: author
    confidence: 0.8
  - target: "[[Léon Bottou]]"
    type: author
    confidence: 0.8
  - target: "[[Ian Goodfellow]]"
    type: successor
    confidence: 0.7
supersedes: null
---

# WGAN（Wasserstein GAN）

## 概述
2017年提出的Wasserstein[[生成对抗网络（GAN）|生成对抗网络]]，通过使用[[Wasserstein距离]]（Earth Mover距离）替代JS散度作为训练目标，有效解决了传统GAN训练不稳定和[[模式崩塌]]问题，提供了有意义的训练损失指标。

## 关键内容
1. **核心创新**：WGAN用[[Wasserstein距离]]（也称Earth Mover距离）替代原始GAN中的JS散度作为分布相似性度量。[[Wasserstein距离]]即使在两个分布不重叠时也能提供连续的梯度信息，解决了传统GAN中[[梯度消失]]的问题。

2. **理论基础**：WGAN基于最优传输理论，使用1-Lipschitz约束下的Wasserstein-1距离。通过Kantorovich-Rubinstein对偶性，将[[计算]][[Wasserstein距离]]转化为求解一个优化问题：W(p_data, p_g) = sup_{||f||_L ≤ 1} E_{x~p_data}[f(x)] - E_{x~p_g}[f(x)]，其中f为1-Lipschitz函数。

3. **实现方法**：WGAN将[[判别器]]（在WGAN中称为Critic）限制为1-Lipschitz函数，通过权重裁剪（weight clipping）、梯度惩罚（WGAN-GP）或谱归一化等方式实现Lipschitz约束。训练目标变为最大化 E_{x~p_data}[D(x)] - E_{z~p_z}[D(G(z))]。

4. **优势**：WGAN提供了有意义的训练损失指标（[[Wasserstein距离]]的近似），训练更加稳定，几乎消除了[[模式崩塌]]问题，并且对超参数变化不敏感。[[判别器]]（Critic）的训练不再需要与[[生成器]]保持平衡，可以多训练几轮。

5. **影响**：WGAN为后续的GAN改进方法奠定了基础，催生了WGAN-GP、SNGAN等一系列稳定GAN训练的方法，推动了生成模型的发展。

## 来源
- [[Arjovsky, Martin, Soumith Chintala, and Léon Bottou. "Wasserstein gan." ICML 2017]] — 原始论文
- paper_08_gan.md — 源文件

## 相关
- [[生成对抗网络（GAN）]] — extends
- [[Wasserstein距离]] — uses
- [[模式崩塌]] — solves
- [[Ian Goodfellow]] — successor
- [[生成器]] — part_of
- [[判别器]] — part_of