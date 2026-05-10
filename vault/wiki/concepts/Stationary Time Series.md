---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [time-series-analysis, statistics, probability-theory]
aliases: ["平稳时间序列", "Stationary Time Series", "Stationarity"]
relates_to:
  - target: "[[Wold Decomposition Theorem]]"
    type: decomposition_applied_to
    confidence: 0.9
  - target: "[[Time Series Analysis]]"
    type: subset_of_processes
    confidence: 0.8
  - target: "[[ARIMA Models]]"
    type: requirement_for_modeling
    confidence: 0.85
supersedes: null
---

# Stationary Time Series

## 概述
平稳[[Time Series Analysis|时间序列]]是指统计性质不随时间推移而改变的随机过程。其均值恒定，波动幅度恒定，任意两个时刻之间的相关性只取决于它们之间的时间间隔，而不取决于具体在哪个时刻观测。

## 关键内容
1. **定义特征**：
   - 均值恒定：序列的均值不随时间变化
   - 方差恒定：序列的波动幅度保持一致
   - 协方差仅依赖于时间间隔：任意两点间的相关性只与它们之间的时间距离有关，而与绝对时间无关

2. **重要意义**：
   - 平稳性是许多[[时间序列分析]]方法的前提假设
   - 为[[Time Series Analysis|时间序列]]建模提供了稳定的基础
   - Wold分解定理专门针对平稳[[Time Series Analysis|时间序列]]提出

3. **类型分类**：
   - 严平稳（Strict Stationarity）：所有统计特性都不随时间变化
   - 宽平稳（Weak/Covariance Stationarity）：仅要求均值、方差和协方差不随时间变化

## 来源
- [[Wold Decomposition Theorem]] — 定义和Wold分解的应用

## 相关
- [[Wold Decomposition Theorem]] — decomposition_applied_to
- [[Time Series Analysis]] — subset_of_processes
- [[ARIMA Models]] — requirement_for_modeling