---
type: entity
entity_type: paper
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 隐式反馈, 矩阵分解]
aliases: [WR-MF, Weighted Regularized Matrix Factorization, 加权正则化矩阵分解]
relates_to:
  - {target: 隐式反馈, type: relates_to}
  - {target: 矩阵分解, type: extends}
  - {target: BPR, type: compares_to}
  - {target: Hu Yifan, type: implements}
  - {target: Pointwise 学习, type: implements}
supersedes: null
---

# WR-MF

## 概述
Weighted Regularized [[矩阵分解|Matrix Factorization]]，Hu et al. (2008) 提出的处理[[隐式反馈]]的[[矩阵分解]]方法，在[[BPR]]论文中作为重要的对比基线方法，通过为未交互物品分配较低但非零的置信度来处理[[隐式反馈]]。

## 关键内容

1. **设计思想**：针对[[隐式反馈]]数据中缺失值问题，WR-MF 不像传统方法那样将未交互物品标记为0（负样本），而是为它们分配较低但非零的置信度，试图在 pointwise 层面优化模型。

2. **优化策略**：采用加权正则化的[[矩阵分解]]方法，对观测到的交互（正样本）赋予较高权重，对未观测到的交互（潜在负样本）赋予较低权重，但仍参与优化过程。

3. **与 BPR 的对比**：虽然 WR-MF 针对[[隐式反馈]]设计，但仍在 pointwise 层面进行优化，即逐个预测用户对物品的偏好分数。相比之下，[[BPR]] 采用 pairwise 优化准则，直接学习物品间的相对排序关系。

4. **实验结果**：[[BPR 论文]]实验表明，尽管 WR-MF 针对[[隐式反馈]]进行了专门设计，但其排序性能（AUC指标）仍不如使用 pairwise 优化的 BPR-MF，验证了优化准则对预测质量的重要性。

5. **历史意义**：作为从[[显式反馈]][[矩阵分解]]向[[隐式反馈]]推荐过渡的重要方法之一，WR-MF 体现了业界对[[隐式反馈]]处理的早期探索，但其 pointwise 优化[[规范化理论|范式]]被后续的 pairwise（BPR）和 listwise 方法所超越。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI，WR-MF 作为重要对比方法
- Hu, Yifan, et al. (2008). Collaborative Filtering for Implicit Feedback Datasets. ICDM 2008

## 相关
- [[隐式反馈]] — relates_to
- [[矩阵分解]] — extends
- [[BPR]] — compares_to
- [[Pointwise 学习]] — implements
- [[Hu Yifan]] — part_of