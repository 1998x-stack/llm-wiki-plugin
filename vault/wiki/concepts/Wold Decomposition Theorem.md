---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [time-series-analysis, statistics, probability-theory, mathematical-theorems, 时间序列]
aliases: ["Wold 分解定理", "Wold Decomposition Theorem", "Wold's Decomposition Theorem"]
relates_to:
  - target: "[[Herman Wold]]"
    type: proved_by
    confidence: 0.9
  - target: "[[Stationary Time Series]]"
    type: applies_to
    confidence: 0.9
  - target: "[[ARMA Models]]"
    type: theoretical_foundation_for
    confidence: 0.9
  - target: "[[ARIMA Models]]"
    type: theoretical_foundation_for
    confidence: 0.9
  - target: "[[Time Series Analysis]]"
    type: core_theorem_in
    confidence: 0.9
  - target: "[[Wold-Kolmogorov Prediction Theory]]"
    type: theoretical_basis_for
    confidence: 0.85
supersedes: null
---

# Wold Decomposition Theorem

## 概述
Wold分解定理是[[时间序列分析]]中的一个基本定理，由瑞典数学家[[Herman Wold]]于1938年在其博士论文中证明。该定理表明任何[[Stationary Time Series|平稳时间序列]]都可以唯一地分解为一个确定性部分和一个纯不确定性部分之和。

## 关键内容
1. **定理表述**：
   - 任何（离散、协方差）[[Stationary Time Series|平稳时间序列]] $X_t$，都可以**唯一地**分解为两个不相关的部分之和：$X_t = D_t + S_t$
   - $D_t$ 是**确定性分量**（deterministic component）——一个可以被自身过去的值完美预测的过程
   - $S_t$ 是**纯不确定性分量**（purely non-deterministic component）——它可以表示为一个无穷阶移动平均过程（MA(∞)）：$S_t = \sum_{j=0}^{\infty} b_j \, \varepsilon_{t-j}$

2. **理论意义**：
   - 为[[Stationary Time Series|平稳时间序列]]提供了统一的结构理解方式
   - 确定了任何平稳过程均由确定性和随机性两种成分构成
   - 为ARMA/[[ARIMA|ARIMA模型]]提供了理论合法性基础

3. **实际应用**：
   - Box-Jenkins方法论的理论基础
   - 信号处理与[[控制论视角|控制论]]中滤波技术的理论支撑
   - 计量经济学中宏观经济[[时间序列分析]]的基础
   - 金融数学中波动率建模的理论依据

## 来源
- [[Herman Wold]] — 证明和历史背景

## 相关
- [[Herman Wold]] — proved_by
- [[Stationary Time Series]] — applies_to
- [[ARMA Models]] — theoretical_foundation_for
- [[ARIMA Models]] — theoretical_foundation_for
- [[Time Series Analysis]] — core_theorem_in