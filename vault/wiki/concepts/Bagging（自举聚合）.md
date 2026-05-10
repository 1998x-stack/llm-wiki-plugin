---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "集成学习", "重采样"]
aliases: ["Bagging", "Bootstrap Aggregating", "自举聚合", "自助法聚合"]
relates_to: ["随机森林（Random Forests）", "决策树（Decision Tree）", "袋外误差（Out-of-Bag Error）", "偏差-方差分解"]
supersedes: null
---

# Bagging（自举聚合）

## 概述 (50-200字符)
一种[[模型融合|集成学习]]技术，通过对训练集有放回随机抽样生成多个子集，在每个子集上训练独立模型，最终通过投票或平均聚合预测结果以降低方差。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[算法]]流程**：给定训练集 D（N 个样本），有放回随机抽样 T 次，每次抽取 N 个样本生成子集 Dᵢ。在每个 Dᵢ 上训练一个完整模型 hᵢ。集成预测时，分类任务采用多数投票 ŷ = mode{h₁(x), ..., hₜ(x)}，回归任务采用平均值 ŷ = mean{h₁(x), ..., hₜ(x)}。
2. **63.2% 数学原理**：有放回抽样 N 次，某样本不被抽中的概率为 (1-1/N)^N → 1/e ≈ 36.8%，因此每个子集约含 63.2% 的唯一样本。未被抽中的 36.8% 样本称为袋外（OOB）样本，可直接用作验证集。
3. **方差降低机制**：Bagging 特别适用于高方差、低偏差的模型（如完整生长的[[决策树（Decision Tree）]]）。通过平均多个独立训练的模型，集成方差 = ρ·σ² + (1-ρ)/T · σ²，当 T → ∞ 时方差下限由树间相关性 ρ 决定。
4. **局限性**：若存在某个极强特征，每棵树都会在根节点选择它，导致树高度相关，集成收益有限。这正是 [[随机森林（Random Forests）]] 引入随机特征子集的原因。

## 来源
- [Breiman, L. (2001). Random forests. Machine learning, 45(1), 5–32.] — 随机森林论文中作为基础技术回顾

## 相关
- [[随机森林（Random Forests）]] — extends
- [[决策树（Decision Tree）]] — uses
- [[袋外误差（Out-of-Bag Error）]] — enables
- [[偏差-方差分解]] — implements
- [[Leo Breiman]] — created_by
