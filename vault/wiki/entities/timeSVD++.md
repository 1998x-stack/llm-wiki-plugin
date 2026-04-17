---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, 时间动态]
aliases: [timeSVD++]
relates_to:
  - {target: SVD++, type: extends}
  - {target: 矩阵分解, type: implements}
  - {target: 隐式反馈, type: uses}
supersedes: null
---

# timeSVD++

## 概述
[[矩阵分解]]的时间动态扩展模型，将用户偏好的时间演化纳入建模，10 维 time[[SVD++]] 精度超过 200 维标准 SVD。

## 关键内容

1. **核心创新**：将 bias 和用户因子都变为时间的函数：
   - $b_i(t)$：物品偏置随时间变化（如电影刚上映时评分较高，后来逐渐回落）
   - $b_u(t)$：用户偏置随时间变化（包括长期漂移和日特定波动）
   - $p_u(t)$：用户隐因子向量随时间变化（品味的演化）
2. **静态假设**：物品的隐因子 $q_i$ 不随时间变化，因为物品本身是静态的。
3. **效果**：一个仅 10 维的 time[[SVD++]] 模型，精度就超过了 200 维的标准 SVD 模型。Koren 总结："正确处理时间动态对精度的影响，大于设计更复杂的推荐架构。"
4. **公式**：$\hat{r}_{ui}(t) = \mu + b_i(t) + b_u(t) + q_i^T \cdot (p_u(t) + |R(u)|^{-1/2} \sum_{j \in R(u)} y_j)$
5. **后续影响**：为[[序列推荐]]、[[会话推荐]]等研究方向埋下了种子。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[SVD++]] — 基础模型
- [[矩阵分解]] — 方法论类别
- [[Yehuda Koren]] — 提出者
