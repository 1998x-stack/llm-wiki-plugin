---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["ARCH Model", "Autoregressive Conditional Heteroscedasticity", "自回归条件异方差模型"]
relates_to:
  - target: "[[GARCH 模型]]"
    type: extends
    confidence: 0.95
  - target: "[[AR 模型（自回归模型）]]"
    type: extends
    confidence: 0.8
  - target: "[[格兰杰因果（Granger Causality）]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# ARCH 模型

## 概述
ARCH（[[AR 模型（自回归模型）|自回归]]条件异方差）模型由 Robert Engle 于 1982 年提出，首次为金融市场波动率的时变特征提供数学框架，揭示了"波动率聚集"现象，是金融计量经济学的里程碑，Engle 因此获得 2003 年诺贝尔经济学奖。

## 关键内容

1. **历史背景**：1970-80 年代全球经济剧烈震荡（石油危机、[[布雷顿森林体系]]崩溃），传统计量模型假设方差恒定（homoscedasticity），但金融数据明显呈现"大波动后跟大波动，小波动后跟小波动"的聚集特征。

2. **核心思想**：条件方差不是常数，而是过去误差平方的函数。ARCH(q) 模型将当前条件方差表示为过去 q 期误差平方的线性组合，使波动率成为可预测的量。

3. **波动率聚集**：Engle 用河流类比——河水汹涌时不会立刻恢复平静，而是持续翻滚一段时间。金融市场同理，一次剧烈震荡后市场不会立刻风平浪静。

4. **学科影响**：开创了金融波动率建模的新纪元，为风险管理、期权定价、资产[[Configuration|配置]]提供了核心工具。Engle 与 Granger 共同获得 2003 年诺贝尔经济学奖。

## 来源
- [[08-engle-1982-arch]] — 当恐慌会"传染"：Engle 的 ARCH 模型如何捕捉金融市场的波动记忆

## 相关
- [[GARCH 模型]] — extends
- [[AR 模型（自回归模型）]] — extends
- [[格兰杰因果（Granger Causality）]] — relates_to
