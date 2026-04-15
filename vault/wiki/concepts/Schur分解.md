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
- Schur Decomposition
- Schur分解定理
- 酉三角化
- Schur标准形
- Schur形式
relates_to:
- target: '[[伊赛·舒尔]]'
  type: implements
  confidence: 0.95
- target: '[[矩阵理论]]'
  type: part_of
  confidence: 0.9
- target: '[[正规矩阵]]'
  type: depends_on
  confidence: 0.9
- target: '[[QR算法]]'
  type: caused
  confidence: 0.9
- target: '[[谱半径]]'
  type: uses
  confidence: 0.75
- target: '[[极大极小定理]]'
  type: uses
  confidence: 0.6
supersedes: null
---

# Schur分解

## 概述

Schur分解（Schur Decomposition，或酉三角化定理）是[[伊赛·舒尔]]于1909年证明的矩阵分解定理：**任意复方阵 $A \in \mathbb{C}^{n \times n}$ 均可酉相似于上三角矩阵**，即存在酉矩阵 $Q$（$Q^*Q = I$）和上三角矩阵 $T$，使得 $A = QTQ^*$，且 $T$ 的对角元素恰为 $A$ 的全部特征值。该定理是现代矩阵分析与数值线性代数的基石，直接催生了[[QR算法]]并统一了[[正规矩阵]]谱理论。与 Jordan 标准形相比，Schur 分解在酉变换约束下牺牲了块对角结构，换取了卓越的数值稳定性。

## 关键内容

### 主定理

**Schur酉三角化定理（1909）**

设 $A \in \mathbb{C}^{n \times n}$。则存在酉矩阵 $Q \in \mathbb{C}^{n \times n}$ 和上三角矩阵 $T$，使得

$$A = QTQ^*, \quad t_{ii} = \lambda_i \; (i=1,\ldots,n)$$

其中 $\lambda_1, \ldots, \lambda_n$ 是 $A$ 的全部特征值（计重数，可任意排序）。

**等价表述**：$\mathbb{C}^n$ 中存在标准正交基，使 $A$ 在此基下为上三角矩阵；等价地，存在 $A$-不变子空间构成的完全旗（complete flag）

$$\{0\} = V_0 \subset V_1 \subset \cdots \subset V_n = \mathbb{C}^n, \quad \dim V_k = k$$

### 证明（归纳法）

**归纳步骤**：由代数基本定理取特征值 $\lambda_1$ 及其单位特征向量 $v_1$，用 Gram-Schmidt 扩充为标准正交基构成酉矩阵 $U_1$，得

$$U_1^* A U_1 = \begin{pmatrix} \lambda_1 & b^* \\ 0 & A' \end{pmatrix}$$

对 $(n-1)$ 阶矩阵 $A'$ 递归应用归纳假设，最终得到 Schur 形式。

证明仅依赖**代数基本定理**（特征值存在）和 **Gram-Schmidt 正交化**，无需 Jordan 理论的根子空间分析。

### Schur不等式

$$\sum_{i=1}^{n} |\lambda_i|^2 \leq \sum_{i,j} |a_{ij}|^2 = \|A\|_F^2$$

**证明**：酉变换保 Frobenius 范数，故 $\|A\|_F = \|T\|_F = \sqrt{\sum_i |t_{ii}|^2 + \sum_{i<j}|t_{ij}|^2} \geq \sqrt{\sum_i|\lambda_i|^2}$。

**等号成立** $\Longleftrightarrow$ $T$ 的严格上三角部分全为零 $\Longleftrightarrow$ $A$ 为[[正规矩阵]]。

### 正规矩阵刻画

$$A \text{ 正规（}A^*A = AA^*\text{）} \iff A = QDQ^*, D \text{ 为对角矩阵}$$

**推论**：Hermite 矩阵（实特征值）、酉矩阵（模为1的特征值）、实对称矩阵（实特征值，正交对角化）均为正规矩阵的特例，它们的谱定理均是 Schur 定理的推论。

### 与 Jordan 标准形的对比

| 性质 | Jordan 标准形 | Schur 分解 |
|------|-------------|----------|
| 变换类型 | 一般相似变换 | 酉（保范）相似 |
| 标准形结构 | 块对角（Jordan块） | 上三角 |
| 数值稳定性 | 差（条件数可任意大） | 好（酉矩阵条件数=1） |
| 唯一性 | 唯一（块排列确定后） | 不唯一（特征值排列任意） |
| 精细程度 | 最细（完整代数结构） | 较粗（丢失Jordan结构信息） |
| 域要求 | 代数闭域 | 复数域 |

**核心权衡**：Jordan 形最精细但数值不稳定；Schur 形数值稳定但信息略少。实际计算一律用 Schur 分解。

### 关键应用

**QR算法**（Francis & Kublanovskaya, 1961）：反复执行 $A_k = Q_kR_k \to A_{k+1} = R_kQ_k$，序列 $\{A_k\}$ 在满足谱间隙条件时收敛到 Schur 形式。被列为"20世纪十大最有影响力算法"。

**矩阵函数**：若 $A = QTQ^*$，则 $f(A) = Qf(T)Q^*$，上三角矩阵的函数值由 Parlett 递推计算。矩阵指数 $e^A$、矩阵对数 $\ln A$、矩阵平方根 $A^{1/2}$ 等均通过此途径计算。

**控制理论**：线性系统稳定性（特征值实部符号）、Riccati 方程求解、$H_\infty$ 控制均依赖 Schur 形式。

**特征值定位**：Schur 不等式 $\sum|\lambda_i|^2 \leq \|A\|_F^2$ 提供无需求解特征多项式的快速估计（特别是在 $n > 4$ 时特征方程无根式解的情形）。

### Schur补

对分块矩阵 $M = \begin{pmatrix} A & B \\ C & D \end{pmatrix}$（$D$ 可逆），Schur 补定义为

$$M/D = A - BD^{-1}C$$

由 Emilie Haynsworth（1968）以 Schur 名字命名，用于高斯消元、正定性判别、条件分布计算和 Kron 网络约化。

## 局限性

1. **非唯一性**：特征值排列顺序任意，存在重特征值时酉因子选择自由度更大
2. **实数域**：实矩阵只能得到"实 Schur 形"（准上三角，含 2×2 实块对应复特征值对）
3. **Jordan结构信息丢失**：严格上三角部分不是相似不变量
4. **不变子空间问题**：无穷维推广——一般可分 Hilbert 空间有界算子是否都有非平凡不变子空间——至今未解决

## 来源

- raw/books/矩阵分析/08_schur_unitary_triangularization_1909.md

## 相关

- [[伊赛·舒尔]]
- [[正规矩阵]]
- [[QR算法]]
- [[矩阵理论]]
- [[谱半径]]
- [[Perron-Frobenius定理]]
