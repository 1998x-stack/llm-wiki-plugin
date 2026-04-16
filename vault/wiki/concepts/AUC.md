---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [评估指标, 排序, 推荐系统, 机器学习]
aliases: [Area Under ROC Curve, ROC 曲线下面积]
relates_to:
  - {target: BPR, type: relates_to}
  - {target: Pairwise 学习, type: relates_to}
  - {target: NDCG, type: compares_to}
supersedes: null
---

# AUC (Area Under ROC Curve)

## 概述
衡量分类器或排序模型区分正负样本能力的评估指标，在推荐系统中用于评价个性化排序质量。

## 关键内容

1. **定义**：AUC 等于随机选取一个正样本和一个负样本时，模型给正样本打分高于负样本的概率。AUC = 0.5 表示随机排序，AUC = 1.0 表示完美排序。

2. **在推荐系统中的计算**：对用户 u，AUC(u) = (1/|I_u^+| · |I \ I_u^+|) Σ_(i,j) δ(x̂_uij > 0)，其中 I_u^+ 为正样本集合，I \ I_u^+ 为负样本集合，δ 为指示函数。

3. **与 [[BPR]] 的关系**：[[BPR]]-OPT 是 AUC 的可微光滑近似，用 ln σ(x) 替代不可微的 Heaviside 阶跃函数 δ(x > 0)。优化 [[BPR]]-OPT 近似等价于直接优化 AUC。

4. **优势**：AUC 对类别不平衡不敏感，适合[[隐式反馈]]场景（正样本远少于负样本）；不依赖绝对阈值，只关注相对排序。

5. **局限性**：AUC 对所有负样本一视同仁，不考虑推荐列表顶部位置的权重；在实际推荐中，用户更关注 Top-K 推荐，此时 [[NDCG]]、[[MRR]] 等指标更合适。

6. **作为 [[BPR]] 实验的主要评价指标**：[[BPR 论文]]在 Rossmann 和 [[Netflix]] 数据集上以 AUC 为主要指标，证明 [[BPR]]-[[矩阵分解|MF]] 显著优于 [[奇异值分解|SVD]]-[[矩阵分解|MF]] 和 WR-[[矩阵分解|MF]]。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, AUC 与 BPR-OPT 关系分析

## 相关
- [[BPR]] — relates_to
- [[Pairwise 学习]] — relates_to
- [[NDCG]] — compares_to
