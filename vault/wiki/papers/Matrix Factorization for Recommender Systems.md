---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [推荐系统, 矩阵分解, Netflix Prize, 机器学习]
aliases: ["Matrix Factorization Techniques for Recommender Systems", "MF", "SVD++", "Netflix Prize"]
relates_to:
  - target: "[[Yehuda Koren]]"
    type: authored_by
  - target: "[[Netflix Prize]]"
    type: part_of
  - target: "[[矩阵分解]]"
    type: implements
  - target: "[[Embedding]]"
    type: implements
---

# Matrix Factorization for Recommender Systems

## 概述
Netflix Prize 获胜团队的核心论文（IEEE Computer 2009），将推荐系统从启发式工程升级为可优化的机器学习问题，提出用隐向量（Embedding）表示用户和物品，通过矩阵补全预测评分，是推荐系统领域最高被引论文之一（~12000+引用）。

## 关键内容

1. **核心问题**：矩阵补全——给定稀疏的用户-物品评分矩阵，补全所有缺失值

2. **隐因子模型**：
   - 用户 $u$ 的隐向量 $\vec{p}_u \in \mathbb{R}^k$
   - 物品 $i$ 的隐向量 $\vec{q}_i \in \mathbb{R}^k$
   - 预测评分：$\hat{r}_{u,i} = \vec{p}_u \cdot \vec{q}_i$

3. **完整模型（带偏差）**：
   - $\hat{r}_{u,i} = \mu + b_u + b_i + \vec{p}_u^T \vec{q}_i$
   - $\mu$：全局平均
   - $b_u$：用户偏差
   - $b_i$：物品偏差

4. **优化方法**：
   - **SGD**：随机梯度下降，适合流式学习
   - **ALS**：交替最小二乘，可并行化，工业大规模常用

5. **SVD++ 扩展**：
   - 融入隐式反馈（看过但未评分的物品）
   - 用户偏好 = 显式偏好 + 隐式行为推断

6. **Netflix Prize 结果**：
   - RMSE 从基线 0.9514 降至 0.8567（提升 10.06%）
   - 矩阵分解类模型贡献超过 7% 的提升

## 来源
- [[03_MatrixFactorization_Netflix_2009]] — 矩阵分解与 Netflix Prize：隐向量时代的到来

## 相关
- [[Yehuda Koren]] — authored_by
- [[Netflix Prize]] — part_of
- [[矩阵分解]] — implements
- [[Embedding]] — implements
- [[BPR]] — compares_to
