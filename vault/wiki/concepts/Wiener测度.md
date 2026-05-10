---
type: concept
status: active
confidence: 0.93
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 研究
- 技术
- 概率论
- 数学
aliases:
- Wiener measure
- 维纳测度
- 路径空间测度
relates_to:
- target: '[[Wiener过程]]'
  type: caused
  confidence: 0.99
- target: '[[概率公理体系]]'
  type: extends
  confidence: 0.9
- target: '[[诺伯特·维纳]]'
  type: depends_on
  confidence: 0.99
supersedes: null
---

# Wiener 测度

## 概述
Wiener 测度是[[诺伯特·维纳]]于1923年在连续函数空间 $C_0[0,1]$ 上构造的概率测度，是无穷维空间上第一个严格的概率测度，奠定了[[Wiener过程]]（[[Wiener过程|布朗运动]]）的数学存在性。

## 关键内容

1. **构造问题**：有限维欧氏空间上的概率测度可通过密度函数定义，但连续函数空间是无穷维的——没有 Lebesgue 测度的类比，密度函数方法失效。Wiener 测度的构造是第一次克服这一障碍。

2. **三步构造**：
   - **有限维分布**：对任意时刻 $0 < t_1 < \cdots < t_n \leq 1$，指定联合密度 $p(x_1,\ldots,x_n) = \prod_k \frac{1}{\sqrt{2\pi(t_k - t_{k-1})}} \exp\!\left(-\frac{(x_k-x_{k-1})^2}{2(t_k-t_{k-1})}\right)$，其中 $t_0=x_0=0$。
   - **[[安德烈·柯尔莫哥洛夫|Kolmogorov]] 相容性**：验证这些有限维分布满足边际化一致性，从而（由 [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 扩展定理）可以定义乘积空间上的测度。
   - **路径连续性**：利用 Borel-Cantelli 引理控制细网格上的增量，证明该测度集中在连续函数子集上——这是关键也是最困难的一步。

3. **与 [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 扩展定理的关系**：Wiener 的方法后来被理解为[[概率公理体系|Kolmogorov 扩展定理]]的应用[[规范化理论|范式]]——先给出满足相容性条件的有限维族，再取极限。[[诺伯特·维纳|维纳]]的工作（1923）比[[Andrey Kolmogorov|柯尔莫哥洛夫]]建立公理体系（1933）早十年。

4. **无穷维[[概率论]]的先驱**：Wiener 测度开创了无穷维空间上[[概率论]]的研究，影响了高斯过程理论、抽象 Wiener 空间（Gross, 1965）和 Malliavin 微积分（1976）。

5. **物理意义**：Wiener 测度赋予"连续函数"一个自然的概率权重——越"不规则"（振荡越大）的路径被赋予越小的权重，但测度集中于处处不可微的路径。

## 来源
- [[raw/books/概率论/13_wiener_brownian_motion]] — §主要结论：Wiener 测度的构造；§突破了什么瓶颈：无穷维测度构造

## 相关
- [[Wiener过程]] — caused（Wiener 测度的存在保证了布朗运动的数学存在性）
- [[概率公理体系]] — extends（与 Kolmogorov 公理化体系同时代，相互促进）
- [[诺伯特·维纳]] — depends_on（由维纳首次构造）
