---
type: entity
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [paper, deep-learning, normalization, google, 2015]
aliases: [Batch Normalization 论文, BN 论文, Ioffe & Szegedy 2015]
relates_to:
  - target: Batch Normalization
    relation: describes
  - target: Sergey Ioffe
    relation: authored_by
  - target: Christian Szegedy
    relation: authored_by
  - target: "GoogLeNet: Inception"
    relation: extends
  - target: 内部协变量偏移（Internal Covariate Shift）
    relation: introduces
  - target: Layer Normalization
    relation: inspired
  - target: Instance Normalization
    relation: inspired
  - target: Group Normalization
    relation: inspired
supersedes: null
---

# Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift (2015 论文)

## 概述
[[Sergey Ioffe]] 与 [[Christian Szegedy]] 于 2015 年发表的论文，提出 [[Batch Normalization]] 技术，解决深度网络训练中的[[内部协变量偏移]]问题，使训练速度提升 14 倍。

## 关键内容

1. **核心问题**：深度网络训练极其脆弱——学习率稍大则梯度爆炸发散，稍小则收敛极慢；对权重初始化极度敏感；Sigmoid 激活函数存在饱和区问题。
2. **核心方法**：对每个 mini-batch [[计算]]均值和方差，做归一化后引入可学习参数 γ（缩放）和 β（平移），让网络自行决定每层需要的分布。公式：$y_i = \gamma \frac{x_i - \mu_\mathcal{B}}{\sqrt{\sigma_\mathcal{B}^2 + \epsilon}} + \beta$
3. **训练/推理差异**：训练时使用当前 batch 统计量（引入正则化噪声），推理时使用训练过程中累积的滑动平均统计量。
4. **实验结果**：MNIST 上收敛快 14 倍；[[ImageNet]] 上 BN-[[Inception Network|Inception]] [[Top-5 错误率]] 4.82%（超越当时人类表现 5.1%）；可使用大 100 倍的学习率而不发散。
5. **正则化副作用**：batch 统计量的随机性类似于 [[Dropout]] 效果，使用 BN 后可减少甚至去掉 [[Dropout]]。

6. **理论争议**：论文声称有效原因是减少"[[内部协变量偏移]]"，但 2018 年 MIT 后续研究表明 BN 并没有显著减少[[内部协变量偏移]]，真正原因是让[[损失曲面（Loss Landscape）|优化景观]]（loss landscape）更加平滑——使梯度方向更稳定，更容易优化。

7. **归一化变体启发**：BN 启发了一系列归一化方法——[[Layer Normalization]]（沿 C×H×W，适合 [[Transformer]]）、[[Instance Normalization]]（沿 H×W，适合风格迁移）、[[Group Normalization]]（沿 group 内 C×H×W，适合小 batch size 目标检测）。

## 来源
- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化

## 相关
- [[Batch Normalization]] — describes
- [[Sergey Ioffe]] — authored_by
- [[Christian Szegedy]] — authored_by
- [[GoogLeNet: Inception]] — extends（在同一架构上验证 BN 效果）
- [[内部协变量偏移]] — describes
