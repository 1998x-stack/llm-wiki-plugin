---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, 分解模型, 标签推荐]
aliases: [PITF, Pairwise Interaction Tensor Factorization]
relates_to: 
  - target: "[[Steffen Rendle]]"
    type: authored_by
    confidence: 0.8
  - target: "[[Factorization Machines]]"
    type: predecessor_to
    confidence: 0.8
  - target: "[[矩阵分解]]"
    type: extends
    confidence: 0.7
supersedes: null
entity_type: paper
---

# PITF

## 概述
Pairwise Interaction Tensor Factorization，由 Steffen Rendle 与 Schmidt-Thieme 合作提出的针对标签推荐任务的成对交互张量分解模型，可被FM框架等价表示。

## 关键内容

1. **任务针对性**：
   专门针对标签推荐任务设计，处理用户-物品-标签三元交互问题。

2. **张量分解**：
   使用张量分解方法建模三元组（用户、物品、标签）之间的复杂交互关系。

3. **与FM的关系**：
   在FM框架下，只需将用户、物品、标签分别编码为one-hot向量并拼接，FM的交叉项会自动产生三组成对交互，与PITF模型方程完全一致。

## 来源
- [[推荐系统/06-factorization-machines.md]] — 5.4 与MF/SVD++/PITF的等价关系

## 相关
- [[Steffen Rendle]] — authored_by
- [[Factorization Machines]] — predecessor_to
- [[矩阵分解]] — extends