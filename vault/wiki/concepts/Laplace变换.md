---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 技术
- 研究
- 数学
- 数值分析
aliases:
- Laplace Transform
- 拉普拉斯变换
- L变换
relates_to:
- target: '[[皮埃尔-西蒙·拉普拉斯]]'
  type: caused
  confidence: 0.9
- target: '[[生成函数]]'
  type: extends
  confidence: 0.85
  note: Laplace变换是生成函数从离散到连续的推广；两者都将函数"编码"为更易分析的形式
- target: '[[概率论]]'
  type: related_to
  confidence: 0.8
  note: Laplace在处理连续概率问题时引入，是矩母函数和特征函数的早期形式
supersedes: null
---

# Laplace 变换

## 概述

Laplace 变换（Laplace Transform）是由[[皮埃尔-西蒙·拉普拉斯]]在处理连续概率问题时引入的积分变换工具，定义为：

$$\mathcal{L}[f](s) = \int_0^\infty f(t)\, e^{-st}\, dt$$

它将时域（或概率域）中的函数 $f(t)$ 转换为复频域的函数 $F(s)$，使微分方程变为代数方程，从而极大地简化分析。Laplace 变换是[[生成函数]]从离散到连续函数的自然推广，也是[[概率论]]中矩[[生成函数|母函数]]（moment generating function）的早期形式。

## 关键内容

- **来源**：Laplace 在 *Théorie analytique des probabilités*（1812）中引入，用于处理连续概率分布的积分[[计算]]和大数近似
- **关系与[[生成函数]]**：离散的[[生成函数]] $G(z) = \sum a_n z^n$ 对应连续的 Laplace 变换 $F(s) = \int f(t)e^{-st}dt$，两者的代数性质和应用思路高度相似
- **主要性质**：线性性、时域微分对应频域多项式乘法（$\mathcal{L}[f'](s) = sF(s) - f(0)$）、卷积定理
- **与[[概率论]]的联系**：在[[概率论]]中，若 $X \geq 0$ 为随机变量，则 $\mathcal{L}[\text{PDF}_X](s) = \mathbb{E}[e^{-sX}]$ 即为矩[[生成函数|母函数]]，控制矩的生成和分布的唯一性
- **现代影响**：Laplace 变换成为信号处理、控制理论、电路分析、偏微分方程和[[概率论]]的基本工具；工程学中的传递函数（transfer function）依赖于此

## 来源

- [[raw/books/概率论/06_laplace_theorie_analytique.md]]

## 相关

- [[皮埃尔-西蒙·拉普拉斯]]
- [[生成函数]]
- [[概率论]]
