---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [statistics, mathematics, data-analysis]
aliases: ["Time Series Analysis", "时间序列分析", "时间序列"]
relates_to:
  - target: "[[Wold Decomposition Theorem]]"
    type: fundamental_theorem_in
    confidence: 0.9
  - target: "[[Stationary Time Series]]"
    type: core_concept_in
    confidence: 0.9
  - target: "[[ARMA Models]]"
    type: includes_model_class
    confidence: 0.9
  - target: "[[ARIMA Models]]"
    type: includes_model_class
    confidence: 0.9
  - target: "[[Box-Jenkins Methodology]]"
    type: standard_methodology
    confidence: 0.85
  - target: "[[Herman Wold]]"
    type: foundational_contributor
    confidence: 0.9
  - target: "[[George Box]]"
    type: methodology_developer
    confidence: 0.85
  - target: "[[Gwilym Jenkins]]"
    type: methodology_developer
    confidence: 0.85
  - target: "[[Kalman Filter]]"
    type: advanced_technique_in
    confidence: 0.75
  - target: "[[State-Space Model]]"
    type: modeling_framework_for
    confidence: 0.75
supersedes: null
---

# Time Series Analysis

## 概述
[[时间序列分析]]是统计学的一个重要分支，专注于按时间顺序排列的数据点的分析。它涉及从时间序列数据中提取有意义的统计信息和特征，用于理解潜在的生成机制并进行预测。

## 关键内容
1. **核心概念**：
   - 平稳性：时间序列的基本假设之一
   - 预测理论：基于历史数据预测未来值的方法
   - 分解方法：将时间序列分解为趋势、季节性和随机成分

2. **重要理论**：
   - Wold分解定理：任何[[Stationary Time Series|平稳时间序列]]都可以分解为确定性和不确定性部分
   - 谱分析：从频域角度分析时间序列的特性

3. **建模方法**：
   - ARMA模型：用于[[Stationary Time Series|平稳时间序列]]的[[ARMA Models|自回归移动平均模型]]
   - [[ARIMA|ARIMA模型]]：用于非[[Stationary Time Series|平稳时间序列]]的[[ARIMA Models|差分整合移动自回归模型]]
   - Box-Jenkins方法论：系统化的时间序列建模流程

## 来源
- [[Wold Decomposition Theorem]] — 历史背景和基础定理

## 相关
- [[Wold Decomposition Theorem]] — fundamental_result
- [[ARIMA Models]] — primary_model_class
- [[Box-Jenkins Methodology]] — standard_approach
- [[Statistics]] — parent_field