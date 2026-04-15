---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 深度学习, 表示学习]
aliases: [Embedding, 嵌入向量, 嵌入表示]
relates_to:
  - {target: 隐因子模型, type: compares_to}
  - {target: 矩阵分解, type: extends}
  - {target: Neural Collaborative Filtering, type: uses}
supersedes: null
---

# Embedding

## 概述
将离散对象（用户、物品、词等）映射为低维稠密向量的表示学习方法，在推荐系统中等价于[[矩阵分解]]的隐因子向量。

## 关键内容

1. **与[[矩阵分解]]的关系**：[[矩阵分解]]中的用户隐因子向量 $p_u$ 和物品隐因子向量 $q_i$，本质上就是 Embedding。用户 ID 和物品 ID 分别通过 Embedding 层映射为稠密向量，通过内积计算匹配分数。
2. **历史发现**：2013 年 Word2Vec 引发 NLP 领域的 Embedding 革命之后，人们回过头来才发现，推荐系统领域早在 2006-2009 年就已经在使用 Embedding 思想了。
3. **[[矩阵分解]]作为浅层神经网络**：[[矩阵分解]]可被视为一种特殊的浅层神经网络——Embedding 层 + 内积层。这正是 [[Neural Collaborative Filtering]] 中 Generalized [[矩阵分解|Matrix Factorization]]（G[[矩阵分解|MF]]）模块的精确定义。
4. **现代应用**：Embedding 已成为现代推荐系统的基础组件，从 [[Wide & Deep]] 的 Embedding 层到双塔模型的用户/物品塔 Embedding，再到[[对比学习]]中的向量表示，均延续了[[矩阵分解]]的 Embedding 思想。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[隐因子模型]] — Embedding 的前身概念
- [[矩阵分解]] — Embedding 的早期实现
- [[Neural Collaborative Filtering]] — 显式使用 Embedding 的深度学习框架
