---
type: concept
status: active
confidence: 0.88
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [研究, 技术]
aliases: ["Wiener integral", "维纳积分", "路径积分（Wiener）"]
relates_to:
  - target: "[[Wiener过程]]"
    type: depends_on
    confidence: 0.99
  - target: "[[Itô随机积分]]"
    type: extends
    confidence: 0.95
  - target: "[[诺伯特·维纳]]"
    type: depends_on
    confidence: 0.99
supersedes: null
---

# Wiener 积分

## 概述
Wiener 积分是[[诺伯特·维纳]]在路径空间上定义的对**确定性函数**的积分 $\int_0^1 f(t)\,dB(t)$，是随机积分最早的严格形式，后被[[Itô随机积分]]推广。

## 关键内容

1. **定义**：对 $L^2[0,1]$ 中的确定性函数 $f$，Wiener 积分定义为 Riemann-Stieltjes 型极限：$$\int_0^1 f(t)\,dB(t) = \lim_{n\to\infty} \sum_{k=1}^n f(t_{k-1})\bigl(B(t_k) - B(t_{k-1})\bigr)$$均方极限在 $L^2$ 中存在且唯一。

2. **统计性质**：结果是均值为0的高斯随机变量，方差为 $\int_0^1 f(t)^2\,dt$（Wiener 等距）——被积函数的 $L^2$ 范数完全决定了积分的分布。

3. **关键约束：确定性被积函数**：被积函数 $f(t)$ 不能依赖于 $B$ 本身。这一约束来自[[Wiener过程]]路径的无界变差（处处不可微），导致依赖路径的 Riemann 和不收敛。突破这一约束需要[[Itô随机积分]]的新框架。

4. **与 Feynman 路径积分的联系**：Feynman 量子力学路径积分的灵感部分来源于 Wiener 积分，两者通过 Wick 旋转 $t \to it$ 相联系。Wiener 积分是目前最接近严格化的"路径积分"版本。

## 来源
- [[raw/books/概率论/13_wiener_brownian_motion]] — §主要结论：Wiener 积分；§突破了什么瓶颈：路径积分的数学基础

## 相关
- [[Wiener过程]] — depends_on（需要布朗运动路径作为积分器）
- [[Itô随机积分]] — extends（Itô 积分将 Wiener 积分推广至随机被积函数）
- [[诺伯特·维纳]] — depends_on（由维纳定义）
