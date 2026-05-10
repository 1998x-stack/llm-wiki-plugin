---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 排序学习, 机器学习]
aliases: [Pairwise Learning, Pairwise 方法, 成对学习]
relates_to:
  - {target: Pointwise 学习, type: compares_to}
  - {target: BPR, type: implements}
  - {target: AUC, type: relates_to}
supersedes: null
---

# Pairwise 学习

## 概述
一种机器学习训练[[规范化理论|范式]]，通过比较样本对之间的相对关系而非预测单个样本的绝对值来进行模型优化。

## 关键内容

1. **与 Pointwise 的对比**：[[Pointwise 学习|Pointwise 方法]]逐个预测 (user, item) 对的绝对分数/概率，优化 MSE 或[[交叉熵]]；Pairwise 方法以三元组 (user, item_i, item_j) 为训练单元，预测两个物品的相对排序，优化 log-sigmoid 等排序损失。

2. **在推荐系统中的优势**：推荐系统的最终输出是有序列表而非分数集合，pairwise 方法直接优化排序质量，与最终评价指标（AUC/NDCG）一致，避免了训练目标与评估目标不匹配的问题。

3. **对缺失数据的处理**：[[Pointwise 学习|Pointwise 方法]]需将未交互物品标记为 0 或忽略，存在建模错误；Pairwise 方法只假设正样本排在未观测数据前面，不对未观测物品之间的相对顺序做假设，遵循最小假设原则。

4. **BPR 中的实现**：BPR-Opt = Σ_(u,i,j) ln σ(x̂_ui - x̂_ui) - λ‖Θ‖²，通过 logistic sigmoid 函数建模偏好概率，是 AUC 的可微光滑近似。

5. **与 Listwise 的比较**：Pairwise 每次只比较两个物品，无法建模全局排序意图；Listwise 方法（如 [[Softmax]] [[交叉熵]]）考虑整个物品列表，在 NDCG、MRR 等指标上提供更紧的下界，但[[计算]]复杂度更高。

6. **在信息检索中的先例**：Pairwise 排序学习在信息检索领域（[[学习排序|Learning to Rank]]）已有先例，如 RankNet、LambdaRank，BPR 是第一个将其系统化应用于推荐系统[[隐式反馈]]场景的工作。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, pairwise 范式确立

## 相关
- [[Pointwise 学习]] — compares_to
- BPR — implements
- AUC — relates_to
