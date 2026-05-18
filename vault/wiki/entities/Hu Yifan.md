---
type: entity
entity_type: person
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 矩阵分解, 隐式反馈, 协同过滤]
aliases: [Hu Yifan, 胡寅凡, Hu Yi-Fan]
relates_to:
  - {target: 隐式反馈, type: implements}
  - {target: WR-MF, type: implements}
  - {target: 矩阵分解, type: implements}
  - {target: 协同过滤, type: implements}
  - {target: BPR, type: compares_to}
supersedes: null
---

# Hu Yifan

## 概述
推荐系统领域研究者，因提出 [[WR-MF]]（[[WR-MF|Weighted Regularized Matrix Factorization]]）方法而知名，该方法在处理[[隐式反馈]]推荐问题方面做出了重要贡献，是BPR论文中的重要对比方法。

## 关键内容

1. **[[WR-MF]] 贡献**：在 ICDM 2008 上发表了 "[[协同过滤|Collaborative Filtering]] for [[隐式反馈|Implicit Feedback]] Datasets" 论文，提出了 [[WR-MF|Weighted Regularized Matrix Factorization]] 方法，针对[[隐式反馈]]数据中缺失值问题，为未交互物品分配较低但非零的置信度，以改进传统[[矩阵分解]]在[[隐式反馈]]场景中的应用。

2. **研究重点**：专注于[[协同过滤]]和[[隐式反馈]]推荐系统，致力于解决[[隐式反馈]]数据中的缺失值问题和如何有效利用用户行为数据进行个性化推荐。

3. **与 BPR 的关系**：Hu Yifan 提出的 [[WR-MF]] 方法成为 [[BPR 论文]]中的重要对比基线，[[BPR 论文]]表明尽管 [[WR-MF]] 针对[[隐式反馈]]进行了专门设计，但在排序性能上仍不如使用 pairwise 优化的 BPR-MF，验证了优化准则对预测质量的重要性。

4. **学术影响**：[[WR-MF]] 方法作为从[[显式反馈]][[矩阵分解]]向[[隐式反馈]]推荐过渡的重要方法之一，为后续研究奠定了基础，启发了后续更多针对[[隐式反馈]]推荐的研究工作。

## 来源
- Hu, Yifan, et al. (2008). Collaborative Filtering for Implicit Feedback Datasets. ICDM 2008
- [[BPR 论文]] — Rendle et al. (2009) UAI，WR-MF 作为重要对比方法

## 相关
- [[隐式反馈]] — implements
- [[WR-MF]] — 代表作
- [[矩阵分解]] — implements
- [[协同过滤]] — implements
- [[BPR]] — compares_to