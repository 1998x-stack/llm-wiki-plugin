---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [机器学习, 排序学习, 推荐系统]
aliases: [Pointwise Method, Pointwise 方法, 单点学习]
relates_to:
  - {target: Pairwise 学习, type: compares_to}
  - {target: 隐式反馈, type: relates_to}
  - {target: BPR, type: contradicts}
supersedes: null
---

# Pointwise 学习

## 概述
一种逐个预测单个样本绝对分数或概率的机器学习训练[[规范化理论|范式]]，在推荐系统中用于预测用户对物品的评分或交互概率。

## 关键内容

1. **基本方法**：以单个 (user, item) 对为训练单元，预测用户 u 对物品 i 的绝对评分 x̂_ui 或交互概率 p(y_ui = 1)，常用损失函数包括均方误差 MSE 和[[交叉熵]] Cross-entropy。

2. **在[[隐式反馈]]中的问题**：
   - **方法一**：将交互物品标记为 1、未交互物品标记为 0，用 MSE 回归优化。问题在于未交互物品是缺失数据而非真正负样本。
   - **方法二**：只使用观测到的正样本训练。问题在于模型无法学到有用信息，最优解退化为对所有物品给出相同预测值。

3. **与 Pairwise 的对比**：
   | 维度 | Pointwise | Pairwise (BPR) |
   |------|-----------|----------------|
   | 训练单元 | 单个 (user, item) 对 | 三元组 (user, item_i, item_j) |
   | 优化目标 | 预测绝对分数/概率 | 预测相对排序 |
   | 损失函数 | MSE, Cross-entropy | BPR-OPT (log-sigmoid) |
   | 对缺失数据的处理 | 标记为 0 或忽略 | 只假设正样本排在缺失数据前面 |
   | 与最终评价指标的关系 | 间接 | 直接优化 AUC |

4. **[[WR-MF]] 的尝试**：Hu et al. (2008) 提出的 Weighted Regularized MF 为未交互物品分配较低但非零的置信度，虽针对[[隐式反馈]]设计，但仍在 pointwise 层面优化，排序质量不如 BPR-MF。

5. **训练目标与评估目标的不匹配**：用 MSE 训练的模型最终却用 AUC/NDCG 评估，这种 mismatch 必然导致次优结果。BPR 通过直接优化与 AUC 等价的目标函数消除了这种不一致。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, 现有方法的根本性错误分析

## 相关
- [[Pairwise 学习]] — compares_to
- [[隐式反馈]] — relates_to
- BPR — contradicts
