---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["AR Model", "Autoregressive Model", "自回归"]
relates_to:
  - target: "[[Wold 分解定理]]"
    type: extends
    confidence: 0.85
  - target: "[[ARIMA 模型]]"
    type: part_of
    confidence: 0.9
  - target: "[[AIC（赤池信息准则）]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# AR 模型（自回归模型）

## 概述
自回归模型是现代时间序列分析的基石，由 George Udny Yule 于 1927 年提出，用当前值与过去若干时刻的线性组合来建模时间序列的动态结构。

## 关键内容

1. **历史背景**：1927 年 Yule 研究沃尔弗太阳黑子数时发现，周期图法无法解释太阳黑子"周期"的不稳定性。他区分了两种"受扰序列"——叠加噪声的周期（Type I）和扰动作用于机制本身的序列（Type II），太阳黑子属于后者。

2. **核心洞察**：Yule 用钟摆类比——不是噪声掩盖了真实周期，而是随机冲击不断重塑动力学过程。这催生了自回归的思想：当前值由过去值和随机扰动共同决定。

3. **数学形式**：AR(p) 模型将当前时刻的值表示为前 p 个时刻的线性组合加上白噪声项。这是第一个用随机差分方程描述时间序列的正式模型。

4. **历史地位**：世界上第一个自回归模型的正式提出，开创了用随机过程而非确定性函数描述时间序列的先河。

## 来源
- [[01-yule-1927-ar-model]] — 一个被随机敲击的钟摆：自回归模型的诞生与太阳黑子之谜

## 相关
- [[Wold 分解定理]] — extends
- [[ARIMA 模型]] — part_of
- [[AIC（赤池信息准则）]] — uses
