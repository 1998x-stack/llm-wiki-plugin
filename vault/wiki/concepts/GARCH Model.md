---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [finance, econometrics, volatility-modeling, time-series, garch]
aliases: ["Generalized Autoregressive Conditional Heteroskedasticity", "广义自回归条件异方差模型"]
relates_to:
  - target: "[[ARCH Model]]"
    type: extends
    confidence: 0.9
  - target: "[[Tim Bollerslev]]"
    type: created_by
    confidence: 1.0
  - target: "[[Volatility Clustering]]"
    type: models
    confidence: 0.9
  - target: "[[Time Series Analysis]]"
    type: part_of
    confidence: 0.8
  - target: "[[Robert Engle]]"
    type: inspired_by
    confidence: 0.8
supersedes: null
---

# GARCH Model

## 概述
GARCH（Generalized Autoregressive Conditional Heteroskedasticity，广义自回归条件异方差）模型是由 Tim Bollerslev 在1986年提出的金融计量经济学模型，用于刻画时间序列数据中的波动率聚集现象，是对 Engle 提出的 ARCH 模型的重要推广。

## 关键内容
1. **核心创新**：GARCH 模型在条件方差的等式中加入了方差自身的滞后值，使得模型仅需少数几个参数就能捕捉波动率的长期持续性。经典的 GARCH(1,1) 模型形式为：
   σ²ₜ = ω + αε²ₜ₋₁ + βσ²ₜ₋₁
   其中 ω（常数项）、α（对最近冲击的反应系数）、β（波动率的持续性系数）为三个待估参数。

2. **与 ARCH 的关系**：GARCH 解决了 ARCH 模型的"参数诅咒"问题，即要刻画波动率的长期持续性需要大量的参数。GARCH 通过引入方差自身的滞后项，用少量参数实现了对无限阶 ARCH 模型的近似。

3. **模型类比**：正如 ARMA 之于 MA，GARCH 之于 ARCH，通过加入自身滞后值大幅减少了所需的参数量，同时保持了对波动率动态特征的刻画能力。

4. **实证优势**：Bollerslev 在论文中使用英国季度通胀率数据展示了 GARCH 的优越性。一个简单的 GARCH(1,1) 模型（仅3个参数）就能达到与需要5个方差参数的 ARCH(4) 模型相当甚至更优的拟合效果。

5. **实际应用**：GARCH 模型在金融实践中有着深远影响，广泛应用于波动率预测、风险管理（如VaR计算）、期权定价和宏观经济预测等领域。

## 来源
- [[09-bollerslev-1986-garch.md]] — Bollerslev 原始论文的详细介绍

## 相关
- [[ARCH Model]] — 扩展
- [[Tim Bollerslev]] — 创建者
- [[Volatility Clustering]] — 建模对象
- [[Time Series Analysis]] — 所属领域
- [[Robert Engle]] — 启发来源