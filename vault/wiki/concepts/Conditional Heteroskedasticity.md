---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [economics, finance, econometrics, volatility-modeling, 时间序列]
aliases: ["Generalized Autoregressive Conditional Heteroskedasticity", "条件异方差"]
relates_to:
  - target: "[[ARCH Model]]"
    type: extends
    confidence: 0.9
  - target: "[[Tim Bollerslev]]"
    type: developed_by
    confidence: 1.0
  - target: "[[Conditional Heteroskedasticity]]"
    type: generalization_of
    confidence: 0.9
  - target: "[[Time Series Analysis]]"
    type: part_of
    confidence: 0.8
supersedes: null
---

# Conditional Heteroskedasticity

## 概述
条件异方差（Conditional Heteroskedasticity）是指[[Time Series Analysis|时间序列]]数据的条件方差随时间变化的现象，其中 [[GARCH 模型]]是对其的广义化建模方法。

## 关键内容
1. **基本概念**：在传统的[[时间序列分析]]中，误差项通常假设为同方差（constant variance），但实际金融数据中经常观察到误差的方差随时间变化，这就是条件异方差现象。

2. **条件 vs 无条件**：无条件异方差关注的是整个序列的总体方差特征，而条件异方差关注的是在给定过去信息的条件下当前的方差。

3. **建模发展**：Engle 提出的 [[ARCH 模型]]首次为条件异方差提供了建模框架，而 Bollerslev 的 [[GARCH 模型]]进一步将其广义化，通过加入方差自身的滞后项解决了原模型的参数过多问题。

4. **实际意义**：条件异方差建模对于风险度量、资产定价和宏观经济分析具有重要意义，因为它能够捕捉到金融市场的不确定性是如何随时间演变的。

## 来源
- [[09-bollerslev-1986-garch.md]] — 介绍条件异方差的概念及其在GARCH模型中的应用

## 相关
- [[ARCH Model]] — 早期建模方法
- [[Tim Bollerslev]] — 广义化发展
- [[GARCH Model]] — 广义化建模方法
- [[Time Series Analysis]] — 所属领域