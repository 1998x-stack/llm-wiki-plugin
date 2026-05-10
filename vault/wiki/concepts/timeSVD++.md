---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 矩阵分解, 算法, 时间动态]
aliases: ["timeSVD++", "Time Dynamic SVD++", "时间动态 SVD++"]
relates_to: []
supersedes: null
---

# timeSVD++

## 概述
time[[SVD++]] 是 [[SVD++]] 模型的时间动态扩展版本，通过建模用户偏好和物品属性随时间的变化，显著提升了推荐系统的预测精度。

## 关键内容

1. **核心思想**：
   用户的品味会随时间变化，物品的受欢迎程度也会因时间而异。time[[SVD++]] 将时间作为一等公民纳入建模，将用户偏置、物品偏置和用户隐因子都建模为时间的函数。

2. **数学公式**：
   $$\hat{r}_{ui}(t) = \mu + b_i(t) + b_u(t) + q_i^T \cdot \left( p_u(t) + |R(u)|^{-1/2} \sum_{j \in R(u)} y_j \right)$$
   
   关键创新在于将 bias 和用户因子都变为时间的函数：
   - $b_i(t)$：物品偏置随时间变化
   - $b_u(t)$：用户偏置随时间变化（包括长期漂移和日特定波动）
   - $p_u(t)$：用户隐因子向量随时间变化（品味的演化）
   
   物品的隐因子 $q_i$ 保持静态不变。

3. **效果**：
   效果显著：一个仅 10 维的 time[[SVD++]] 模型，精度就超过了 200 维的标准 SVD 模型。正如 Koren 总结的："正确处理时间动态对精度的影响，大于设计更复杂的推荐架构。"

4. **重要观察**：
   - 物品隐因子 $q_i$ 不随时间变化，因为物品本身是静态的
   - 时间动态建模的重要性远超模型复杂度，体现了对数据特性深刻理解的价值

## 来源
- [[推荐系统/04-matrix-factorization-for-recsys.md]] — 详细介绍 timeSVD++ 模型
- [[]] — 

## 相关
- [[SVD++]] — 基础模型
- [[矩阵分解]] — 核心方法
- [[时间动态]] — 建模要素
- [[Matrix Factorization Techniques for Recommender Systems]] — 提出论文