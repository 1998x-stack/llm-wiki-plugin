---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 评估指标, 机器学习]
aliases: [RMSE, Root Mean Square Error, 均方根误差]
relates_to:
  - {target: Netflix Prize, type: part_of}
  - {target: 矩阵分解, type: compares_to}
  - {target: 平均绝对误差 MAE, type: compares_to}
supersedes: null
---

# RMSE

## 概述
均方根误差，推荐系统评分预测任务的核心评估指标，[[Netflix Prize]] 竞赛的官方评判标准。

## 关键内容

1. **定义**：RMSE（Root Mean Square Error）衡量预测评分与真实评分之间的偏差，[[计算]]公式为 $\sqrt{\frac{1}{N}\sum(r_{ui} - \hat{r}_{ui})^2}$。值越小表示预测越准确。
2. **[[Netflix Prize]] 基线**：[[Cinematch]] 基线 RMSE 为 0.9514，竞赛目标为降至 0.8563 以下（10% 提升）。最终 [[BellKor's Pragmatic Chaos]] 以 0.8567（10.06% 提升）获胜。
3. **各方法 RMSE 对比**：
   - [[FunkSVD]]: ~0.896（~5.9% 提升）
   - SVD (100 factors): 0.9025（~5.1% 提升）
   - [[SVD++]] (100 factors): 0.8924（~6.2% 提升）
   - [[timeSVD++]] (10 factors): < 0.8924（> 6.2% 提升）
4. **局限性**：RMSE 优化评分预测精度，但不直接等价于推荐列表的排序质量。后来的研究逐渐转向 NDCG、MAP、AUC 等排序指标。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Netflix Prize]] — 使用 RMSE 作为评判标准
- [[矩阵分解]] — 优化的目标指标
- [[平均绝对误差 MAE]] — 另一种评估指标
