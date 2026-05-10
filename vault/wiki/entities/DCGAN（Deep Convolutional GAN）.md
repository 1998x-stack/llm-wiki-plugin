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
aliases: ["DCGAN", "Deep Convolutional GAN", "深度卷积生成对抗网络"]
relates_to: 
  - target: "[[生成对抗网络（GAN）]]"
    type: extends
    confidence: 0.9
  - target: "[[Generative Adversarial Nets (2014 论文)]]"
    type: extends
    confidence: 0.9
  - target: "[[Alec Radford]]"
    type: author
    confidence: 0.8
  - target: "[[Luke Metz]]"
    type: author
    confidence: 0.8
  - target: "[[Soumith Chintala]]"
    type: author
    confidence: 0.8
  - target: "[[Batch Normalization]]"
    type: uses
    confidence: 0.8
  - target: "[[卷积神经网络]]"
    type: part_of
    confidence: 0.9
supersedes: null
---

# DCGAN（Deep Convolutional GAN）

## 概述
2015年提出的深度卷积[[生成对抗网络（GAN）|生成对抗网络]]，通过将传统GAN的全连接层替换为卷积层，显著提升了生成质量和训练稳定性，成为后续所有CNN-based生成模型的基础架构。

## 关键内容
1. **架构创新**：DCGAN首次将[[卷积神经网络（CNN）|卷积神经网络]]成功应用于GAN框架，用ConvTranspose2d（转置卷积）替代池化层进行上采样，用strided convolutions替代池化层进行下采样，整个网络完全由可学习的卷积操作构成。

2. **训练稳定性提升**：相比原始GAN，DCGAN引入了多项关键技术：（1）在[[生成器]]中广泛使用[[Batch Normalization]]（除输出层）；（2）在[[判别器]]中使用Leaky[[ReLU激活函数]]；（3）[[生成器]]输出层使用Tanh激活而非ReLU；（4）取消全连接层，采用纯卷积架构。

3. **设计原则**：DCGAN建立了生成模型的通用设计准则：使用卷积替代全连接、逐步上采样、逐步下采样、[[Batch Normalization|批归一化]]等，这些原则被后续几乎所有基于CNN的生成模型所采纳。

4. **应用价值**：DCGAN使得GAN能够生成高质量的图像（如64x64人脸），并展示了GAN在特征学习方面的潜力，为后来的PGGAN、StyleGAN等高分辨率生成模型奠定了基础。

## 来源
- [[Radford, Alec, et al. "Unsupervised representation learning with deep convolutional generative adversarial networks." arXiv 2015]] — 原始论文
- paper_08_gan.md — 源文件

## 相关
- [[生成对抗网络（GAN）]] — extends
- [[Generative Adversarial Nets (2014 论文)]] — extends
- [[Alec Radford]] — author
- [[卷积神经网络]] — part_of
- [[Batch Normalization]] — uses
- [[转置卷积]] — uses