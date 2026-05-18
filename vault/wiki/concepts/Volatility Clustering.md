---
type: concept
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [finance, econometrics, volatility-modeling, time-series, 经济学]
aliases: ["Volatility Clustering", "波动聚集效应", "波动率聚集"]
relates_to:
  - target: "[[GARCH Model]]"
    type: modeled_by
    confidence: 0.9
  - target: "[[ARCH Model]]"
    type: modeled_by
    confidence: 0.8
  - target: "[[Financial Markets]]"
    type: observed_in
    confidence: 0.9
  - target: "[[Time Series Analysis]]"
    type: part_of
    confidence: 0.7
supersedes: null
---

# Volatility Clustering

## 概述
波动率聚集（Volatility Clustering）是指在金融[[Time Series Analysis|时间序列]]中，高波动率时期往往会聚集在一起，低波动率时期也会聚集在一起的现象，即波动率具有时变性和持续性。

## 关键内容
1. **现象描述**：金融市场的波动率具有明显的聚集性特征：一次剧烈的价格震荡发生后，市场不会在第二天就恢复风平浪静，而是在此后相当长的时间内持续保持较高的波动水平，然后才慢慢平息。这就像往湖面扔石头后，波纹会持续一段时间才完全消失。

2. **经济意义**：这种现象反映了金融市场信息冲击的持续影响，表明市场对新信息的消化需要一定时间，而不是瞬时完成的。

3. **建模需求**：波动率聚集现象促使了[[AR 模型（自回归模型）|自回归]][[Conditional Heteroskedasticity|条件异方差]]（ARCH）模型和广义[[AR 模型（自回归模型）|自回归]][[Conditional Heteroskedasticity|条件异方差]]（GARCH）模型的发展，这些模型为波动率的时变特征提供了数学框架。

4. **观察实例**：在股票收益率、汇率变动、商品价格等金融[[Time Series Analysis|时间序列]]中都能观察到明显的波动率聚集现象。

## 来源
- [[09-bollerslev-1986-garch.md]] — 对该现象的详细描述及其在GARCH模型发展中的作用

## 相关
- [[GARCH Model]] — 用于建模此现象
- [[ARCH Model]] — 早期建模方法
- [[Financial Markets]] — 现象发生的场所
- [[Time Series Analysis]] — 分析方法所在领域