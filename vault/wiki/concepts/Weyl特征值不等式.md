---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 研究
- 技术
- 矩阵理论
aliases:
- Weyl inequality
- Weyl不等式
- Weyl加法不等式
- 特征值扰动界
- Weyl eigenvalue inequalities
relates_to:
- target: '[[赫尔曼·外尔]]'
  type: implements
  confidence: 0.95
- target: '[[极大极小定理]]'
  type: depends_on
  confidence: 0.95
- target: '[[矩阵扰动理论]]'
  type: caused
  confidence: 0.9
- target: '[[正规矩阵]]'
  type: depends_on
  confidence: 0.85
- target: '[[Schur分解]]'
  type: uses
  confidence: 0.7
- target: '[[谱半径]]'
  type: uses
  confidence: 0.7
supersedes: null
---

# Weyl特征值不等式

## 概述

Weyl特征值不等式（1912）是[[矩阵扰动理论]]的奠基性定理，由[[赫尔曼·外尔]]在证明偏微分方程特征值渐近律的过程中作为技术工具发展而来。**核心结论：Hermitian [[矩阵]] $A$ 和 $B$ 之和 $A+B$ 的每个特征值，受 $A$ 和 $B$ 各自特征值的精确线性控制；扰动[[矩阵]]将特征值偏移量限制在谱范数量级内。** 该定理将 Hermitian 特征值揭示为[[矩阵]]空间上 Lipschitz 连续的函数，是数值[[线性代数]]所有对称特征值算法正确性分析的数学基础。

## 关键内容

### 主定理（加法不等式）

设 $A, B$ 为 $n \times n$ Hermitian [[矩阵]]，特征值非递减排列：$\lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_n$。则对满足 $i+j-1 \leq n$ 的指标：

$$\lambda_{i+j-1}(A+B) \leq \lambda_i(A) + \lambda_j(B)$$

对应的下界（$i+j-n \geq 1$ 时）：

$$\lambda_{i+j-n}(A+B) \geq \lambda_i(A) + \lambda_j(B)$$

**最常用特例**（取 $j=1$ 或 $j=n$）：

$$\lambda_i(A) + \lambda_1(B) \leq \lambda_i(A+B) \leq \lambda_i(A) + \lambda_n(B)$$

即每个特征值 $\lambda_i(A+B)$ 被夹在 $\lambda_i(A)$ 加上 $B$ 最小/最大特征值之间。

### 特征值扰动界（Lipschitz连续性）

设 $A$ 为 Hermitian，$E$ 为 Hermitian 扰动，则：

$$\max_{1 \leq i \leq n} |\lambda_i(A+E) - \lambda_i(A)| \leq \|E\|_2$$

**解读**：扰动[[矩阵]] $E$ 使每个特征值偏移至多 $\|E\|_2$（谱范数 = $E$ 的最大特征值绝对值）。这是全局结论，同时控制所有 $n$ 个特征值。

**Lipschitz 表述**：映射 $A \mapsto \lambda(A)$（有序特征值向量）满足

$$\|\lambda(A) - \lambda(B)\|_\infty \leq \|A - B\|_2$$

Lipschitz 常数恰为1，且该界是紧的（可以等号成立）。

### 证明思路

证明完全依赖[[极大极小定理]]的**子空间维数论证**：

1. 由 [[恩斯特·菲舍尔|Fischer]] 极大极小，$\lambda_k(A+B) = \min_{\dim V=k} \max_{x \in V, \|x\|=1} x^*(A+B)x$
2. 取 $k = i+j-1$，构造子空间 $V_0 = U^\perp \cap W^\perp$（$U$ = $A$ 前 $i$ 个特征向量，$W$ = $B$ 前 $j$ 个特征向量），维数论证保证 $\dim(V_0^\perp) \leq i+j$
3. 在适当选取的 $(i+j-1)$ 维子空间上，[[瑞利勋爵|Rayleigh]] 商分解为 $x^*Ax + x^*Bx \leq \lambda_i(A) + \lambda_j(B)$

**精髓**：将特征值代数问题化为子空间几何问题，通过维数计数（[[组合数学|组合论]]证）连接不同[[矩阵]]的谱。

### Hermitian 限制的必要性

对于**非[[正规矩阵]]**，Weyl 不等式不成立。考虑 $n$ 阶 Jordan 块 $J_n$（特征值全为0），扰动 $J_n + \varepsilon e_n e_1^T$ 的特征值为 $\varepsilon^{1/n} e^{2\pi ik/n}$——对极小 $\varepsilon$，特征值偏移量仍为 $\varepsilon^{1/n} \gg \varepsilon$。Hermitian 性（自伴性）是特征值稳定性的结构保证。

### 推广与加强

| 结果 | 作者 | 年份 | 内容 |
|------|------|------|------|
| [[樊畿|Ky Fan]] 部分和不等式 | [[樊畿]] | 1949 | $\sum_{i=1}^k\lambda_i(A+B)\leq\sum_{i=1}^k\lambda_i(A)+\sum_{i=1}^k\lambda_i(B)$，将Weyl的逐项控制提升为部分和控制 |
| Hoffman-[[赫尔穆特·维兰特|Wielandt]]不等式 | Hoffman & [[赫尔穆特·维兰特|Wielandt]] | 1953 | $\sum_i|\lambda_i(A)-\lambda_i(B)|^2 \leq \|A-B\|_F^2$，$\ell^2$ 加强 |
| Lidskii不等式 | Lidskii | 1950 | 特征值部分和的约束，$\lambda(A)-\lambda(B)\prec\lambda(A-B)$ |
| Davis-Kahan定理 | Davis & Kahan | 1970 | 特征子空间扰动的 $\sin\Theta$ 界 |
| Kato算子扰动论 | Kato | 1966 | 无穷维自伴算子推广 |
| Horn猜想（已解决） | Klyachko; Knutson-Tao | 1998–1999 | 特征值完整约束的充要条件，涉及 Schubert 演算 |

### Horn猜想（1962–1999）

Alfred Horn 在1962年提出：Weyl-Lidskii 型不等式是否给出了 $A+B$ 特征值的**完整**约束？即给定三组实数 $\alpha, \beta, \gamma$，何时存在 Hermitian [[矩阵]] $A, B$ 使 $\lambda(A)=\alpha, \lambda(B)=\beta, \lambda(A+B)=\gamma$？

1999–2000年，Knutson-Tao 通过**蜂巢模型**（honeycomb model）结合 Schubert 演算给出完整解答，将[[矩阵]]分析与代数几何、组合学深度连接。这是21世纪初数学的重大成就。

## 现代应用

| 应用场景 | Weyl不等式的作用 |
|---------|--------------|
| 数值特征值算法（QR、分治、MRRR） | [[后向误差分析|后向稳定性]]分析：舍入误差 $\leq \|E\|_2$ 界定计算精度 |
| PCA的统计一致性 | 样本协方差与总体协方差的特征值偏差界 |
| 谱聚类稳定性 | 噪声扰动下 Laplacian 特征值的稳定性保证 |
| 量子力学微扰论 | 能级移动的严格误差控制 |
| 随机[[矩阵理论]] | Wigner 半圆律、Tracy-Widom 分布的证明工具 |
| 图论与网络科学 | 边扰动下 Fiedler 值（代数连通度）的稳定性 |

## 局限性

1. **仅限 Hermitian [[矩阵]]**：对非[[正规矩阵]]不成立，需要伪谱（pseudospectra）理论替代
2. **只给界不给等号**：不等式是紧的但不精确，$A+B$ 的特征值在允许范围内可任意取值
3. **无穷维推广复杂**：对无界算子需要 Kato 的精细理论框架

## 来源

- [[raw/books/矩阵分析/09_weyl_eigenvalue_inequalities_1912.md]]

## 相关

- [[赫尔曼·外尔]]
- [[极大极小定理]]
- [[矩阵扰动理论]]
- [[正规矩阵]]
- [[Schur分解]]
- [[谱半径]]
