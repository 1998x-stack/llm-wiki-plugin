---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 深度学习, 神经网络]
aliases: [PNN, Product-based Neural Network]
relates_to:
  - {target: DeepFM, type: compares_to}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# PNN

## 概述
Product-based Neural Network，通过内积/外积操作显式建模[[特征交叉|特征交互]]的神经网络架构，[[DeepFM]] 论文中将其作为 Deep 部分的替代方案（[[DeepFM]]-P 变体）。

## 关键内容

1. **内积/外积操作**：PNN 使用内积（IPNN）、外积（OPNN）或混合（PNN*）操作来显式捕获[[特征交叉|特征交互]]，与标准 DNN 的隐式交互学习不同。
2. **[[DeepFM]]-P 变体**：[[DeepFM]] 论文提出了 [[DeepFM]]-P 变体，将 Deep 部分替换为 PNN，验证了"FM + Deep [[共享嵌入]]"框架的一般性和可扩展性。
3. **与 [[DeepFM]] 的关系**：PNN 本身是独立的 CTR 模型，但在 [[DeepFM]] 架构中可作为 Deep 部分的替换组件，体现了 [[DeepFM]] 框架的灵活性。

## 来源
- [Product-based Neural Networks for User Response Prediction (2016)](https://arxiv.org/abs/1611.00144)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — Deep 部分的可选替换
- [[CTR 预估]] — 应用场景
- [[特征交叉]] — 核心建模目标
