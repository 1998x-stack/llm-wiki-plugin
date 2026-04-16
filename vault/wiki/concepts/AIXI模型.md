---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, 研究, AI工程]
aliases:
- AIXI
- 通用人工智能模型
relates_to:
- target: '[[Solomonoff先验]]'
  type: depends_on
  confidence: 0.95
- target: '[[算法信息论]]'
  type: depends_on
  confidence: 0.9
- target: '[[雷·所罗门诺夫]]'
  type: extends
  confidence: 0.85
supersedes: null
---

# AIXI模型

## 概述

AIXI 是 Marcus Hutter (2000) 提出的通用人工智能理论模型，将 Solomonoff 归纳推理与 Bellman 最优控制结合，在任何可计算环境中都能做出最优决策（但本身不可计算）。

## 关键内容

### 核心思想

AIXI = Solomonoff 归纳 + Bellman 最优方程

- **感知**：使用 Solomonoff 先验 [[Solomonoff先验|M(x)]] 对环境进行[[托马斯·贝叶斯|贝叶斯]]预测
- **决策**：选择使期望累积奖励最大化的动作
- **学习**：通过与环境交互不断更新后验信念

### 最优性

AIXI 在任何可计算的环境中都能做出最优决策——它的累积奖励与最优策略的差距有界，且上界仅取决于环境的 [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 复杂性。

### 不可计算性

与 Solomonoff 先验一样，AIXI 是不可计算的。它提供了一个理论上限（gold standard），实际的[[强化学习]]算法可以视为 AIXI 的可计算近似。

### 与 LLM 的关系

大语言模型可以看作 AIXI 在纯文本环境中的某种近似：通过大规模预训练学习了一个"通用先验"，然后通过上下文学习（in-context learning）适应新任务——类似于 AIXI 的[[托马斯·贝叶斯|贝叶斯]]更新机制。

## 来源

- [[raw/books/信息论/08_solomonoff_1964_formal_theory_of_inductive_inference.md]] — Solomonoff (1964) 深度解析
- [Universal Artificial Intelligence (Hutter 2005)](https://link.springer.com/book/10.1007/b138233)

## 相关

- [[Solomonoff先验]] — 感知模块的基础
- [[算法信息论]] — 理论基础
- [[雷·所罗门诺夫]] — 理论先驱
