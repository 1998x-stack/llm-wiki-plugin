---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 深度学习, 分解模型]
aliases: [FNN, Factorization-machine supported Neural Networks]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: DeepFM, type: compares_to}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# FNN

## 概述
Factorization-machine supported Neural Networks，采用两阶段训练策略（FM 预训练 [[Embedding]] + DNN），是 [[DeepFM]] 端到端训练[[规范化理论|范式]]的对比基线。

## 关键内容

1. **两阶段训练**：先用 FM 预训练 [[Embedding]]，再将预训练好的 [[Embedding]] 作为 DNN 的初始化。这种串行方式存在两个问题：预训练阶段的 FM 能力受限于二阶交互，且预训练的 [[Embedding]] 可能不是 DNN 的最优初始化。
2. **与 [[DeepFM]] 对比**：[[DeepFM]] 实现了从随机初始化开始的端到端训练，不需要 FM 预训练等额外步骤。实验表明端到端训练的 [[DeepFM]] 表现优于需要预训练的 FNN。
3. **历史地位**：FNN 是早期尝试将 FM 与 DNN 结合的工作，为后续 [[DeepFM]] 的[[共享嵌入]] + 端到端训练[[规范化理论|范式]]提供了重要的研究基础。

## 来源
- [Deep Learning over Multi-field Categorical Data (2016)](https://arxiv.org/abs/1601.02376)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[Factorization Machines]] — 预训练基础
- [[DeepFM]] — 端到端替代方案
- [[CTR 预估]] — 应用场景
- [[嵌入表示]] — Embedding 预训练策略
