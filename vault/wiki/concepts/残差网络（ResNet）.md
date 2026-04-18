---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "计算机视觉", "网络架构", "机器学习"]
aliases: ["ResNet", "Residual Network", "何恺明网络"]
relates_to: ["卷积神经网络（CNN）", "退化问题（Degradation Problem）", "残差连接（Residual Connection）", "ImageNet"]
supersedes: null
---

# 残差网络（ResNet）

## 概述 (50-200字符)
何恺明等人于2015年提出的深度网络架构，通过[[残差连接]]解决退化问题，使网络可训练至152层以上，获[[ImageNet|ILSVRC]] 2015冠军并首次超越人类图像识别水平。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心架构**：残差网络通过引入[[残差连接（Residual Connection）]]（skip connection/[[残差连接（Residual Connection）|恒等捷径]]），将传统网络的直接映射 H(x) 重构为 H(x) = F(x) + x，其中 F(x) 是网络学习的残差。这一设计使梯度可以通过"梯度高速公路"直接流向浅层。
2. **两种残差块**：BasicBlock（Conv3×3-BN-ReLU-Conv3×3-BN，用于ResNet-18/34）和Bottleneck（Conv1×1降维-Conv3×3-Conv1×1升维，用于ResNet-50/101/152）。Bottleneck通过1×1卷积将计算量减少约8倍。
3. **ResNet家族**：ResNet-18(11M参数, 69.8% Top-1)、ResNet-34(21M, 73.3%)、ResNet-50(25M, 76.1%)、ResNet-101(44M, 77.4%)、ResNet-152(60M, 78.3%)。ResNet-152在[[ImageNet|ILSVRC]] 2015以3.57% Top-5错误率夺冠。
4. **退化问题的解决**：[[退化问题（Degradation Problem）]]指更深层网络训练误差反而更高的现象。ResNet通过残差学习使网络在最优解接近恒等映射时只需将权重推向零，比学习恒等变换容易得多。
5. **广泛影响**：[[残差连接]]成为现代深度学习的默认[[规范化理论|范式]]，被[[Transformer]]、GPT、BERT、扩散模型U-Net等架构广泛采用。后续衍生出DenseNet、SENet、ResNeXt、EfficientNet等变体。

## 来源
- [raw/articles/ai-papers/machine-learning/13_resnet_2015.md](../../raw/articles/ai-papers/machine-learning/13_resnet_2015.md) — 原始笔记文件

## 相关
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — implements
- [[卷积神经网络（CNN）]] — extends
- [[退化问题（Degradation Problem）]] — supersedes
- [[残差连接（Residual Connection）]] — uses
- [[ImageNet]] — compares_to
