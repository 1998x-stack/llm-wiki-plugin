---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 深度学习, 注意力机制]
aliases: [AutoInt, Automatic Feature Interaction Learning]
relates_to:
  - {target: DeepFM, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# AutoInt

## 概述
2019 年提出的 [[CTR 预估]]模型，通过[[多头注意力|多头自注意力]]机制显式建模[[特征交叉|特征交互]]，解决了 [[DeepFM]] DNN 部分黑盒不可解释的问题。

## 关键内容

1. **[[多头注意力|多头自注意力]]**：利用 [[Transformer架构|Transformer]] 式的[[多头注意力|多头自注意力]]机制（Multi-Head [[Self-Attention机制|Self-Attention]]）来建模[[特征交叉|特征交互]]，使得交互学习过程透明可解释。
2. **可解释交互**：相比 [[DeepFM]] 中 DNN 的隐式"黑盒"高阶交互，AutoInt 通过注意力权重可以直观看到哪些特征对之间的交互被模型认为更重要。
3. **解决 [[DeepFM]] 局限**：直接针对 [[DeepFM]] 的"DNN 部分隐式交叉难以解释"这一不足，提供了可解释的[[特征交叉|特征交互]]学习方案。
4. **CTR 模型演化链**：在 CTR 模型演化中代表"可解释性"方向的重要工作，位于 [[DeepFM]] → AutoInt → DCN V2 的演进路径上。

## 来源
- [AutoInt: Automatic Feature Interaction Learning via Self-Attentive Neural Networks (2019)](https://arxiv.org/abs/1810.11921)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 改进的前作
- [[xDeepFM]] — 同期显式交互工作
- [[特征交叉]] — 核心建模目标
- [[CTR 预估]] — 应用场景
