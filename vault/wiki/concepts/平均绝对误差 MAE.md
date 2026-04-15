---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 评估指标, 机器学习]
aliases: ["MAE", "Mean Absolute Error", "平均绝对误差"]
relates_to:
  - target: "[[基于物品的协同过滤]]"
    type: uses
  - target: "[[Item-Based Collaborative Filtering Recommendation Algorithms]]"
    type: uses
supersedes: null
---

# 平均绝对误差 MAE

## 概述
推荐系统预测评分准确性的核心评估指标，计算预测评分与实际评分之间绝对误差的平均值，MAE 越小说明预测越准确。

## 关键内容

1. **公式定义**：MAE = (1/N) × Σ|p_i - q_i|，其中 p_i 是预测评分，q_i 是实际评分，N 是测试样本数量。

2. **在推荐系统中的应用**：MAE 是推荐系统评估的标准做法，被广泛用于比较不同推荐算法的预测准确性。[[Item-Based Collaborative Filtering Recommendation Algorithms]] 采用 MAE 作为主要评估指标，比较 [[基于物品的协同过滤|Item-Based CF]] 与 [[基于用户的协同过滤|User-Based CF]] 的推荐质量。

3. **实验结论**：在 [[MovieLens]] 100K 数据集上，[[基于物品的协同过滤|Item-Based CF]] 使用调整后余弦相似度时 MAE 最低，显著优于基本余弦相似度和皮尔逊相关系数，且优于或等同于最优的 [[基于用户的协同过滤|User-Based CF]] 方法。

4. **与其他指标的关系**：MAE 衡量的是预测值与真实值的平均偏差，对异常值不敏感（相比均方误差 MSE）。在推荐系统中，MAE 的降低直接对应推荐质量的提升。

5. **局限性**：MAE 只衡量评分预测的准确性，不直接反映推荐结果的相关性、多样性或用户满意度。现代推荐系统评估还引入了 Precision@K、[[NDCG]]、覆盖率等更多维度的指标。

## 来源
- [[Item-Based Collaborative Filtering Recommendation Algorithms]] — 第 7.2 节

## 相关
- [[基于物品的协同过滤]] — uses
- [[Item-Based Collaborative Filtering Recommendation Algorithms]] — uses
- [[MovieLens]] — uses
