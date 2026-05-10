---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["ARIMA", "AutoRegressive Integrated Moving Average", "差分整合自回归移动平均模型"]
relates_to:
  - target: "[[AR 模型（自回归模型）]]"
    type: extends
    confidence: 0.95
  - target: "[[移动平均模型]]"
    type: extends
    confidence: 0.95
  - target: "[[指数平滑]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# ARIMA 模型

## 概述
[[ARIMA]]（[[AR 模型（自回归模型）|自回归]]积分移动平均模型）由 [[George Box]] 和 [[Gwilym Jenkins]] 于 1970 年在《[[Time Series Analysis]]: Forecasting and Control》中提出，将 AR、差分和 MA 统一为单一框架，是[[时间序列分析]]历史上影响最深远的建模方法。

## 关键内容

1. **历史背景**：1970 年前，AR 和 MA 被视为两类独立模型，差分技术散落在不同领域。Box 和 Jenkins 的核心洞见：三者不是互相竞争的方法，而是同一模型的三个组成部分。

2. **[[ARIMA]](p,d,q) 框架**：AR(p) [[AR 模型（自回归模型）|自回归]]部分（当前值依赖过去 p 个值）+ I(d) 差分部分（d 次差分实现平稳化）+ MA(q) 移动平均部分（当前值依赖过去 q 个随机冲击）。

3. **[[Box-Jenkins Methodology|Box-Jenkins 方法论]]**：提出系统性的建模流程——识别（通过 ACF/PACF 选择 p,d,q）→ 估计（最大似然或最小二乘）→ 诊断检验（残差白噪声检验）→ 预测。

4. **学科影响**：统计学、计量经济学、运筹学、信号处理、金融工程、气象学、工业控制等领域均受其深远影响，至今仍是[[时间序列分析]]的入门必修内容。

## 来源
- [[06-box-jenkins-1970-arima]] — 时间序列的"统一场论"：Box 与 Jenkins 如何用一本书改变了预测科学

## 相关
- [[AR 模型（自回归模型）]] — extends
- [[移动平均模型]] — extends
- [[指数平滑]] — compares_to
- [[N-BEATS]] — compares_to（深度学习时间序列预测）
- [[Prophet]] — compares_to（Facebook 开源的预测工具）
- [[协整分析（Cointegration）]] — compares_to（多变量时间序列）
- [[马尔可夫体制转换模型]] — compares_to（状态转换时间序列）
