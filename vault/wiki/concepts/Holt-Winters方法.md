---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [时间序列分析, 预测方法, 季节性分析, 时间序列]
aliases: ["Holt-Winters Method", "Holt-Winters方法"]
relates_to:
  - target: "[[指数平滑]]"
    type: part_of
  - target: "[[Holt双参数指数平滑]]"
    type: extends
  - target: "[[季节性分量]]"
    type: implements
  - target: "[[Peter R. Winters]]"
    type: implements
  - target: "[[ARIMA]]"
    type: compares_to
  - target: "[[ETS框架]]"
    type: extends
supersedes: null
---

# Holt-Winters方法

## 概述
Holt-Winters方法是完整的三参数[[指数平滑]]方法，包含水平分量、趋势分量和季节性分量，用于预测具有趋势和季节性特征的[[Time Series Analysis|时间序列]]数据。

## 关键内容

1. **发展历程**：由[[彼得·温特斯|Peter R. Winters]]在1960年提出，在Holt的双参数[[指数平滑]]基础上增加季节性分量，形成完整的[[Time Series Analysis|时间序列]]预测方法。

2. **三个参数**：
   - alpha：控制水平分量（数据的基准值）
   - beta：控制趋势分量（数据的上升或下降速率）
   - gamma：控制季节性分量（周期性波动的模式）

3. **两种季节性模式**：
   - 加法模型：季节波动的幅度恒定（如小商店每年夏天多卖100瓶水）
   - 乘法模型：季节波动的幅度随水平值成比例变化（如连锁企业夏天销量翻倍）

4. **应用场景**：适用于具有明显趋势和季节性特征的数据，如季度销售额、月度用电量、季节性商品销量等。

5. **技术原理**：就像预测冰淇淋销量，不仅要了解销量的基准水平和增长趋势，还要掌握"夏天高、冬天低"的周期模式。

6. **实用价值**：至今仍在工业界广泛应用，如[[Amazon]]的需求预测系统、零售企业的补货[[算法]]、能源行业的负荷预测等。

## 来源
- [[03-holt-1957-exponential-smoothing]] — 方法发展历程
- [[指数平滑]] — 相关概念
- [[Peter R. Winters]] — 相关人物

## 相关
- [[指数平滑]] — part_of
- [[Holt双参数指数平滑]] — extends
- [[季节性分量]] — implements
- [[Peter R. Winters]] — implements
- [[ARIMA]] — compares_to
- [[ETS框架]] — extends