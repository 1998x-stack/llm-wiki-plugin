---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论"]
aliases: ["GARCH Model", "Generalized ARCH", "广义自回归条件异方差模型"]
relates_to:
  - target: "[[ARCH 模型]]"
    type: extends
    confidence: 0.95
  - target: "[[ARIMA 模型]]"
    type: compares_to
    confidence: 0.75
supersedes: null
---

# GARCH 模型

## 概述
GARCH（广义[[AR 模型（自回归模型）|自回归]]条件异方差）模型由 Tim Bollerslev 于 1986 年提出，在 ARCH 基础上引入条件方差的[[AR 模型（自回归模型）|自回归]]项，仅用三个参数即可捕捉波动率的长期持续性，是金融计量经济学引用量最高的论文之一。

## 关键内容

1. **ARCH 的局限**：ARCH(q) 需要大量参数才能刻画波动率的长期持续性（q 可能需 20+），导致估计精度下降、约束困难、模型笨重脆弱。

2. **GARCH 的创新**：将条件方差表示为过去方差和过去误差平方的组合，GARCH(p,q) 用极少的参数实现 ARCH 需要几十个参数才能达到的效果。类比：用直尺画曲线，ARCH 用无数短线段拼接，GARCH 用平滑曲线一步到位。

3. **核心公式**：σ²_t = ω + Σα_i·ε²_{t-i} + Σβ_j·σ²_{t-j}，仅三个参数（ω, α, β）即可捕捉波动率的长期记忆。

4. **影响**：成为金融波动率建模的标准工具，衍生出 EGARCH、TGARCH、IGARCH 等数十种变体，广泛应用于风险管理、期权定价、VaR 计算。

## 来源
- [[09-bollerslev-1986-garch]] — 三个参数驯服金融风暴：Bollerslev 的 GARCH 模型

## 相关
- [[ARCH 模型]] — extends
- [[ARIMA 模型]] — compares_to
