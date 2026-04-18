---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "优化问题", "网络训练", "机器学习"]
aliases: ["Degradation Problem", "深度网络退化", "退化悖论"]
relates_to: ["残差网络（ResNet）", "梯度消失", "过拟合"]
supersedes: null
---

# 退化问题（Degradation Problem）

## 概述 (50-200字符)
深度神经网络中出现的反直觉现象：随着网络层数增加，训练误差（非测试误差）反而升高，表明深层网络无法有效学习，甚至学不会简单的恒等映射。

## 关键内容 (≥300字符, 用[[双链]])
1. **现象描述**：在CIFAR-10实验中，20层网络训练误差为8.75%，而56层网络为7.61%——更深的网络训练误差反而更高。这不是[[过拟合]]，因为训练集本身的表现也变差了。
2. **退化悖论**：理论上，56层网络可以把后36层学成恒等映射，效果至少与20层网络相当。但优化算法做不到这一点——深层网络学不会恒等映射（Identity Mapping）。
3. **根本原因**：传统网络要求每层直接从零学习目标映射 H(x)。当网络极深时，梯度在[[反向传播]]过程中逐渐消失，导致浅层参数几乎无法更新。
4. **解决方案**：[[残差网络（ResNet）]]通过[[残差连接（Residual Connection）]]将学习目标改为残差 F(x) = H(x) - x。当最优解接近恒等映射时，残差 F*(x) ≈ 0，将权重推向零比学习恒等变换容易得多。
5. **历史意义**：该问题的发现直接催生了残差学习的提出，成为深度学习架构设计的转折点。今天几乎所有深度架构（[[Transformer 架构|Transformer]]、GPT等）都包含[[残差连接]]来避免退化问题。

## 来源
- [raw/articles/ai-papers/machine-learning/13_resnet_2015.md](../../raw/articles/ai-papers/machine-learning/13_resnet_2015.md) — 原始笔记文件

## 相关
- [[残差网络（ResNet）]] — supersedes
- [[残差连接（Residual Connection）]] — extends
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — caused
- [[梯度消失]] — relates_to
