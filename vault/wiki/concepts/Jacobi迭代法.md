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
- Jacobi Iterative Method
- 同时位移法
- method of simultaneous displacements
relates_to:
- target: '[[卡尔·古斯塔夫·雅各布·雅可比]]'
  type: caused
  confidence: 0.95
- target: '[[谱半径]]'
  type: depends_on
  confidence: 0.9
  note: 迭代矩阵谱半径 ρ(B_J)<1 是收敛的充要条件
- target: '[[Gauss-Seidel方法]]'
  type: related_to
  confidence: 0.9
  note: 同期发展的互补迭代方法，各有优劣
- target: '[[矩阵理论]]'
  type: extends
  confidence: 0.8
  note: 基于矩阵分裂 A=D+L+U 的迭代框架
- target: '[[高斯求积公式]]'
  type: related_to
  confidence: 0.6
  note: 雅可比同时研究最小二乘法（Gauss求积驱动力）与线性方程组迭代求解
supersedes: null
---

# Jacobi 迭代法

## 概述

Jacobi 迭代法是求解线性方程组 $Ax=b$ 的经典迭代方法，由[[卡尔·古斯塔夫·雅各布·雅可比]]约于 1845 年提出。核心思想是将系数[[矩阵]]分裂为对角部分与非对角部分（$A=D+L+U$），利用旧值同步更新所有分量，在对角占优等条件下保证收敛。其"同时更新"特性使它天然适合并行计算，并开创了迭代求解线性方程组的整个[[规范化理论|范式]]。

## 关键内容

### 矩阵分裂与迭代格式

将 $A=D+L+U$（$D$ 对角，$L$ 严格下三角，$U$ 严格上三角），方程组改写为：

$$x^{(k+1)} = D^{-1}(b - (L+U)x^{(k)})$$

分量形式：

$$x_i^{(k+1)} = \frac{1}{a_{ii}}\!\left(b_i - \sum_{j \neq i} a_{ij} x_j^{(k)}\right), \quad i=1,\ldots,n$$

**关键特征**：计算 $x^{(k+1)}$ 时全部使用上一步旧值 $x^{(k)}$，所有分量**同时更新**（simultaneous displacements）。

### 收敛理论

**充要条件**：Jacobi 迭代收敛当且仅当迭代[[矩阵]] $B_J = -D^{-1}(L+U)$ 的[[谱半径]] $\rho(B_J) < 1$。

**充分条件——严格对角占优**：若 $|a_{ii}| > \sum_{j\neq i}|a_{ij}|$ 对所有 $i$ 成立，则对任意初始值收敛。直觉：对角元素主导每个方程，各未知数近乎独立可解。

**充分条件——对称正定**：若 $A$ 对称正定且 $2D-A$ 也正定，则收敛。

**收敛速率**：$R = -\log_{10}\rho(B_J)$，每步误差缩小为原来的 $\rho(B_J)$ 倍；误差界 $\|x^{(k)}-x^*\| \leq \rho(B_J)^k\|x^{(0)}-x^*\|$。

### Jacobi 与 Gauss-Seidel 的核心对比

| 维度 | Jacobi | [[Gauss-Seidel方法]] |
|------|--------|---------------------|
| 更新策略 | 同时（simultaneous）| 逐次（successive）|
| 收敛速度 | 通常较慢 | 通常较快（利用最新值）|
| 并行性 | 天然并行 | 存在顺序依赖 |
| 收敛条件 | 需要 $\rho(B_J)<1$ | 不同迭代[[矩阵]]，条件略有差异 |
| 内存 | 需两份 $x^{(k)}$ 和 $x^{(k+1)}$ | 原地更新（in-place）|

### 加权 Jacobi 与松弛

引入松弛参数 $\omega$ 得加权 Jacobi：

$$x^{(k+1)} = (1-\omega)x^{(k)} + \omega D^{-1}(b-(L+U)x^{(k)})$$

$\omega=1$ 退化为原始方法；适当选取 $\omega$ 可加速收敛，这为后来的 SOR 方法（Successive Over-Relaxation，David M. Young，1950）埋下伏笔。

### 历史背景

动机来自 19 世纪天文学：行星轨道摄动理论需要求解大规模但对角占优的线性方程组，直接法的 $O(n^3)$ 计算量在手工计算时代难以承受。相关思想散见于雅可比 1845 年（Astronomische Nachrichten）和 1846 年（Crelle's Journal）的论文——"Jacobi 迭代法"是后人对其方法的总结命名，并非雅可比自己的称谓。

### 后续影响

| 方向 | 代表成果 |
|------|---------|
| SOR 方法 | David M. Young（1950），对特定结构[[矩阵]]存在最优 $\omega_{\text{opt}}$，大幅加速 |
| [[矩阵]]分裂理论 | Richard Varga《[[矩阵|Matrix]] Iterative Analysis》（1962），系统化 $A=M-N$ 框架 |
| 块 Jacobi / 区域分解 | 标量分量推广为向量块，现代并行有限元核心 |
| Krylov 预条件 | Jacobi 预条件（$M=D$）是最简且效果常出人意料的预条件器 |
| 多重网格光滑子 | Jacobi 迭代消除高频误差，与粗网格校正配合实现 $O(n)$ 最优复杂度 |
| 异步迭代 | Chazan & Miranker（1969），[[分布式系统|分布式计算]]中允许使用"过时"数据仍收敛 |
| GPU 计算 | 同时更新天然映射到 GPU 大规模并行核心 |

### 局限性

- **收敛慢**：对 PDE 离散化（如 Laplacian），$\rho(B_J) = \cos(\pi/n) \approx 1 - \pi^2/(2n^2)$，误差减小一个数量级需 $O(n^2)$ 次迭代；SOR/CG/多重网格显著更快
- **不通用**：对非对角占优[[矩阵]]可能发散
- **不利用最新值**：串行环境下每步信息"过时"，是相较 Gauss-Seidel 的主要缺点

## 来源

- [[raw/books/数值分析/06_jacobi_iteration.md]]

## 相关

- [[卡尔·古斯塔夫·雅各布·雅可比]]
- [[谱半径]]
- [[Gauss-Seidel方法]]
- [[矩阵理论]]
