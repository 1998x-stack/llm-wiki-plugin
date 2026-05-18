---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "网络架构", "梯度流", "机器学习"]
aliases: ["Residual Connection", "Skip Connection", "恒等捷径", "Identity Shortcut"]
relates_to: ["残差网络（ResNet）", "梯度消失", "反向传播", "Transformer"]
supersedes: null
---

# 残差连接（Residual Connection）

## 概述 (50-200字符)
一种网络结构设计，将输入x直接加到层的输出上形成H(x)=F(x)+x，使梯度可通过[[跳跃连接（Skip Connection）|恒等捷径]]直接流向浅层，有效解决深层网络的退化问题和[[梯度消失]]。

## 关键内容 (≥300字符, 用[[双链]])
1. **数学形式**：传统网络学习 H(x)，残差网络学习 F(x) = H(x) - x，输出为 F(x) + x。这一"加号"是[[残差网络（ResNet）|ResNet]]的核心创新，让网络只需学习残差而非完整映射。
2. **梯度流分析**：[[反向传播]]时 ∂L/∂x = ∂L/∂H · (∂F/∂x + 1)。无论 ∂F/∂x 多小（[[梯度消失]]），整体梯度至少有 ∂L/∂H · 1 这一项——梯度可以绕过任意层直接流向浅层，形成"梯度高速公路"。
3. **为什么更容易学**：若最优解接近恒等映射 H*(x) ≈ x，则残差 F*(x) ≈ 0。将网络权重推向零比将权重推向恒等变换容易得多，这使深层网络的优化变得可行。
4. **实现细节**：当输入输出维度不匹配时（stride≠1或通道数变化），shortcut需用1×1卷积进行投影对齐。BasicBlock用于[[残差网络（ResNet）|ResNet]]-18/34，Bottleneck用于[[残差网络（ResNet）|ResNet]]-50/101/152。
5. **广泛影响**：[[残差连接]]已成为现代深度学习的默认组件，被[[Transformer]]（每个子层都有残差）、GPT、BERT、[[扩散模型]][[U-Net]]等架构采用。后续衍生出DenseNet（密集连接）、SENet（通道[[注意力机制|注意力]]+残差）等变体。

## 来源
- [raw/articles/ai-papers/machine-learning/13_resnet_2015.md](../../raw/articles/ai-papers/machine-learning/13_resnet_2015.md) — 原始笔记文件

## 相关
- [[残差网络（ResNet）]] — uses
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — implements
- [[退化问题（Degradation Problem）]] — supersedes
- [[反向传播]] — extends
- [[Transformer]] — uses
