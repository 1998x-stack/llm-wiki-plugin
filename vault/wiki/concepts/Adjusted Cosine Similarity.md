---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 相似度度量, 协同过滤]
aliases: ["Adjusted Cosine", "调整余弦相似度", "修正余弦相似度"]
relates_to:
  - target: "[[基于物品的协同过滤]]"
    type: uses
  - target: "[[Item-Based Collaborative Filtering Recommendation Algorithms]]"
    type: part_of
supersedes: null
---

# Adjusted Cosine Similarity

## 概述
一种改进的余弦相似度计算方法，通过减去每个用户的平均评分来消除用户评分尺度差异对物品相似度计算的干扰，是 [[基于物品的协同过滤|Item-Based CF]] 中表现最优的相似度度量方法。

## 关键内容

1. **公式定义**：sim(i,j) = Σ_u[(r_ui - r̄_u)(r_uj - r̄_u)] / (√Σ_u(r_ui - r̄_u)² × √Σ_u(r_uj - r̄_u)²)，其中 r̄_u 是用户 u 的平均评分，求和遍历所有同时评价过物品 i 和 j 的用户集合。

2. **与普通余弦相似度的区别**：普通余弦相似度直接将物品视为用户评分向量计算夹角，没有考虑不同用户的评分尺度差异。一个"宽容"的用户可能给所有物品打 4-5 分，而"严格"的用户只给 2-3 分，这会导致相似度计算偏差。

3. **与皮尔逊相关系数的区别**：皮尔逊相关系数减去的是物品的平均评分（r̄_i），而调整后余弦相似度减去的是用户的平均评分（r̄_u）。在 [[基于物品的协同过滤|Item-Based CF]] 框架下，调整后余弦相似度的实验表现更优。

4. **直观理解**：如果用户 A 通常打分偏高（均分 4.2），他给电影 X 和 Y 都打了 5 分，调整后 X 和 Y 各自获得 0.8 的"超额评分"，反映用户 A 确实认为这两部电影都不错。这种调整消除了用户个人评分习惯的干扰。

5. **实验验证**：在 [[Item-Based Collaborative Filtering Recommendation Algorithms]] 的实验中，调整后余弦相似度在三种相似度方法（余弦相似度、调整后余弦相似度、皮尔逊相关系数）中表现最优，显著降低了 MAE。

## 来源
- [[Item-Based Collaborative Filtering Recommendation Algorithms]] — 第 5.2 节

## 相关
- [[基于物品的协同过滤]] — uses
- [[Item-Based Collaborative Filtering Recommendation Algorithms]] — part_of
- [[基于用户的协同过滤]] — compares_to
