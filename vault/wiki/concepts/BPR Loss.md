---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, 序列推荐, 损失函数]
aliases: ["Bayesian Personalized Ranking Loss", "BPR Loss", "贝叶斯个性化排序损失"]
relates_to:
  - target: "[[GRU4Rec]]"
    type: utilized_in
    confidence: 0.9
  - target: "[[TOP1 Loss]]"
    type: alternative_to
    confidence: 0.8
  - target: "[[排序优化]]"
    type: objective
    confidence: 0.8
  - target: "[[成对学习]]"
    type: paradigm
    confidence: 0.8
  - target: "[[Rendle等人]]"
    type: originally_developed_by
    confidence: 0.8
supersedes: null
---

# BPR Loss

## 概述
BPR Loss（[[BPR|Bayesian Personalized Ranking]] Loss）是一种用于个性化排序的成对损失函数，在[[GRU4Rec]]论文中被用于优化推荐系统的排序质量，强调正样本分数应高于负样本分数。

## 关键内容

1. **数学定义**：
   BPR损失的核心思想是优化正负样本之间的相对排序，公式为：L_BPR = -(1/N_S) * Σ log(σ(ȓ_i - ȓ_j))，其中ȓ_i是正样本（用户实际点击的物品）的分数，ȓ_j是负样本的分数，N_S是负样本数量。

2. **设计原理**：
   与传统分类任务的[[二元交叉熵|交叉熵损失]]不同，BPR Loss关注的是推荐问题的本质——排序而非分类。它通过最大化正样本与负样本分数之间的间隔来优化模型，符合推荐系统中"正确物品应排在前列"的目标。

3. **在[[GRU4Rec]]中的应用**：
   [[GRU4Rec]]论文比较了多种损失函数，发现BPR Loss在使用adagrad优化器时表现稳定，显著优于[[二元交叉熵|交叉熵损失]]。BPR Loss特别适合处理推荐中的[[隐式反馈]]数据。

## 来源
- [[12-gru4rec.md]] — 详细介绍

## 相关
- [[GRU4Rec]] — utilized_in
- [[TOP1 Loss]] — alternative_to
- [[排序优化]] — objective
- [[成对学习]] — paradigm
- [[Rendle等人]] — originally_developed_by