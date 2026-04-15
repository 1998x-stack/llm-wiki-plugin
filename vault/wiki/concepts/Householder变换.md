---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 研究]
aliases: ["Householder Reflection", "Householder反射", "Householder矩阵", "QR分解", "QR decomposition", "Householder三角化"]
relates_to:
  - target: "[[阿尔斯顿·豪斯霍尔德]]"
    type: caused
    confidence: 0.95
  - target: "[[QR算法]]"
    type: implements
    confidence: 0.9
    note: Hessenberg化简是QR算法高效实现的关键预处理（每步QR迭代由O(n^3)降为O(n^2)）
  - target: "[[奇异值分解]]"
    type: implements
    confidence: 0.85
    note: Golub-Kahan双对角化（1965）用Householder将矩阵化为双对角形，是SVD计算的标准方法
  - target: "[[Schur分解]]"
    type: implements
    confidence: 0.8
    note: Householder变换是计算Schur分解的工具（先化Hessenberg，再用QR迭代至三角形）
  - target: "[[后向误差分析]]"
    type: related_to
    confidence: 0.85
    note: 正交变换κ(H)=1不放大误差，是Wilkinson后向稳定性分析中"酉变换优越性"论点的核心例证
  - target: "[[条件数]]"
    type: related_to
    confidence: 0.8
    note: 正交矩阵条件数κ=1（最优），这是Householder变换比高斯消元数值稳定的根本原因
supersedes: null
---

# Householder 变换

## 概述

Householder 变换（Householder Reflection）由[[阿尔斯顿·豪斯霍尔德]]于 1958 年提出。定义为 $H = I - 2vv^T/v^Tv$——关于与法向量 $v$ 正交的超平面的镜像反射。核心性质：**正交矩阵**（$H^T H = I$）、**对合**（$H^2 = I$）、**条件数 = 1**（不放大误差）。通过恰当选择 $v$，可以将任意向量 $x$ 一次反射到坐标轴方向（消去多个分量），这使其成为比 Givens 旋转（每次消去一个元素）更高效的 QR 分解工具，计算量从 $O(n^4)$ 降至 $O(n^3)$。

## 关键内容

### 定义与性质

$$H = I - \frac{2vv^T}{v^Tv}, \quad v \in \mathbb{R}^n \setminus \{0\}$$

| 性质 | 说明 |
|------|------|
| 对称性 | $H^T = H$ |
| 正交性 | $H^TH = I$，即 $H^{-1} = H$ |
| 对合性 | $H^2 = I$ |
| 行列式 | $\det(H) = -1$ |
| **条件数** | $\kappa_2(H) = 1$（最优！不放大舍入误差）|
| 几何意义 | 关于法向量 $v$ 的超平面做镜像反射 |

### 核心技巧：消去向量的多个分量

给定向量 $x$，选取 $v = x + \text{sign}(x_1)\|x\|_2 e_1$，则：

$$Hx = -\text{sign}(x_1)\|x\|_2 e_1$$

一次反射消去了 $x$ 的 $n-1$ 个分量（$x_2, \ldots, x_n$ 全变为零）。符号选取 $+\text{sign}(x_1)$ 是为了避免**灾难性对消**（catastrophic cancellation）。

相比 **Givens 旋转**（每次只能消去一个元素），Householder 变换是**批量消去**：

| 方法 | 每步消去 | 化三角形总步数 | 总计算量 |
|------|---------|------------|---------|
| Givens 旋转 | 1 个元素 | $O(n^2)$ 次旋转 | $O(n^4)$ |
| **Householder 变换** | **整列元素** | **$n-1$ 次变换** | **$O(n^3)$** |

### QR 分解

对 $m \times n$ 矩阵 $A$（$m \geq n$），依次应用 $n$ 次 Householder 变换：

$$H_n \cdots H_2 H_1 A = R \quad \Rightarrow \quad A = QR$$

其中 $Q = H_1 H_2 \cdots H_n$（正交），$R$ 为上三角矩阵。

**计算量**：$\frac{2}{3}n^3$（方阵）或 $2mn^2 - \frac{2}{3}n^3$（$m \times n$ 矩阵）

**隐式表示**（重要！）：$H$ 无需显式存储为 $n\times n$ 矩阵，只存储 $v$（$n$ 个数），矩阵-向量乘积：

$$Hx = x - 2\frac{v^Tx}{v^Tv}v \quad [O(n) \text{ 计算，} O(n) \text{ 存储}]$$

### Hessenberg 化简（特征值预处理）

对一般 $n\times n$ 矩阵，通过两侧 Householder 变换（$n-2$ 步）化为**上 Hessenberg 形式**（$h_{ij}=0$ 当 $i>j+1$）：

$$Q^T A Q = H_{\text{Hessenberg}} \quad [\frac{10}{3}n^3 \text{ 次运算}]$$

对**对称矩阵**化为**三对角形式**：$\frac{4}{3}n^3$ 次运算

**意义**：对 Hessenberg 矩阵的 QR 迭代每步仅需 $O(n^2)$（而非 $O(n^3)$），这使[[QR算法]]实际可行。

### 数值稳定性：为何优于 Gauss 消元

Householder 变换（正交变换）的条件数 $\kappa_2(H) = 1$——**不放大误差**。

相比之下，Gauss 消元的增长因子可达 $2^{n-1}$（最坏情况），即使带列主元选取，在某些矩阵上仍不够稳定。

这一优势是[[后向误差分析]]（Wilkinson）所指出的"酉变换的根本优越性"的直接体现：$\kappa(Q) = 1$，正交变换引入的后向误差 $\|\delta A\|/\|A\| \approx \varepsilon_\text{mach}$。

### 主要应用

| 应用 | 说明 |
|------|------|
| QR 分解 | 最稳定的稠密矩阵 QR 分解方法（LAPACK DGEQRF）|
| Hessenberg 化简 | QR 算法特征值计算的预处理（LAPACK DGEHRD）|
| 对称三对角化 | 对称特征值计算预处理（LAPACK DSYTRD）|
| SVD 计算 | Golub-Kahan 双对角化（LAPACK DBDSDC）|
| 最小二乘 | $\min\|Ax-b\|_2$：$A=QR$，解 $Rx=Q^Tb$（比法方程更稳定）|
| 块 Householder（WY 表示）| 现代并行计算中将多个变换合并为 BLAS-3 矩阵-矩阵乘 |

### 局限性

- **破坏稀疏性**：稀疏矩阵经 Householder 变换后一般变为稠密（大规模稀疏特征值问题应用 Lanczos/Arnoldi）
- **顺序依赖**：第 $k$ 步依赖前 $k-1$ 步结果，并行化受限（通信回避算法 TSQR/CAQR 是现代改进方向）
- **与 Givens 互补**：带状矩阵、增量更新 QR 等场景 Givens 旋转更合适

## 来源

- [[raw/books/数值分析/18_householder_transformations.md]]

## 相关

- [[阿尔斯顿·豪斯霍尔德]]
- [[QR算法]]
- [[奇异值分解]]
- [[Schur分解]]
- [[后向误差分析]]
- [[条件数]]
