---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [prediction-theory, time-series-analysis, statistics, probability-theory]
aliases: ["Wold-Kolmogorov Prediction Theory", "Wold-Kolmogorov 预测理论", "Prediction Theory"]
relates_to:
  - target: "[[Herman Wold]]"
    type: co_developer
    confidence: 0.9
  - target: "[[Andrey Kolmogorov]]"
    type: co_developer
    confidence: 0.9
  - target: "[[Wold Decomposition Theorem]]"
    type: extension_of
    confidence: 0.85
  - target: "[[Probability Theory]]"
    type: subfield_of
    confidence: 0.85
  - target: "[[Kalman Filter]]"
    type: successor_method
    confidence: 0.7
  - target: "[[State-Space Model]]"
    type: predecessor_framework
    confidence: 0.7
supersedes: null
---

# Wold-Kolmogorov Prediction Theory

## 概述
Wold-[[安德烈·柯尔莫哥洛夫|Kolmogorov]]预测理论是平稳过程预测理论的统一体系，结合了[[Herman Wold]]和[[Andrey Kolmogorov]]在预测问题上的研究成果。Wold的工作侧重时域，而[[安德烈·柯尔莫哥洛夫|Kolmogorov]]的工作侧重频域（谱分析）。

## 关键内容
1. **理论构成**：
   - Wold贡献：从时域角度直接在时间轴上给出分解的存在性与唯一性
   - [[安德烈·柯尔莫哥洛夫|Kolmogorov]]贡献：从频域（谱分析）角度建立预测理论，用谱密度刻画可预测性的判据

2. **核心洞察**：
   - 平稳过程的**可预测性**与其谱密度函数的性质密切相关
   - 当平稳过程的谱密度f(λ)满足Paley-Wiener条件：$\int_{-\pi}^{\pi} \log f(\lambda) \, d\lambda > -\infty$时，该过程是"纯不确定的"——它的未来无法被过去完美预测

3. **理论意义**：
   - 共同构成了平稳过程预测理论的两大支柱
   - 统一了时域和频域的预测方法
   - 为后续的信号处理和控制系统设计提供了理论基础

## 来源
- [[Wold Decomposition Theorem]] — Wold和Kolmogorov工作的交汇

## 相关
- [[Herman Wold]] — co_developer
- [[Andrey Kolmogorov]] — co_developer
- [[Wold Decomposition Theorem]] — theoretical_basis
- [[Spectral Analysis]] — related_method