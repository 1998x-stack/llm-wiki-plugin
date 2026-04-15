---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags:
- 研究
- 技术
- 数值分析
- 矩阵理论
aliases:
- QR Algorithm
- QR迭代
- QR变换
- QR decomposition algorithm
relates_to:
- target: '[[Schur分解]]'
  type: implements
  confidence: 0.95
- target: '[[矩阵理论]]'
  type: part_of
  confidence: 0.85
- target: '[[谱半径]]'
  type: uses
  confidence: 0.8
supersedes: null
---

# QR算法

## 概述

QR算法（QR Algorithm）是计算[[矩阵]]全部特征值（即[[Schur分解]]）的最重要迭代算法，由英国工程师 John G. F. Francis 和苏联数学家 Vera N. Kublanovskaya 于1961年独立发明，被列为"20世纪十大最有影响力的算法"之一。核心思想：对[[矩阵]]反复执行 QR 分解（$A_k = Q_kR_k$），然后颠倒乘法顺序（$A_{k+1} = R_kQ_k = Q_k^*A_kQ_k$），在满足谱间隙条件时，序列 $\{A_k\}$ 收敛到上三角形式——即 $A$ 的 [[伊赛·舒尔|Schur]] 形式。LAPACK、MATLAB 和 NumPy/SciPy 的特征值求解器均以此为核心引擎。

## 关键内容

### 基本迭代

**输入**：$n \times n$ 复方阵 $A_0 = A$

**迭代**：对 $k = 0, 1, 2, \ldots$：
1. [[Householder变换|QR分解]]：$A_k = Q_k R_k$（$Q_k$ 酉，$R_k$ 上三角）
2. 重组：$A_{k+1} = R_k Q_k = Q_k^* A_k Q_k$

**关键性质**：每一步 $A_{k+1}$ 与 $A$ 酉相似，故特征值不变。在适当条件下，$A_k$ 趋向上三角[[矩阵]]（[[Schur分解|Schur形式]]），对角元素收敛到特征值。

### 收敛条件与速率

**收敛条件**：若 $A$ 的特征值满足 $|\lambda_1| > |\lambda_2| > \cdots > |\lambda_n|$（严格分离），则 QR 迭代收敛。

**收敛速率**：第 $(i,i+1)$ 次对角收敛速率约为 $O(|\lambda_{i+1}/\lambda_i|^k)$，与幂法的谱间隙控制相同。

**退化情形**：特征值等模时需要特殊处理（位移策略、双重位移等）。

### 实用改进

**带位移的QR算法**（Francis 1961）：在 QR 分解前减去位移 $\mu_k$：
$$A_k - \mu_k I = Q_k R_k, \quad A_{k+1} = R_k Q_k + \mu_k I$$
[[瑞利勋爵|Rayleigh]] 商位移使收敛从线性加速到三次方，极大提升效率。

**Hessenberg化预处理**：先将 $A$ 化为上 Hessenberg 形（上双对角和对角线以下全零），使每步 QR 分解代价从 $O(n^3)$ 降至 $O(n^2)$。

**隐式 QR（Francis 双重位移）**：使用复共轭位移对处理实[[矩阵]]的复特征值，保持全程在实数算术中进行。

**[[詹姆斯·威尔金森|Wilkinson]] 位移（1965）**：[[詹姆斯·威尔金森]]为对称三对角[[矩阵]]提出的位移策略——选取末部 $2\times 2$ 子[[矩阵]]中更接近 $a_{nn}$ 的特征值作为位移，实现**全局收敛性**和**三次方渐近收敛速率**；实际计算中每个特征值通常只需1–2次迭代即可隔离。是对称特征值计算的黄金标准。

### 历史背景

**Francis（1961）**：发表于 *The Computer Journal*，论文明确指出目标是计算 [[伊赛·舒尔|Schur]] 标准形，使用"QR变换"术语，引入带位移和双步迭代。

**Kublanovskaya（1961）**：发表于 *USSR Computational Mathematics*，从 LQ 分解角度独立构造相同算法。

两人都看到了[[伊赛·舒尔]] 1909年定理的计算潜力——将一个存在性结果（[[Schur分解]]存在）转化为构造性算法（迭代计算 [[伊赛·舒尔|Schur]] 形式）。从 [[伊赛·舒尔|Schur]] 1909年到 Francis/Kublanovskaya 1961年，历经半个世纪。

**"20世纪十大算法"**：该名单由 Dongarra 和 Sullivan（2000）在 *Computing in Science & Engineering* 评选，QR 算法与 Monte Carlo 方法、[[快速傅里叶变换]]、单纯形法等并列其中。

### 现代实现

| 软件/库 | 接口 | 说明 |
|---------|------|------|
| LAPACK | `xGEES`, `xGEEV` | 计算 [[伊赛·舒尔|Schur]] 形或特征值/向量 |
| MATLAB | `schur(A)`, `eig(A)` | 直接调用 LAPACK |
| NumPy/SciPy | `scipy.linalg.schur(A)` | 实/复 [[伊赛·舒尔|Schur]] 形 |
| Julia | `schur(A)` | 调用 LAPACK |

**大规模稀疏[[矩阵]]**：Krylov 子空间方法（如 Arnoldi 算法、ARPACK 库）本质上是在低维投影空间中计算"部分 [[伊赛·舒尔|Schur]] 分解"，只提取少数主要特征值。

## 与其他算法的关系

| 算法 | 关系 |
|------|------|
| 幂法（Power Method） | QR算法的推广——幂法每次只提取一个特征向量，QR算法同时提取全部 |
| LR算法（Rutishauser 1958） | QR算法的前身，用 LR 分解（LU分解）代替 QR；数值不稳定 |
| Lanczos算法 | 用于大规模对称[[矩阵]]，在 Krylov 子空间中隐式执行部分 QR |
| Arnoldi算法 | 非对称大规模[[矩阵]]的 Krylov 方法，计算部分 [[伊赛·舒尔|Schur]] 分解 |

## 来源

- [[raw/books/矩阵分析/08_schur_unitary_triangularization_1909.md]]

## 相关

- [[Schur分解]]
- [[伊赛·舒尔]]
- [[矩阵理论]]
- [[谱半径]]
- [[快速傅里叶变换]]
