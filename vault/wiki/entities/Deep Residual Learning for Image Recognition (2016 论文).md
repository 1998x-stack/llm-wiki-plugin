---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "计算机视觉", "残差网络"]
aliases: ["Deep Residual Learning for Image Recognition", "ResNet 论文", "何恺明 2016"]
relates_to: ["残差网络（ResNet）", "卷积神经网络（CNN）", "ImageNet"]
supersedes: null
---

# Deep Residual Learning for Image Recognition (2016 论文)

## 概述 (50-200字符)
何恺明等人提出的残差学习框架，通过引入[[残差连接]]解决了深度神经网络的退化问题，使网络能够训练至152层以上。该论文获CVPR 2016最佳论文，[[ImageNet|ILSVRC]] 2015冠军。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[退化问题（Degradation Problem）]]**：实验发现更深的网络（如56层）训练误差反而比浅层网络（如20层）更高，这不是[[过拟合（Overfitting）|过拟合]]而是优化问题——深层网络学不会恒等映射。
2. **残差学习公式**：将目标映射重构为 H(x) = F(x) + x，网络只需学习残差 F(x) = H(x) - x。当最优解接近恒等映射时，将权重推向零比学习恒等变换更容易。
3. **梯度高速公路**：[[反向传播]]时 ∂L/∂x = ∂L/∂H · (∂F/∂x + 1)，[[残差连接（Residual Connection）|恒等捷径]]贡献的"1"确保梯度可以绕过任意层直接流向浅层，有效解决[[梯度消失]]问题。
4. **两种残差块设计**：BasicBlock（两层3×3卷积，用于[[残差网络（ResNet）|ResNet]]-18/34）和Bottleneck（1×1降维→3×3→1×1升维，用于[[残差网络（ResNet）|ResNet]]-50/101/152），后者将计算量减少约8倍。
5. **[[ImageNet|ILSVRC]] 2015 成果**：[[残差网络（ResNet）|ResNet]]-152以3.57% Top-5错误率夺冠，首次超越人类水平（约5%）。

## 来源
- [raw/articles/ai-papers/machine-learning/13_resnet_2015.md](../../raw/articles/ai-papers/machine-learning/13_resnet_2015.md) — 原始笔记文件

## 相关
- [[残差网络（ResNet）]] — implements
- [[卷积神经网络（CNN）]] — extends
- [[ImageNet]] — compares_to
- [[退化问题（Degradation Problem）]] — caused
- [[残差连接（Residual Connection）]] — implements
