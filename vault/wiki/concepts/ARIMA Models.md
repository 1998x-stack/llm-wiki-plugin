---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [time-series-analysis, statistics, mathematical-models, 时间序列]
aliases: ["ARIMA Models", "差分整合移动自回归模型", "Autoregressive Integrated Moving Average Models"]
relates_to:
  - target: "[[ARMA Models]]"
    type: extension_of
    confidence: 0.85
  - target: "[[Box-Jenkins Methodology]]"
    type: methodology_for
    confidence: 0.9
  - target: "[[Wold Decomposition Theorem]]"
    type: theoretical_foundation
    confidence: 0.85
  - target: "[[State-Space Model]]"
    type: equivalent_representation
    confidence: 0.7
  - target: "[[Kalman Filter]]"
    type: algorithmic_solution_for_state_space
    confidence: 0.7
supersedes: null
---

# ARIMA Models

## 概述
[[ARIMA]]（差分整合移动[[AR 模型（自回归模型）|自回归]]）模型是[[时间序列分析]]中的一类重要统计模型，是ARMA模型的扩展，能够处理非[[Stationary Time Series|平稳时间序列]]数据。

## 关键内容
1. **模型组成**：
   - AR部分（[[AR 模型（自回归模型）|自回归]]）：使用[[Time Series Analysis|时间序列]]的滞后值作为预测因子
   - I部分（整合/差分）：通过差分操作将非平稳序列转换为平稳序列
   - MA部分（移动平均）：使用预测误差的滞后值作为线性组合

2. **理论联系**：
   - 理论基础直接来源于Wold分解定理
   - Box与Jenkins发展的系统化[[ARIMA]]建模方法论成为[[时间序列分析]]的标准[[规范化理论|范式]]
   - 整套方法的数学根基可追溯到Wold在1938年证明的定理

3. **应用价值**：
   - 在经济计量学中广泛应用于[[宏观经济数据|宏观经济指标]]预测
   - 在金融领域用于风险管理和投资决策
   - 是[[Time Series Analysis|时间序列]]预测中最常用的模型之一

## 来源
- [[Box-Jenkins Methodology]] — 理论发展与Wold定理的关系

## 相关
- [[ARMA Models]] — extension_of
- [[Box-Jenkins Methodology]] — methodology_for
- [[Wold Decomposition Theorem]] — theoretical_foundation