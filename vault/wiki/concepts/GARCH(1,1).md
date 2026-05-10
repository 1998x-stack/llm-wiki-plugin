---
type: concept
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [finance, econometrics, volatility-modeling, time-series]
aliases: ["GARCH(1,1)", "GARCH 1,1"]
relates_to:
  - target: "[[GARCH Model]]"
    type: part_of
    confidence: 1.0
  - target: "[[Volatility Clustering]]"
    type: models
    confidence: 0.9
  - target: "[[Tim Bollerslev]]"
    type: created_by
    confidence: 1.0
supersedes: null
---

# GARCH(1,1)

## 概述
GARCH(1,1) 是 GARCH 模型中最常用的具体形式，仅包含一个滞后项的自回归成分和一个滞后项的条件方差成分，用三个参数有效地刻画了波动率的动态特征。

## 关键内容
1. **数学表达式**：GARCH(1,1) 模型的标准形式为：
   σ²ₜ = ω + αε²ₜ₋₁ + βσ²ₜ₋₁
   其中，σ²ₜ 是 t 时刻的条件方差，ε²ₜ₋₁ 是前期的误差平方项，σ²ₜ₋₁ 是前期的条件方差项，ω、α、β 是三个待估参数。

2. **参数含义**：
   - ω（常数项）：表示最低水平的波动率
   - α（ARCH项系数）：衡量最近期冲击对当前波动率的影响程度
   - β（GARCH项系数）：衡量前期波动率水平对当前波动率的持续性影响

3. **递归结构优势**：由于包含方差自身的滞后项，GARCH(1,1) 具有递归结构，当前条件方差实际上隐含了所有历史误差平方的加权和，权重按几何级数衰减。

4. **实际应用**：在实证研究中，GARCH(1,1) 被证明通常是最佳选择，更高阶的 GARCH 模型很少能带来显著改进。估计结果中 α + β 通常接近于1，意味着波动率冲击的衰减速度极慢，很好地捕捉了金融数据中常见的"长记忆"特征。

## 来源
- [[09-bollerslev-1986-garch.md]] — Bollerslev 原始论文中对该模型的详细说明

## 相关
- [[GARCH Model]] — 隶属模型类
- [[Volatility Clustering]] — 建模对象
- [[Tim Bollerslev]] — 创建者