---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "生成模型", "NeurIPS"]
aliases: ["Generative Adversarial Nets", "GAN paper 2014", "生成对抗网络论文"]
relates_to: ["生成对抗网络（GAN）", "Ian Goodfellow", "Yoshua Bengio", "对抗训练", "纳什均衡"]
supersedes: null
---

# Generative Adversarial Nets (2014 论文)

## 概述
[[Ian Goodfellow]] 等人于 NeurIPS 2014 发表的开创性论文，首次提出[[生成对抗网络（GAN）|生成对抗网络]]框架，通过两个神经网络的[[零和博弈]]实现数据分布的隐式建模。

## 关键内容
1. **核心贡献**：提出了一种全新的生成模型框架，无需显式建模数据分布。[[生成器]] 和 [[判别器]] 通过交替训练进行对抗博弈，最终使生成分布收敛至真实数据分布。这一思想源自一次酒吧争论后的灵感，Goodfellow 当晚回家即实现了原型。
2. **理论证明**：论文严格证明了两个关键命题：（1）给定[[生成器]] G，最优[[判别器]]为 D*_G(x) = p_data(x) / (p_data(x) + p_g(x))；（2）全局最优时 p_g = p_data，[[判别器]]输出恒为 1/2，全局损失为 -log 4。定理表明若 G 和 D 有足够容量且每步更新 D 至最优，算法收敛至真实分布。
3. **训练算法**：每步先采样真实数据和噪声向量，上升梯度训练[[判别器]] k 步（通常 k=1），再采样新噪声向量下降梯度训练[[生成器]] 1 步。实践中[[生成器]]使用非饱和目标 log D(G(z)) 替代原目标 log(1-D(G(z))) 以缓解梯度饱和。
4. **历史影响**：[[Yann LeCun]] 称其为"过去十年机器学习中最有趣的想法"。该论文催生了整个[[生成对抗网络（GAN）|生成对抗网络]]研究领域，包括 DCGAN、WGAN、StyleGAN 等后续工作，最终推动了生成式 AI 的爆发。

## 来源
- Goodfellow, I., Pouget-Abadie, J., Mirza, M., Xu, B., Warde-Farley, D., Ozair, S., Courville, A., & Bengio, Y. (2014). Generative adversarial nets. NeurIPS, 27.

## 相关
- [[Ian Goodfellow]] — author
- [[Yoshua Bengio]] — author
- [[生成对抗网络（GAN）]] — implements
- [[对抗训练]] — proposes
- [[纳什均衡]] — uses
