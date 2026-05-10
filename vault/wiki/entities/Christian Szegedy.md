---
type: entity
status: active
confidence: 0.80
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [person, computer-vision, CNN, inception]
aliases: [Christian Szegedy]
relates_to:
  - target: GoogLeNet / Inception
    relation: contributed_to
  - target: Batch Normalization
    relation: contributed_to
  - target: "Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift (2015 论文)"
    relation: authored_by
  - target: Sergey Ioffe
    relation: collaborates_with
supersedes: null
---

# Christian Szegedy

## 概述
[[计算]]机视觉研究者，[[Inception Network|GoogLeNet]]/[[Inception Network|Inception]] 架构的主要设计者，后提出对抗样本概念。

## 关键内容

1. **[[Going Deeper with Convolutions (2014 论文)|GoogLeNet 论文]]（2014）**：发表《Going Deeper with Convolutions》，提出 [[GoogLeNet: Inception|Inception 模块]]，通过多尺度卷积核并行处理实现高效的特征提取。
2. **[[GoogLeNet: Inception|Inception 模块]]**：使用 1×1、3×3、5×5 卷积核并行[[计算]]并拼接输出，在保持[[计算]]效率的同时增加网络宽度。
3. **[[Batch Normalization]]**：与 [[Sergey Ioffe]] 合作提出 [[Batch Normalization]]，成为加速网络训练的标准技术。在 [[Inception Network|Inception]] 架构上验证 BN 效果，BN-[[Inception Network|Inception]] [[Top-5 错误率]] 4.82%（集成后 4.09%），超越当时人类表现（5.1%）。

## 来源
- [[ai_papers_timeline.md]] — 2014、2015 年时间线条目
- [[raw/articles/ai-papers/foundations/paper_04_batchnorm.md]] — 论文精读 #04：批归一化

## 相关
- [[GoogLeNet: Inception]] — contributed_to
- [[Batch Normalization]] — contributed_to
- [[Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift (2015 论文)]] — authored_by
