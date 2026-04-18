---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "生成模型"]
aliases: ["GAN", "Generative Adversarial Network", "生成对抗网络", "生成式对抗网络"]
relates_to: ["对抗训练", "模式崩塌", "纳什均衡", "零和博弈", "生成器", "判别器", "Wasserstein距离", "VAE（变分自编码器）", "扩散模型（Diffusion Model）", "Dropout（随机失活）", "过拟合（Overfitting）"]
supersedes: null
---

# 生成对抗网络（GAN）

## 概述
一种通过[[生成器]]与[[判别器]][[零和博弈]]学习数据分布的生成模型框架，由 [[Ian Goodfellow]] 于 2014 年提出，开创了[[对抗训练]][[规范化理论|范式]]。

## 关键内容
1. **核心思想**：GAN 将生成建模转化为两个神经网络的博弈问题。[[生成器]]（造假者）从随机噪声 z ~ N(0, I) 生成伪造数据 G(z)，目标是欺骗[[判别器]]；[[判别器]]（鉴别专家）接收真实数据 x 或生成数据 G(z)，输出其为真实数据的概率 D(·) ∈ [0, 1]，目标是正确[[区分]]真假。两者通过[[对抗训练]]不断提升，最终达到 [[纳什均衡]]。
2. **数学目标函数**：min_G max_D V(D, G) = E_{x~p_data}[log D(x)] + E_{z~p_z}[log(1 - D(G(z)))]。这是一个 [[零和博弈]]（Minimax Game）。实践中[[生成器]]的目标改为最大化 log D(G(z)) 而非最小化 log(1-D(G(z)))，以避免早期训练时的梯度饱和问题。
3. **理论保证**：Goodfellow 严格证明了给定 G 时最优[[判别器]]为 D*_G(x) = p_data(x) / (p_data(x) + p_g(x))，全局最优点为 p_g = p_data，此时 D*(x) = 1/2（无法[[区分]]真假）。但现实中此条件无法满足，GAN 训练极不稳定。
4. **常见训练问题**：[[模式崩塌]]（[[生成器]]只生成几种样本）、训练不稳定（损失震荡不收敛）、[[梯度消失]]（[[判别器]]太强时[[生成器]]梯度为零）、超参数敏感。解决方案包括 [[Wasserstein距离]]（WGAN）、谱归一化、非饱和损失、Adam β₁=0.5 等。
5. **演化谱系**：原版 GAN（2014）→ DCGAN（2015，卷积化）→ WGAN（2017，Wasserstein 距离）→ Pix2Pix / CycleGAN（2017，条件控制）→ PGGAN（2018，渐进式训练）→ StyleGAN 系列（2019-2020，风格解耦）→ 最终被 [[扩散模型（Diffusion Model）]]（2020+）超越。

## 来源
- [[Generative Adversarial Nets (2014 论文)]] — 原始论文，NeurIPS 2014
- 10_gan_2014.md — 源文件，含完整 PyTorch 代码实现

## 相关
- [[Generative Adversarial Nets (2014 论文)]] — implements
- [[Ian Goodfellow]] — proposes
- [[对抗训练]] — part_of
- [[模式崩塌]] — relates_to
- [[纳什均衡]] — relates_to
- [[零和博弈]] — relates_to
- [[生成器]] — part_of
- [[判别器]] — part_of
- [[Wasserstein距离]] — extends
- [[VAE（变分自编码器）]] — compares_to
- [[扩散模型（Diffusion Model）]] — supersedes
