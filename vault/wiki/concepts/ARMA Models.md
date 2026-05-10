---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [time-series-analysis, statistics, mathematical-models]
aliases: ["ARMA Models", "自回归移动平均模型", "Autoregressive Moving Average Models"]
relates_to:
  - target: "[[Wold Decomposition Theorem]]"
    type: theoretical_foundation
    confidence: 0.9
  - target: "[[ARIMA Models]]"
    type: basis_for
    confidence: 0.85
  - target: "[[Time Series Analysis]]"
    type: important_model_class
    confidence: 0.85
supersedes: null
---

# ARMA Models

## 概述
ARMA（[[AR 模型（自回归模型）|自回归]]移动平均）模型是[[时间序列分析]]中的一种统计模型，结合了[[AR 模型（自回归模型）|自回归]]（AR）部分和移动平均（MA）部分，用于描述[[Stationary Time Series|平稳时间序列]]的行为。

## 关键内容
1. **模型结构**：
   - 模型形式：$X_t = \phi_1 X_{t-1} + \cdots + \phi_p X_{t-p} + \varepsilon_t + \theta_1 \varepsilon_{t-1} + \cdots + \theta_q \varepsilon_{t-q}$
   - AR部分（[[AR 模型（自回归模型）|自回归]]）：用过去的观测值来预测当前值
   - MA部分（移动平均）：用过去的随机冲击来修正预测

2. **理论基础**：
   - 理论根基直接来自Wold分解定理
   - 如果一个因果可逆的ARMA过程是平稳的，其AR部分可以展开为无穷阶的MA过程
   - 这恰好与Wold分解定理保证的MA(∞)形式相一致

3. **重要意义**：
   - 为[[Stationary Time Series|平稳时间序列]]建模提供了有效工具
   - 是更广泛的[[ARIMA|ARIMA模型]]的基础
   - 在经济、金融、工程等领域广泛应用

## 来源
- [[Wold Decomposition Theorem]] — 理论基础与Wold定理的联系

## 相关
- [[Wold Decomposition Theorem]] — theoretical_foundation
- [[ARIMA Models]] — basis_for
- [[Time Series Analysis]] — important_model_class