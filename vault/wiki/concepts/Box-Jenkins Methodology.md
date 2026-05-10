---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [time-series-analysis, statistics, modeling-methodology]
aliases: ["Box-Jenkins Methodology", "Box-Jenkins 方法论", "Box-Jenkins Modeling"]
relates_to:
  - target: "[[George Box]]"
    type: developer
    confidence: 0.9
  - target: "[[Gwilym Jenkins]]"
    type: developer
    confidence: 0.9
  - target: "[[ARIMA Models]]"
    type: methodology_for
    confidence: 0.9
  - target: "[[Wold Decomposition Theorem]]"
    type: theoretical_foundation
    confidence: 0.85
supersedes: null
---

# Box-Jenkins Methodology

## 概述
Box-Jenkins方法论是由[[George Box]]和[[Gwilym Jenkins]]在1970年代发展的[[时间序列分析]]方法论，为[[ARIMA|ARIMA模型]]提供了一套完整的建模流程。该方法论的理论核心基于Wold分解定理。

## 关键内容
1. **建模步骤**：
   - 模型识别（Identification）：确定[[ARIMA|ARIMA模型]]的参数
   - 参数估计（Estimation）：估计模型参数
   - 模型诊断（Diagnostic Checking）：检验模型的充分性

2. **理论基础**：
   - 理论根基可直接追溯到[[Herman Wold]]在1938年证明的Wold分解定理
   - 定理从纯数学层面证明了用MA(∞)表示平稳过程的随机部分是必然的数学事实
   - 为ARMA模型的存在提供了理论合法性

3. **应用范围**：
   - 宏观经济[[时间序列分析]]（GDP、通胀率、汇率预测）
   - 金融[[数据分析]]
   - 工业过程控制
   - 信号处理等

## 来源
- [[ARIMA Models]] — 发展历程和理论基础

## 相关
- [[George Box]] — developer
- [[Gwilym Jenkins]] — developer
- [[ARIMA Models]] — methodology_for
- [[Wold Decomposition Theorem]] — theoretical_foundation