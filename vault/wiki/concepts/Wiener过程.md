---
type: concept
status: active
confidence: 0.97
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 研究
- 技术
- 概率论
aliases:
- 布朗运动
- Brownian Motion
- Wiener process
- 标准布朗运动
relates_to:
- target: '[[Wiener测度]]'
  type: depends_on
  confidence: 0.99
- target: '[[随机游走]]'
  type: extends
  confidence: 0.95
- target: '[[Itô随机积分]]'
  type: extends
  confidence: 0.95
- target: '[[马尔可夫链]]'
  type: extends
  confidence: 0.85
- target: '[[正态分布]]'
  type: uses
  confidence: 0.95
- target: '[[中心极限定理]]'
  type: depends_on
  confidence: 0.85
- target: '[[诺伯特·维纳]]'
  type: depends_on
  confidence: 0.99
supersedes: null
---

# Wiener 过程

## 概述
Wiener 过程（布朗运动）是概率论中最重要的连续时间随机过程：具有独立平稳正态增量、几乎处处连续路径，由[[诺伯特·维纳]]于1923年在[[Wiener测度]]框架下首次严格构造。

## 关键内容

1. **定义性质**：标准 Wiener 过程 $\{B(t)\}_{t \geq 0}$ 满足：$B(0)=0$；增量 $B(t)-B(s) \sim N(0, t-s)$ 对 $0 \leq s < t$；不重叠区间上的增量相互独立；路径 $t \mapsto B(t)$ 几乎处处连续。

2. **路径正则性（核心结果）**：以概率1，Wiener 过程路径是连续函数，但在每一点处不可微。更精确地，路径几乎处处是 $\alpha$-Hölder 连续的对任意 $\alpha < 1/2$，但对 $\alpha \geq 1/2$ 不成立。指数 $1/2$ 是"连续与可微之间"的临界点，对应 $\Delta B \sim \sqrt{\Delta t}$。

3. **不可微性的直觉**：$B'(t) \approx \Delta B / \Delta t \sim 1/\sqrt{\Delta t} \to \infty$，即"导数"趋于无穷——这是纯粹随机性在微观尺度上的必然代价。处处不可微意味着路径在任何尺度下都是锯齿状的（尺度不变的粗糙）。

4. **关键路径性质**：
   - **自相似性**：$\{B(ct)\} \overset{d}{=} \{\sqrt{c}\, B(t)\}$
   - **时间反演**：$\{t B(1/t)\}_{t>0}$ 也是 Wiener 过程
   - **二次变差**：$\sum_k (B(t_k) - B(t_{k-1}))^2 \to t$（这是[[Itô随机积分]]理论的关键）
   - **常返性（一维）**：以概率1，布朗运动将无限次到达任意实数点

5. **三大中心角色**：Wiener 过程同时是：最简单的连续时间[[马尔可夫链|马尔可夫过程]]（连续路径）；最简单的连续时间鞅（$B(t)$、$B(t)^2-t$、$e^{\lambda B(t) - \lambda^2 t/2}$ 均为鞅）；对称[[随机游走]]在时空同时缩放下的极限（空间步长 $\propto \sqrt{\text{时间步长}}$）。

6. **历史背景**：物理现象由罗伯特·布朗（1827）发现，物理理论由爱因斯坦（1905）给出，[[路易·巴舍利耶]]（1900）独立描述了有限维分布。[[诺伯特·维纳]]（1923）通过[[Wiener测度]]给出了第一个严格的数学存在性证明。

7. **分形维数**：Wiener 过程路径的图像 Hausdorff 维数为 $3/2$（在 $\mathbb{R}^2$ 中）；$d$ 维布朗运动轨迹的维数为 $\min(2, d)$。

## 来源
- [[raw/books/概率论/13_wiener_brownian_motion]] — 全文（核心问题、主要结论、路径性质、重要性、对后续影响）

## 相关
- [[Wiener测度]] — depends_on（存在性由 Wiener 测度保证）
- [[随机游走]] — extends（Wiener 过程是对称随机游走的连续极限）
- [[Itô随机积分]] — extends（Wiener 过程是 Itô 积分的驱动过程）
- [[马尔可夫链]] — extends（连续时间马尔可夫过程的原型）
- [[正态分布]] — uses（增量服从正态分布）
- [[中心极限定理]] — depends_on（随机游走→Wiener过程的极限论证）
- [[诺伯特·维纳]] — depends_on（由维纳首次严格构造）
