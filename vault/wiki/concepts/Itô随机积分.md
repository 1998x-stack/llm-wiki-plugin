---
type: concept
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 研究
- 技术
- 概率论
aliases:
- Ito随机积分
- Itô integral
- 伊藤积分
- 随机积分
relates_to:
- target: '[[Wiener过程]]'
  type: depends_on
  confidence: 0.99
- target: '[[Wiener积分]]'
  type: extends
  confidence: 0.95
- target: '[[马尔可夫链]]'
  type: uses
  confidence: 0.7
supersedes: null
---

# Itô 随机积分

## 概述
Itô 随机积分由伊藤清（Kiyoshi Itô）于1944年提出，将[[Wiener积分]]推广至被积函数可依赖[[Wiener过程|布朗运动]]本身的情形，是随机微分方程和数学金融的核心工具，以违反直觉的 Itô 公式（含额外二阶项）为标志。

## 关键内容

1. **动机与局限的超越**：[[Wiener积分]] $\int_0^T f(t) \, dB(t)$ 只能对不依赖于 $B$ 的确定性函数 $f$ 积分。Itô 积分则允许 $f(t, \omega) = f(t, B(t))$——被积函数依赖于[[Wiener过程|布朗运动]]的路径，这对于描述随机微分方程（SDE）不可缺少。

2. **定义（Itô 等距）**：对适应过程（adapted process）$f(t, \omega)$，通过简单过程逼近定义 $\int_0^T f \, dB$，并使用 Itô 等距保证极限存在：$$\mathbb{E}\!\left[\left(\int_0^T f \, dB\right)^2\right] = \mathbb{E}\!\left[\int_0^T f^2 \, dt\right]$$

3. **Itô 公式（随机链式法则）**：若 $X_t = \int_0^t \sigma \, dB + \int_0^t \mu \, dt$，则对光滑函数 $F$：$$dF(X_t) = F'(X_t) \, dX_t + \frac{1}{2} F''(X_t) \, dt$$相比普通链式法则多出 $\frac{1}{2}F'' dt$ 项——来源于[[Wiener过程|布朗运动]]的二次变差 $d[B,B]_t = dt$。这是[[Wiener过程]]路径不可微性在微积分中的体现。

4. **鞅性质**：若 $\mathbb{E}\int_0^T f^2 \, dt < \infty$，则 $M_t = \int_0^t f \, dB$ 是一个均方连续鞅。这一性质使 Itô 积分与[[概率论]]中的鞅理论深度融合。

5. **为何需要新积分**：[[Wiener过程]]路径处处不可微，故 Riemann-Stieltjes 积分 $\int g \, dB$ 无法直接定义（被积量无界变差）。Itô 积分通过左端点 Riemann 和（非中点）绕过这一困难——不同端点选取给出不同积分（Stratonovich 积分），这是随机积分的独特之处。

6. **应用**：SDE $dS = \mu S \, dt + \sigma S \, dB$（几何[[Wiener过程|布朗运动]]，Black-Scholes 模型）；Feynman-Kac 公式（PDE 与 SDE 对应）；随机控制（HJB 方程）；深度学习中 SGD 的 SDE 近似。

## 来源
- [[raw/books/概率论/13_wiener_brownian_motion]] — §对后续发展的影响：Itô 随机积分（1944）；§局限性：路径不可微带来的技术困难

## 相关
- [[Wiener过程]] — depends_on（布朗运动是驱动过程，二次变差是 Itô 公式的来源）
- [[Wiener积分]] — extends（推广了确定性被积函数的限制）
- [[马尔可夫链]] — uses（SDE 解通常是马尔可夫过程）
