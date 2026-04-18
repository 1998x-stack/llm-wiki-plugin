---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, 建模技术]
aliases: [Bias 建模, 偏置建模, Bias Model]
relates_to:
  - {target: 矩阵分解, type: part_of}
  - {target: SVD++, type: part_of}
  - {target: timeSVD++, type: part_of}
supersedes: null
---

# Bias 建模

## 概述
推荐系统中将评分信号分解为系统性偏差（全局均值、用户偏置、物品偏置）和用户-物品交互项的建模方法。

## 关键内容

1. **核心公式**：$\hat{r}_{ui} = \mu + b_u + b_i + q_i^T p_u$，其中 $\mu$ 为全局平均评分，$b_u$ 为用户偏置，$b_i$ 为物品偏置，$q_i^T p_u$ 为隐因子交互项。
2. **设计精妙性**：将评分信号分解为"与交互无关的部分"（bias）和"真正的交互部分"（$q_i^T p_u$），使得隐因子只需要建模最本质的用户-物品匹配，大大降低了学习难度。
3. **生动例子**：预测用户 Tom 对电影 Batman 的评分。全局均分 3.5，Tom 倾向于低 0.3（挑剔），Batman 倾向于高 0.2（好评）。仅用基线预测就能得到 $3.5 - 0.3 + 0.2 = 3.4$。
4. **实践意义**：在很多实际推荐系统中，仅用 $\mu + b_u + b_i$ 这个简单的基线模型就能解释 80% 以上的评分变异。先把简单的偏置项调好，往往能获得事半功倍的效果。
5. **正则化**：Bias 项也纳入正则化：$\lambda(\|p_u\|^2 + \|q_i\|^2 + b_u^2 + b_i^2)$，防止[[过拟合（Overfitting）|过拟合]]。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[矩阵分解]] — Bias 建模所属框架
- [[SVD++]] — 包含 Bias 的扩展模型
- [[timeSVD++]] — 包含时间动态 Bias 的扩展模型
