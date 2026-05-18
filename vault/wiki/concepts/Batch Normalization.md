---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [深度学习, 归一化, CNN, 训练稳定性, LLM能力, 优化景观]
aliases: [批归一化, BatchNorm, BN]
relates_to:
  - target: Layer Normalization
    relation: compares_to
  - target: Instance Normalization
    relation: compares_to
  - target: Group Normalization
    relation: compares_to
  - target: 残差连接（Residual Connection）
    relation: relates_to
  - target: 内部协变量偏移（Internal Covariate Shift）
    type: solves
  - target: ReLU激活函数
    relation: relates_to
  - target: Dropout（随机失活）
    relation: compares_to
  - target: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift"
    relation: implements
  - target: Sergey Ioffe
    relation: created_by
  - target: Christian Szegedy
    relation: created_by
supersedes: null
---

# Batch Normalization

## 概述

在一个 batch 上对某一特征维度统计均值和方差并做归一化，解决[[内部协变量偏移]]问题。在 CNN 中广泛使用，使训练速度提升 14 倍，大幅降低对初始化和学习率的敏感性。

## 关键内容

1. **核心公式**：对 mini-batch $\mathcal{B} = \{x_1, \ldots, x_m\}$，[[计算]]均值 $\mu_\mathcal{B}$ 和方差 $\sigma_\mathcal{B}^2$，归一化 $\hat{x}_i = \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}}$，再缩放平移 $y_i = \gamma \hat{x}_i + \beta$。其中 γ 和 β 是可学习参数，让网络自行决定每层需要的分布。

2. **训练 vs 推理**：训练时使用当前 batch 统计量（引入正则化噪声），推理时使用训练过程中累积的滑动平均统计量（running_mean, running_var），两者行为不一致。

3. **在 CNN 中的位置**：通常插在卷积层之后、激活函数之前（Conv → BN → ReLU），使激活处于合理范围。后来研究发现放在激活函数后有时效果更好，至今仍有争议。

4. **正则化副作用**：batch 统计量的随机性类似于 [[Dropout（随机失活）|Dropout]] 效果，使用 BN 后可减少甚至去掉 [[Dropout]]（尤其卷积层）。

5. **适用场景**：batch size 较大（≥16）、输入尺寸固定的 CNN 图像任务中效果好。不适合 [[Transformer架构|Transformer]]：序列长度可变导致 batch 统计不稳定；不同位置 token 语义差异大不宜混合统计；[[AR 模型（自回归模型）|自回归]]生成场景单样本推理时无法正常工作。

6. **局限性**：小 batch size 时方差估计不准（→ [[Group Normalization]]）；在线学习/单样本推理无法使用（→ [[Layer Normalization]]）；分布式训练跨设备同步统计量开销大。

7. **理论争议**：论文声称有效原因是减少"[[内部协变量偏移]]"，但 2018 年 MIT 后续研究表明 BN 并没有显著减少[[内部协变量偏移]]，真正原因是**让[[损失曲面（Loss Landscape）|优化景观]]（loss landscape）更加平滑**——使梯度方向更稳定，更容易优化。这个"[[损失景观平滑化]]"解释目前更被学界接受。

8. **归一化变体对比**：
   | 方法 | 归一化维度 | 主要应用 | Batch Size 要求 |
   |------|-----------|---------|----------------|
   | Batch Norm | 沿 N 方向（每个通道独立） | CNN | 较大 (≥16) |
   | [[Layer Normalization]] | 沿 C×H×W 方向（每个样本独立） | [[Transformer]], LSTM | 任意 |
   | [[Instance Normalization]] | 沿 H×W 方向（每个样本每个通道独立） | 风格迁移 | 任意 |
   | [[Group Normalization]] | 沿 group 内的 C×H×W | 目标检测 | 任意 |

9. **实验结果**：在 MNIST 上，BN 能将达到 99% 测试准确率的步骤从约 50 万步减少到 3.5 万步（快 14 倍！）；在 [[ImageNet]] 上，BN-[[Inception Network|Inception]] 达到了 4.09% 的 [[Top-5 错误率]]，超越了当时的人类表现（5.1%）。

10. **历史背景**：2014-2015 年间，研究者们试图训练越来越深的网络，但遇到了训练极其脆弱的问题——学习率稍大则[[梯度爆炸]]，稍小则收敛极慢，权重初始化不好则训练失败。BN 的提出彻底改变了这一局面，让深度网络训练从"玄学艺术"变成了"工程科学"。

11. **[[Google]] 机构**：该论文由 [[Sergey Ioffe]] 和 [[Christian Szegedy]] 在 [[Google]] 机构完成，发表于 2015 年，成为现代深度学习的基础组件之一。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-Self-Attention机制解析]] — Self-Attention 机制解析系列 QA
- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化

## 相关

- [[Layer Normalization]] — compares_to（Transformer 选择 LayerNorm 而非 BatchNorm 的核心对比）
- [[Instance Normalization]] — compares_to（BN 的变体，沿空间维度归一化，用于风格迁移）
- [[Group Normalization]] — compares_to（BN 的变体，按通道组归一化，解决小 batch size 问题）
- [[残差连接（Residual Connection）]] — relates_to（BN 与残差连接配合使用于 ResNet 等架构）
- [[内部协变量偏移（Internal Covariate Shift）]] — solves（BN 论文提出的核心解决方案）
- [[ReLU激活函数]] — relates_to（BN 通常放在 ReLU 之前）
- [[Dropout（随机失活）]] — compares_to（BN 的正则化效果可部分替代 Dropout）
