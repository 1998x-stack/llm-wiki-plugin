---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [统计学, 因果推断, 缺失数据]
aliases: [Missing Completely At Random, MCAR]
relates_to:
  - {target: MNAR, type: compares_to}
  - {target: 矩阵分解, type: uses}
  - {target: 逆倾向评分, type: compares_to}
supersedes: null
---

# MCAR (完全随机缺失)

## 概述
完全随机缺失（Missing Completely At Random）指数据的缺失是完全随机的，每个数据点有相同概率被观测到，观测数据是全量数据的无偏子集。

## 关键内容

1. **定义**：在 MCAR 机制下，每个用户对每个物品的评分都有相同的概率被观测到，缺失完全是随机的。此时观测到的数据就是全量数据的一个无偏子集，可以放心地在上面训练和评估模型。

2. **与 [[MNAR]] 的对比**：[[MNAR]]（非随机缺失）下，某个评分是否被观测到与该评分的值本身高度相关。MCAR 是最理想的缺失机制，但现实中极少出现。

3. **在传统推荐系统中的隐式假设**：大量 [[矩阵分解]] 方法（如经典 [[奇异值分解|SVD]]、[[交替最小二乘法 ALS|ALS]] 等）直接在观测到的评分上最小化误差，隐式假设缺失数据是 MCAR 的。这一假设在推荐系统场景中通常不成立。

4. **与 [[逆倾向评分|IPS]] 的关系**：[[Tobias Schnabel]] 等人证明，当所有 [[倾向性评分]] 相等时（即 MCAR 情形），[[逆倾向评分|IPS]] 退化为传统的朴素估计器。这说明传统方法是 [[逆倾向评分|IPS]] 在 MCAR 特殊假设下的特例。

5. **随机对照实验**：在推荐系统中，通过随机强制曝光实验（如 [[Yahoo! R3]] 数据集的收集方式）可以近似实现 MCAR 条件，获得无偏的 ground truth 数据用于评估。

6. **现实中的不可达性**：真实的推荐系统数据几乎从不满足 MCAR 假设——用户的选择、系统的推荐策略、位置效应等都会导致非随机缺失。

## 来源
- [Recommendations as Treatments (Schnabel et al., ICML 2016)](https://arxiv.org/abs/1602.05352)

## 相关
- [[MNAR]] — 非随机缺失，MCAR 的现实对照
- [[矩阵分解]] — 传统方法隐式假设 MCAR
- [[逆倾向评分]] — 在 MCAR 下退化为朴素估计器
- [[Yahoo! R3]] — 通过随机实验近似 MCAR 的数据集
