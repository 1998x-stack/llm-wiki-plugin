---
type: concept
status: active
confidence: 0.75
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [时间序列分析, 预测方法, 统计模型, 时间序列]
aliases: ["ARIMA模型", "自回归积分滑动平均模型", "Autoregressive Integrated Moving Average"]
relates_to:
  - target: "[[指数平滑]]"
    type: compares_to
  - target: "[[Box-Jenkins方法]]"
    type: implements
  - target: "[[ETS框架]]"
    type: relates_to
  - target: "[[George Box]]"
    type: implements
  - target: "[[Gwilym Jenkins]]"
    type: implements
  - target: "[[State-Space Model]]"
    type: equivalent_representation
    confidence: 0.7
  - target: "[[Kalman Filter]]"
    type: algorithmic_solution_for_state_space
    confidence: 0.7
supersedes: null
---

# ARIMA

## 概述
ARIMA（Autoregressive Integrated Moving Average，[[AR 模型（自回归模型）|自回归]]积分滑动平均）模型是由Box和Jenkins在1970年系统化的[[Time Series Analysis|时间序列]]预测模型，与[[指数平滑]]方法平行发展，在学术界曾被认为更加"严谨"。

## 关键内容

1. **历史发展**：由[[George Box]]和[[Gwilym Jenkins]]在1970年系统化，形成了著名的Box-Jenkins方法论，是[[时间序列分析]]的重要分支。

2. **模型组成**：
   - AR（[[AR 模型（自回归模型）|自回归]]）：利用序列自身的滞后值作为回归变量
   - I（积分）：通过差分使非平稳序列变为平稳
   - MA（滑动平均）：利用过去的误差项进行建模

3. **参数结构**：ARIMA(p,d,q)模型包含三个参数，分别代表[[AR 模型（自回归模型）|自回归]]阶数、差分次数和移动平均阶数。

4. **学术地位**：很长一段时间里，学术界认为ARIMA比[[指数平滑]]更"严谨"，因为它有完整的统计理论支撑。

5. **与[[指数平滑]]的关系**：某些[[指数平滑]]模型恰好等价于特定的ARIMA模型（例如[[简单指数平滑]]等价于ARIMA(0,1,1)）。

6. **[[ETS框架]]的统一**：Rob Hyndman的[[ETS框架]]揭示了[[指数平滑]]与ARIMA的深层联系，实现了两种方法的理论统一。

7. **实际应用**：虽然理论上更完备，但在实际预测竞赛（如M3、M4）中，ARIMA的表现并不总是优于[[指数平滑]]方法。

## 来源
- [[03-holt-1957-exponential-smoothing]] — 与指数平滑的关系
- [[Box-Jenkins方法]] — 相关概念
- [[指数平滑]] — 相关概念

## 相关
- [[指数平滑]] — compares_to
- [[Box-Jenkins方法]] — implements
- [[ETS框架]] — relates_to
- [[George Box]] — relates_to
- [[Gwilym Jenkins]] — relates_to