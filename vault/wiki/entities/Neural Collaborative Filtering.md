---
type: entity
entity_type: paper
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 深度学习, NCF]
aliases: [Neural Collaborative Filtering, NCF, 神经协同过滤]
relates_to:
  - {target: 何向南, type: implements}
  - {target: 矩阵分解, type: extends}
  - {target: Embedding, type: uses}
supersedes: null
---

# Neural Collaborative Filtering

## 概述
[[何向南]]等人 2017 年提出的深度学习推荐框架，将[[矩阵分解]]显式纳入神经网络架构，用 MLP 替换内积以捕捉非线性交互。

## 关键内容

1. **核心论点**：[[矩阵分解]]可被视为一种特殊的浅层神经网络（用户 ID 和物品 ID 通过 [[Embedding]] 层映射为稠密向量，通过内积计算匹配分数）。N[[协同过滤|CF]] 用更强大的多层感知机（MLP）替换简单内积，以捕捉更复杂的用户-物品交互模式。
2. **Neu[[矩阵分解|MF]] 模型**：将 Generalized [[矩阵分解|Matrix Factorization]]（G[[矩阵分解|MF]]，本质即[[矩阵分解]]）和 MLP 并行组合，取得了优于纯[[矩阵分解]]的效果。
3. **历史定位**：N[[协同过滤|CF]] 代表了推荐系统从传统[[矩阵分解]]向深度学习范式过渡的关键节点，后续 BERT4Rec、SASRec 等序列推荐方法均在此基础上进一步演进。
4. **与 [[矩阵分解|MF]] 的关系**：N[[协同过滤|CF]] 并未否定[[矩阵分解]]，而是将其作为子模块（G[[矩阵分解|MF]]）纳入更广泛的神经网络框架，体现了"加法式"的建模哲学。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[何向南]] — 提出者
- [[矩阵分解]] — NCF 的基线和子模块
- [[Embedding]] — NCF 使用的核心技术
