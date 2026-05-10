---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [时间序列分析, 统计框架, 状态空间模型]
aliases: ["ETS Framework", "Error-Trend-Seasonal Framework", "误差-趋势-季节性框架"]
relates_to:
  - target: "[[指数平滑]]"
    type: extends
  - target: "[[状态空间模型]]"
    type: implements
  - target: "[[Rob J. Hyndman]]"
    type: implements
  - target: "[[ARIMA]]"
    type: relates_to
supersedes: null
---

# ETS框架

## 概述
ETS（Error, Trend, Seasonal）框架是[[罗布·海德曼|Rob J. Hyndman]]等人提出的状态空间框架，将[[指数平滑]]方法统一纳入具有完整统计理论基础的模型体系。

## 关键内容

1. **核心理念**：将各种[[指数平滑]]方法表示为[[State-Space Model|状态空间模型]]，包括误差项、趋势项和季节性项的组合，为[[指数平滑]]提供了完整的概率分布假设。

2. **理论突破**：2002年前后，Hyndman及其合作者证明了每种[[指数平滑]]方法都对应一个[[State-Space Model|状态空间模型]]，将[[指数平滑]]从"工程技巧"提升为"统计方法"。

3. **三大组成部分**：
   - Error（误差）：模型中的随机扰动项
   - Trend（趋势）：数据的趋势成分（无、加法、乘法）
   - Seasonal（季节性）：数据的季节性成分（无、加法、乘法）

4. **理论意义**：
   - [[指数平滑]]不再只是"启发式[[算法]]"，而是有似然函数的正规统计方法
   - 可以进行模型选择和区间预测
   - 某些[[指数平滑]]模型等价于特定的[[ARIMA|ARIMA模型]]

5. **实践价值**：提供了自动化的模型选择机制，[[Python]]的statsmodels库、R的forecast包等都将ETS作为核心方法。

6. **权威著作**：Hyndman等人2008年出版的《Forecasting with [[指数平滑|Exponential Smoothing]]: The State Space Approach》是该领域的标准参考。

## 来源
- [[03-holt-1957-exponential-smoothing]] — 理论统一介绍
- [[Rob J. Hyndman]] — 相关人物
- [[指数平滑]] — 相关概念

## 相关
- [[指数平滑]] — extends
- [[状态空间模型]] — implements
- [[Rob J. Hyndman]] — implements
- [[ARIMA]] — relates_to