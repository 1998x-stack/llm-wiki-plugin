---
type: concept
status: active
confidence: 0.8
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [时间序列预测, 深度学习, 可解释AI]
aliases: ["可解释型N-BEATS", "Interpretable Configuration"]
relates_to:
  - target: "[[N-BEATS：Neural Basis Expansion Analysis for Interpretable Time Series Forecasting]]"
    type: configuration_of
    confidence: 0.9
  - target: "[[神经基函数展开分析]]"
    type: variant_of
    confidence: 0.9
  - target: "[[趋势栈]]"
    type: incorporates
    confidence: 0.9
  - target: "[[季节性栈]]"
    type: incorporates
    confidence: 0.9
  - target: "[[可解释AI]]"
    type: contributes_to
    confidence: 0.8
supersedes: null
---

# N-BEATS可解释配置

## 概述
N-BEATS的可解释配置是该模型的一个运行模式，通过将不同的栈赋予明确的语义角色来实现模型的可解释性。

## 关键内容

1. **趋势栈（Trend Stack）**：
   - 基函数被约束为低阶多项式
   - 输出被表示为多项式系数与时间幂次向量的线性组合
   - 只能生成平滑的趋势曲线：单调增长、单调下降或缓慢弯曲的走势

2. **季节性栈（Seasonality Stack）**：
   - 基函数被约束为傅里叶级数，即正弦和余弦函数的线性组合
   - 专门负责捕捉数据中的周期性波动：每周的销售规律、每年的温度循环等

3. **设计意义**：
   - 直接来源于经典时间序列分解思想
   - 通过基函数约束，让神经网络自动完成趋势、季节性和残差的分解
   - 每个成分都可以单独可视化和分析
   - 预测精度仅略低于通用配置，但获得极高透明度

## 来源
- [[14-nbeats-2019-neural-basis-expansion.md]] — 详细介绍可解释配置的设计和原理

## 相关
- [[N-BEATS：Neural Basis Expansion Analysis for Interpretable Time Series Forecasting]] — configuration_of
- [[神经基函数展开分析]] — variant_of
- [[趋势栈]] — incorporated
- [[季节性栈]] — incorporated
- [[可解释AI]] — contributes_to