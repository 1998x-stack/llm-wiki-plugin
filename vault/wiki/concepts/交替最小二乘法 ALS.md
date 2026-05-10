---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 矩阵分解, 优化算法]
aliases: [交替最小二乘法, ALS, Alternating Least Squares]
relates_to:
  - {target: 矩阵分解, type: uses}
  - {target: Apache Spark MLlib, type: implements}
  - {target: 隐式反馈, type: uses}
supersedes: null
---

# 交替最小二乘法 ALS

## 概述
[[矩阵分解]]的优化方法之一，交替固定用户[[矩阵]]或物品[[矩阵]]，将非凸问题转化为可精确求解的二次优化子问题。

## 关键内容

1. **核心思想**：交替固定 $P$ 和 $Q$ 中的一个，将问题转化为二次优化问题求解另一个。固定 $Q$ 时，每个用户的 $p_u$ 可以独立求解；固定 $P$ 时同理。
2. **三大优势**：
   - 每一步的子问题可以精确求解（闭式解）
   - 天然适合并行化（固定 $Q$ 时每个用户的 $p_u$ 可独立求解）
   - 适合处理[[隐式反馈]]数据（此时训练数据不再稀疏）
3. **与 SGD 对比**：SGD 实现简单、收敛速度快、内存占用小；ALS 每步精确求解、适合并行、适合[[隐式反馈]]。两者是[[矩阵分解]]的两大主流优化方法。
4. **工业应用**：ALS 优化的[[矩阵分解]]成为了 [[Apache Spark MLlib]] 等大数据框架的标准推荐[[算法]]实现，因其分布式友好特性被大量企业采用。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[矩阵分解]] — ALS 优化的目标模型
- [[Apache Spark MLlib]] — ALS 的工业实现
- [[隐式反馈]] — ALS 特别适合处理的信号类型
