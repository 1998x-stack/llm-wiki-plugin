---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 马尔可夫链, 矩阵分解, RecSys]
aliases: [FPMC, Factorized Personalized Markov Chains]
relates_to:
  - {target: 序列推荐, type: implements}
  - {target: 马尔可夫链, type: uses}
  - {target: 矩阵分解, type: uses}
  - {target: SASRec, type: supersedes}
  - {target: FFM, type: compares_to}
supersedes: null
---

# FPMC

## 概述
Factorized Personalized [[马尔可夫链|Markov Chain]]s，结合[[马尔可夫链]]与[[矩阵分解]]的[[序列推荐]]方法，在稀疏数据上表现良好，但只能捕获最近一步行为，被 [[SASRec]] 全面超越。

## 关键内容

1. **核心方法**：将用户的下一个行为建模为两个部分的组合——（1）基于最近一个行为的[[马尔可夫链]]转移（个性化序列模式）；（2）用户-物品的全局偏好（[[矩阵分解]]）。通过分解转移张量实现高效计算。

2. **适用场景**：在数据极度稀疏的场景下表现良好，因为模型的简约性（parsimony）天然适合低数据量环境。在 [[Amazon]] Beauty 等极稀疏数据集上，FPMC 曾优于 [[GRU4Rec]] 等深度方法。

3. **根本局限**：只能看到"最近一步"，完全无法捕获用户的长期偏好模式。例如用户三个月前购买的相机与当前浏览的镜头配件之间的关联，FPMC 无法建模。

4. **与 [[SASRec]] 的关系**：[[SASRec]] 论文提供了一个优美的理论分析——当将[[Self-Attention机制|自注意力]]块设置为零（退化为恒等映射）、使用非共享物品嵌入、移除[[位置编码]]时，[[SASRec]] 退化为 FPMC。这说明 [[SASRec]] 是 FPMC 等经典模型的广义化。

5. **历史地位**：代表了[[马尔可夫链]]方法在[[序列推荐]]中的巅峰，后续被深度学习方法（[[GRU4Rec]]、[[SASRec]] 等）全面超越，但在稀疏数据场景下仍是一个有效的基线。

## 来源
- [FPMC 原始论文 (RecSys 2010)](https://dl.acm.org/doi/10.1145/1864708.1864721)

## 相关
- [[SASRec]] — 全面超越 FPMC，且可退化为其特例
- [[马尔可夫链]] — FPMC 的序列建模基础
- [[矩阵分解]] — FPMC 的全局偏好建模基础
- [[GRU4Rec]] — 在稀疏数据上 FPMC 曾优于 GRU4Rec
- [[序列推荐]] — FPMC 解决的核心场景
