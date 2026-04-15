---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
aliases:
- Algorithmic Probability
- Solomonoff Prior
- M(x)
- 算法概率
relates_to:
- target: '[[雷·所罗门诺夫]]'
  type: caused
  confidence: 0.95
- target: '[[柯尔莫哥洛夫复杂性]]'
  type: related_to
  confidence: 0.95
- target: '[[算法信息论]]'
  type: part_of
  confidence: 0.95
- target: '[[信息论]]'
  type: extends
  confidence: 0.85
- target: '[[贝叶斯推断]]'
  type: related_to
  confidence: 0.9
supersedes: null
---

# Solomonoff先验

## 概述

Solomonoff 先验（算法概率）M(x) = Σ 2^{-|p|} 是对所有能输出 x 的程序按其长度加权求和，是 Occam 剃刀的精确数学化，为通用归纳推理提供了最优先验分布。

## 关键内容

### 定义

$$M(x) = \sum_{p: U(p) = x^*} 2^{-|p|}$$

其中 U 是一台固定的[[图灵机|通用图灵机]]，求和遍历所有使 U 输出以 x 为前缀的串的程序 p，|p| 是程序 p 的长度。

### 直觉解释

想象一只猴子在键盘上随机打字，产生一个程序。这个程序被送入[[图灵机|通用图灵机]]执行。M(x) 就是猴子打出的程序恰好输出 x 的概率。

### Occam 剃刀的形式化

短程序的概率（2^{-|p|}）远高于长程序。一个 10 bit 的程序比一个 100 bit 的程序有 2^90 ≈ 10^27 倍高的先验概率。因此，如果一个简单的规律（短程序）能解释数据，它自动获得更高的后验概率。

### 与 Kolmogorov 复杂性的关系

$$K(x) \leq -\log_2 M(x) \leq K(x) + O(\log K(x))$$

算法概率的负对数近似等于 [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 复杂性。一个字符串的先验概率主要由能产生它的最短程序决定。

### Solomonoff 收敛定理

如果数据由某个可计算的概率分布 μ 生成，Solomonoff 预测器的预测概率会以指数速度收敛到 μ 的真实条件概率，且总预测误差有界：

$$D_{\text{KL}}(\mu \| M | x_1 \cdots x_n) \leq K(\mu) \cdot \ln 2$$

### 不可计算性

M(x) 是不可计算的——不存在算法能在有限时间内精确计算它。这涉及对所有可能程序的求和，等价于解决[[停机问题]]。但它提供了一个理论上限（gold standard），实际学习算法可视为其可计算近似。

## 来源

- [[raw/books/信息论/08_solomonoff_1964_formal_theory_of_inductive_inference.md]] — Solomonoff (1964) 深度解析

## 相关

- [[雷·所罗门诺夫]] — 提出者
- [[柯尔莫哥洛夫复杂性]] -M(x) 的负对数近似等于 K(x)
- [[算法信息论]] — 所属学科
- [[信息论]] — 扩展的学科
- [[贝叶斯推断]] — Solomonoff 先验是通用贝叶斯先验
