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
- 数值分析
aliases:
- Krylov Subspace Methods
- Krylov Methods
- Krylov子空间
- Krylov subspace
relates_to:
- target: '[[共轭梯度法]]'
  type: related_to
  confidence: 0.95
  note: CG是Krylov方法家族中最早也是最重要的成员（1952）
- target: '[[Jacobi迭代法]]'
  type: extends
  confidence: 0.7
  note: Krylov方法是对经典定点迭代法的根本性超越，收敛率从O(1/κ)改善为O(1/√κ)
- target: '[[条件数]]'
  type: depends_on
  confidence: 0.85
  note: Krylov方法的收敛速率由条件数（或特征值分布）决定
- target: '[[快速傅里叶变换]]'
  type: related_to
  confidence: 0.5
  note: 两者均是20世纪十大算法，均改变了大规模计算的可行性边界
supersedes: null
---

# Krylov 子空间方法

## 概述

Krylov 子空间方法（Krylov Subspace Methods）是现代大规模[[线性代数]]计算的核心方法族，以苏联数学家 Aleksei Nikolaevich Krylov（1863–1945）命名其使用的子空间。核心思想是：在 $k$ 步[[矩阵]]-向量乘法生成的 $k$ 维子空间 $K_k(A, v) = \text{span}\{v, Av, A^2v, \ldots, A^{k-1}v\}$ 中寻找最优近似解，每步只需一次[[矩阵]]-向量乘法，能高效利用[[矩阵]]稀疏性。[[共轭梯度法]]（1952）是其第一个也是最重要的成员，后续发展出 GMRES、Lanczos、Arnoldi 等方法，构成了当代科学计算不可或缺的工具集。

## 关键内容

### Krylov 子空间

$$K_k(A, v) = \text{span}\{v, Av, A^2v, \ldots, A^{k-1}v\}$$

**关键性质**：
- 仅通过[[矩阵]]-向量乘法生成，无需显式存储[[矩阵]]（对稀疏[[矩阵]]尤为有利）
- 维数最多为 $n$，$k=n$ 时涵盖整个解空间
- 与[[矩阵]]的**谱结构**深刻关联：特征值聚集 → 更快收敛

### 方法家族

| 方法 | 年份 | 目标方程 | 最优准则 |
|------|------|---------|---------|
| **Lanczos** | 1950 | 对称[[矩阵]]特征值 | 三对角化 |
| **CG** | 1952 | SPD 线性方程组 | $A$-范数最小残差 |
| **MINRES** | 1975 | 对称不定方程组 | $\ell^2$ 残差最小 |
| **Arnoldi** | 1951/1975 | 非对称[[矩阵]]特征值 | Hessenberg化 |
| **BiCG** | 1976 | 非对称方程组 | 双正交化 |
| **GMRES** | 1986 | 非对称方程组 | $\ell^2$ 残差最小 |
| **BiCGSTAB** | 1992 | 非对称方程组 | 稳定BiCG |
| **QMR** | 1991 | 非对称方程组 | 准极小残差 |

### 与经典迭代法的根本区别

**经典定点迭代**（Jacobi/Gauss-Seidel）：$x^{(k+1)} = g(x^{(k)})$，每步从上一步单一迭代点出发，收敛率固定为[[谱半径]] $\rho(B) < 1$。

**Krylov 方法**：$x_k \in x_0 + K_k(A, r_0)$，在递增子空间中寻找最优解，利用全部历史信息，收敛率随步数动态改善。

**核心优势**：
- 利用**所有**前 $k$ 步[[矩阵]]-向量乘法的信息（而非仅用最新一步）
- 收敛率由[[条件数]]**平方根**决定（CG），优于经典方法的[[条件数]]本身
- 对稀疏[[矩阵]]高效：每步 $O(\text{nnz})$ 次运算（nnz = 非零元素数）

### CG-Lanczos 深层联系

[[共轭梯度法]]中产生的三项递推关系与 Lanczos 算法产生的三对角[[矩阵]]之间存在精确对应：

$$\text{Lanczos 三对角化} \iff \text{CG 递推关系}$$

两者都在同一个 Krylov 子空间中工作，数学核心相同，只是"输出目标"不同（特征值 vs 线性方程组解）。这一深层联系在 1970 年代被完全阐明。

### 预处理

所有 Krylov 方法都可以配合预处理器（preconditioner）$M \approx A$：

$$M^{-1}A x = M^{-1}b \quad \Rightarrow \quad \kappa(M^{-1}A) \ll \kappa(A)$$

预处理是让 Krylov 方法实用的关键技术，也是当代数值[[线性代数]]最活跃的研究方向之一。

## 来源

- [[raw/books/数值分析/15_conjugate_gradient.md]]

## 相关

- [[共轭梯度法]]
- [[条件数]]
- [[Jacobi迭代法]]
- [[快速傅里叶变换]]
