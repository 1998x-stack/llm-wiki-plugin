---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["Cointegration", "协整检验", "Johansen 方法"]
relates_to:
  - target: "[[格兰杰因果（Granger Causality）]]"
    type: relates_to
    confidence: 0.85
  - target: "[[ARIMA 模型]]"
    type: compares_to
    confidence: 0.75
  - target: "[[误差修正模型]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# 协整分析（Cointegration）

## 概述
协整分析由 Engle 和 Granger（1987）正式定义，Johansen（1988）提出基于[[最大似然原理|最大似然估计]]的系统性框架，解决了非[[Stationary Time Series|平稳时间序列]]之间长期均衡关系的建模问题，是宏观计量经济学的核心工具。

## 关键内容

1. **历史背景**：1980 年代宏观经济学面临方法论危机——GDP、消费、物价等重要变量都是非平稳的，直接回归导致"[[伪回归]]"，差分又丢失长期水平关系信息。

2. **核心概念**：两个（或多个）单整变量的某种线性组合是平稳的。类比"醉汉与他的狗"——各自漫无目的地游走，但狗绳限制了它们之间的距离。

3. **Johansen 方法**：基于向量[[AR 模型（自回归模型）|自回归]]（VAR）的[[最大似然原理|最大似然估计]]框架，提供[[迹检验]]和[[最大特征值检验]]，可同时检测多个协整向量，克服了 Engle-Granger 两步法的局限。

4. **[[误差修正模型]]（ECM）**：[[协整 (Cointegration)|协整关系]]的直接推论——短期偏离均衡时，存在一种"纠错力"将系统拉回长期均衡路径。

## 来源
- [[10-johansen-1988-cointegration]] — 醉汉与他的狗：Johansen 如何重塑长期均衡分析

## 相关
- [[格兰杰因果（Granger Causality）]] — relates_to
- [[ARIMA 模型]] — compares_to
- [[误差修正模型]] — extends
