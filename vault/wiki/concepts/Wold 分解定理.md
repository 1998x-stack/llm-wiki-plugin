---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 时间序列]
aliases: ["Wold Decomposition", "Wold's Theorem", "沃尔德分解"]
relates_to:
  - target: "[[AR 模型（自回归模型）]]"
    type: extends
    confidence: 0.85
  - target: "[[移动平均模型]]"
    type: extends
    confidence: 0.9
  - target: "[[白噪声]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Wold 分解定理

## 概述
Wold 分解定理由 Herman Wold 于 1938 年在博士论文中证明，指出任何平稳时间序列都可唯一分解为确定性分量和纯非确定性分量（无穷阶 MA 过程），为现代时间序列分析奠定理论基石。

## 关键内容

1. **历史背景**：1930 年代[[概率论]]走向成熟，柯尔莫哥洛夫 1933 年建立概率公理化体系。Wold 在斯德哥尔摩大学师从 Harald Cramer，在博士论文中完成了这一奠基性工作。

2. **定理内容**：任何（离散、协方差）平稳时间序列 X_t 可唯一分解为 X_t = D_t + S_t，其中 D_t 是确定性分量（可被自身过去值完美预测），S_t 是纯非确定性分量，可表示为无穷阶移动平均过程 MA(∞)。

3. **核心意义**：任何平稳过程 = 确定性部分 + 无穷阶 MA 部分。这为理解时间序列的"原子结构"提供了统一框架。

4. **影响**：为 ARMA 模型、[[ARIMA 模型]]等后续发展提供了理论基础，是时间序列分析中最重要的分解定理之一。

## 来源
- [[02-wold-1938-decomposition]] — 一切时间序列的"原子结构"：Wold 分解定理的诞生

## 相关
- [[AR 模型（自回归模型）]] — extends
- [[移动平均模型]] — extends
- [[白噪声]] — depends_on
