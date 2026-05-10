---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 矩阵分解, 算法]
aliases: ["SVD++", "SVD Plus Plus"]
relates_to: []
supersedes: null
---

# SVD++

## 概述
SVD++ 是一种改进的[[矩阵分解]]模型，通过将[[隐式反馈]]信息融入用户表示中，显著提升了推荐系统在稀疏数据上的表现。

## 关键内容

1. **核心思想**：
   SVD++ 模型将用户的[[隐式反馈]]（如浏览、收藏、购买等行为）融入到用户隐因子向量的表示中，使得即使在显式评分极度稀疏的情况下，模型也能利用丰富的[[隐式反馈|隐式信号]]来丰富用户画像。

2. **数学公式**：
   $$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T \left( p_u + |R(u)|^{-1/2} \sum_{j \in R(u)} y_j \right)$$
   
   其中 $R(u)$ 是用户 $u$ 交互过的物品集合，$y_j$ 是物品 $j$ 作为[[隐式反馈]]的因子向量，$|R(u)|^{-1/2}$ 是归一化因子。

3. **优势**：
   - 在 [[Netflix]] 数据集上，SVD++ 将 100 维模型的 RMSE 从 0.9025 降至 0.8924，实现了约 1% 的相对提升
   - 有效解决了稀疏性问题，充分利用了用户的各种[[隐式反馈|行为信号]]
   - 将[[显式反馈]]和[[隐式反馈]]有机融合在同一框架内

4. **应用场景**：
   SVD++ 成为现代推荐系统的标准做法，广泛应用于各种需要同时利用显式和[[隐式反馈]]的场景。

## 来源
- [[推荐系统/04-matrix-factorization-for-recsys.md]] — 详细介绍 SVD++ 模型
- [[]] — 

## 相关
- [[矩阵分解]] — 基础方法
- [[隐式反馈]] — 输入数据类型
- [[timeSVD++]] — 时序扩展
- [[Matrix Factorization Techniques for Recommender Systems]] — 提出论文