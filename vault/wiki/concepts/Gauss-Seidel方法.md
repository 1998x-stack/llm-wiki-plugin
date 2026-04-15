---
type: concept
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 研究]
aliases: ["Gauss-Seidel Method", "逐次位移法", "method of successive displacements", "高斯-赛德尔迭代"]
relates_to:
  - target: "[[菲利普·路德维希·冯·赛德尔]]"
    type: caused
    confidence: 0.85
    note: 赛德尔1874年正式发表逐次位移法
  - target: "[[Jacobi迭代法]]"
    type: extends
    confidence: 0.9
    note: 同类迭代框架，利用最新值代替旧值
  - target: "[[谱半径]]"
    type: depends_on
    confidence: 0.9
    note: 迭代矩阵 B_GS = -(D+L)^{-1}U 的谱半径<1 是收敛充要条件
  - target: "[[卡尔·弗里德里希·高斯]]"
    type: related_to
    confidence: 0.6
    note: 以高斯命名但历史文献未确认高斯明确使用过此方法
supersedes: null
---

# Gauss-Seidel 方法

## 概述

Gauss-Seidel 方法（亦称逐次位移法）是求解线性方程组 $Ax=b$ 的迭代算法，由[[菲利普·路德维希·冯·赛德尔]]于 1874 年正式发表。与[[Jacobi迭代法]]的核心区别在于：计算第 $i$ 个分量时，立即使用本轮已更新的分量值（而非全部用旧值），因此通常收敛更快，但存在顺序依赖，天然并行性弱于 Jacobi 方法。

## 关键内容

### 迭代格式

$$x_i^{(k+1)} = \frac{1}{a_{ii}}\!\left(b_i - \sum_{j<i} a_{ij}x_j^{(k+1)} - \sum_{j>i} a_{ij}x_j^{(k)}\right)$$

与 Jacobi 方法的区别：$j<i$ 的分量使用已更新的 $x_j^{(k+1)}$，而非旧值 $x_j^{(k)}$。

矩阵形式：$x^{(k+1)} = -(D+L)^{-1}Ux^{(k)} + (D+L)^{-1}b$，迭代矩阵 $B_{GS} = -(D+L)^{-1}U$。

### 收敛性质

**充要条件**：[[谱半径]] $\rho(B_{GS}) < 1$。

**充分条件**（与 Jacobi 相同）：严格对角占优或对称正定。

对于来自偏微分方程离散化（如离散 Laplacian）的矩阵，Gauss-Seidel 的谱半径平方近似等于 Jacobi 的谱半径，即 $\rho(B_{GS}) \approx \rho(B_J)^2$，理论上每步迭代效果翻倍。

### 与 Jacobi 方法对比

| 特性 | Jacobi | Gauss-Seidel |
|------|--------|--------------|
| 更新方式 | 全用旧值，同步 | 即用新值，顺序 |
| 收敛速度 | 通常较慢 | 通常较快（约翻倍） |
| 并行化 | 天然并行 | 依赖更新顺序，难以并行 |
| 内存 | 需存新旧两份向量 | 原地更新，节省内存 |
| 适用场景 | GPU/分布式计算 | 串行单线程计算 |

### 命名中的历史争议

方法以"高斯-赛德尔"命名，但[[卡尔·弗里德里希·高斯]]是否明确使用过这种迭代法存在学术争议。一些历史学家认为高斯在私人计算中可能使用过类似方法（因用途与他广泛使用的最小二乘法相关），但没有明确文献记录；赛德尔 1874 年的论文才是可考的正式发表。

### 后续发展

Gauss-Seidel 方法是 **SOR 方法**（Successive Over-Relaxation）的直接前身。引入松弛参数 $\omega$：

$$x_i^{(k+1)} = (1-\omega)x_i^{(k)} + \omega \cdot \text{(Gauss-Seidel更新值)}$$

David M. Young（1950年博士论文）证明对特定结构矩阵存在最优 $\omega_{\text{opt}}$，使谱半径最小化，大幅优于基础 Gauss-Seidel。

## 来源

- [[raw/books/数值分析/06_jacobi_iteration.md]]

## 相关

- [[菲利普·路德维希·冯·赛德尔]]
- [[Jacobi迭代法]]
- [[谱半径]]
- [[卡尔·弗里德里希·高斯]]
