---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 深度学习, 特征交叉]
aliases: [xDeepFM, eXtreme DeepFM]
relates_to:
  - {target: DeepFM, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# xDeepFM

## 概述
微软于 KDD 2018 提出的 [[CTR 预估]]模型，引入 CIN（Compressed Interaction Network）在向量级显式建模任意阶[[特征交叉|特征交互]]，解决 [[DeepFM]] FM 组件仅二阶交叉的局限。

## 关键内容

1. **CIN 网络**：提出 Compressed Interaction Network，在向量级（vector-wise）而非维度级（dimension-wise）进行[[特征交叉|特征交互]]计算，保留了更丰富的特征结构信息。
2. **显式任意阶交互**：相比 [[DeepFM]] 的 FM 组件仅能建模二阶交互，x[[DeepFM]] 通过 CIN 显式建模任意阶的向量级[[特征交叉|特征交互]]。
3. **解决 [[DeepFM]] 局限**：直接针对 [[DeepFM]] 的两大不足——FM 局限于二阶交叉、DNN 学习的是维度级交互而非向量级交互——提供了系统性的改进方案。
4. **KDD 2018**：论文 "x[[DeepFM]]: Combining Explicit and Implicit [[特征交叉|Feature Interaction]]s for Recommender Systems" 发表于 KDD 2018。

## 来源
- [xDeepFM (KDD 2018)](https://arxiv.org/abs/1803.05170)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 直接改进的前作
- DCN — 同期显式交叉的并行工作
- [[AutoInt]] — 后续可解释交互工作
- [[特征交叉]] — 核心建模目标
- [[CTR 预估]] — 应用场景
