---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, 注意力机制, 分解模型]
aliases: [AFM, Attentional Factorization Machines]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: DeepFM, type: compares_to}
  - {target: 特征交叉, type: uses}
  - {target: CTR 预估, type: implements}
supersedes: null
---

# AFM

## 概述
引入[[注意力机制（Attention Mechanism）|注意力机制]]的[[Factorization Machines|因子分解机]]变体，为不同[[特征交叉|特征交互]]赋予不同权重，解决 FM 暴力枚举所有特征对缺乏选择性的问题。

## 关键内容

1. **注意力加权[[特征交叉|特征交互]]**：FM 组件会[[计算]]所有特征对之间的交互，没有选择性地关注更重要的交互。AFM 通过引入[[注意力机制（Attention Mechanism）|注意力机制]]来为不同的[[特征交叉|特征交互]]赋予不同的权重。
2. **解决 [[DeepFM]] 局限**：[[DeepFM]] 的 FM 部分暴力枚举所有特征对，在特征数量很大时大量不相关的特征对交互实际上是噪声。AFM 的[[注意力机制（Attention Mechanism）|注意力机制]]可以自动筛选重要交互。
3. **与 [[DeepFM]] 的关系**：AFM 是对 FM 本身的改进，可以视为 [[DeepFM]] FM 组件的潜在替换方案。将 AFM 替代 FM 集成到 [[DeepFM]] 架构中是一个自然的研究方向。

## 来源
- [Attentional Factorization Machines: Learning the Weight of Feature Interactions via Attention Networks (IJCAI 2017)](https://arxiv.org/abs/1708.04617)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[Factorization Machines]] — 改进的基础模型
- [[DeepFM]] — 可替代其 FM 组件
- [[特征交叉]] — 核心建模目标
- [[CTR 预估]] — 应用场景
