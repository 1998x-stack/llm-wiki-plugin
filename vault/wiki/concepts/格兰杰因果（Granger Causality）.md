---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["Granger Causality", "格兰杰因果检验", "预测因果性"]
relates_to:
  - target: "[[AR 模型（自回归模型）]]"
    type: depends_on
    confidence: 0.9
  - target: "[[因果推断]]"
    type: compares_to
    confidence: 0.85
  - target: "[[协整分析]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# 格兰杰因果（Granger Causality）

## 概述
Granger 因果检验由 [[Clive Granger]] 于 1969 年提出，用"X 的过去值是否能帮助预测 Y"来定义[[Time Series Analysis|时间序列]]间的预测性因果关系，是计量经济学中因果分析的核心工具之一，也是 Granger 获得 2003 年诺贝尔经济学奖的核心贡献。

## 关键内容

1. **历史背景**：1960 年代计量经济学面临因果难题——联立方程模型预先假定因果方向，数据无法纠正错误假设。Granger 注意到因果关系中一个被忽视的维度：时间。原因必须发生在结果之前。

2. **核心定义**：如果在包含 X 和 Y 过去值的信息集下，对 Y 的预测精度显著高于仅用 Y 过去值的预测精度，则称 X Granger-cause Y。这是基于预测能力的因果定义，而非哲学意义上的因果性。

3. **检验方法**：通过比较受限模型（仅用 Y 的过去值）和非受限模型（同时用 X 和 Y 的过去值）的预测误差，用 F 检验判断 X 的系数是否联合显著不为零。

4. **局限性**：Granger 因果不等于真正的因果关系——可能存在隐藏的第三变量同时驱动两者。但它提供了一个可操作的、可用数据检验的因果性定义。

## 来源
- [[05-granger-1969-causality]] — 谁是因，谁是果？一位经济学家用"预测"重新定义了因果关系

## 相关
- [[AR 模型（自回归模型）]] — depends_on
- [[因果推断]] — compares_to
- [[协整分析]] — relates_to
