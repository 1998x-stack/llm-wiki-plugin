---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [研究, 技术]
aliases: ["Hoffman-Wielandt theorem", "HW不等式", "Hoffman-Wielandt inequality", "正规矩阵特征值扰动"]
relates_to:
  - target: "[[赫尔穆特·维兰特]]"
    type: implements
    confidence: 0.95
  - target: "[[矩阵扰动理论]]"
    type: part_of
    confidence: 0.95
  - target: "[[Weyl特征值不等式]]"
    type: extends
    confidence: 0.9
  - target: "[[正规矩阵]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Von Neumann迹不等式]]"
    type: uses
    confidence: 0.85
  - target: "[[奇异值分解]]"
    type: uses
    confidence: 0.75
supersedes: null
---

# Hoffman-Wielandt定理

## 概述

Hoffman-Wielandt定理（1953）由 Alan J. Hoffman 与[[赫尔穆特·维兰特]]发表于 *Duke Mathematical Journal*（仅三页），给出了[[正规矩阵]]特征值在 Frobenius 范数下的最优整体扰动界：**对两个 $n \times n$ 正规矩阵 $A, B$，存在最优特征值配对排列 $\pi$，使得配对偏差的平方和 $\leq \|A-B\|_F^2$**。这是[[矩阵扰动理论]]的核心结果：不等式是最优的（等号可达），将[[Weyl特征值不等式]]从单个特征值的谱范数控制提升为全部特征值的 Frobenius 范数整体控制，并将分析问题与最优指派（组合优化）优雅联系。

## 关键内容

### 主定理

设 $A, B \in \mathbb{C}^{n \times n}$ 均为正规矩阵（$A^*A = AA^*$，$B^*B = BB^*$），特征值分别为 $\lambda_1,\ldots,\lambda_n$ 和 $\mu_1,\ldots,\mu_n$。则：

$$\min_{\pi \in S_n} \sum_{i=1}^n |\lambda_i - \mu_{\pi(i)}|^2 \leq \|A - B\|_F^2$$

**等价形式**：存在排列 $\pi$，使得：
$$\sum_{i=1}^n |\lambda_i - \mu_{\pi(i)}|^2 \leq \|A - B\|_F^2$$

**等号条件**：$A$ 与 $B$ 可被同一酉矩阵同时对角化，即 $AB = BA$（$A$ 与 $B$ 交换）。此时两矩阵共享特征向量基，$E = B-A$ 在公共特征基下对角化，Frobenius 范数精确等于特征值差的平方和。

### 与 Weyl 不等式的比较

| 性质 | Weyl 不等式（1912） | Hoffman-Wielandt（1953） |
|------|-----------------|------------------------|
| 适用范围 | Hermitian 矩阵 | 所有正规矩阵 |
| 范数类型 | 谱范数 $\|E\|_2$ | Frobenius 范数 $\|E\|_F$ |
| 控制类型 | 逐个特征值 $|\lambda_i - \mu_i|$ | 全局：最优配对平方和 |
| 配对问题 | 按实数升序（自然排序） | 需在 $n!$ 种配对中取最优 |
| 是否最优 | 是（谱范数意义下最优） | 是（Frobenius 范数意义下最优） |

**具体比较（Hermitian 情形）**：
- Weyl：$\sum |\lambda_i - \mu_i|^2 \leq n\|E\|_2^2$（平方求和后变宽松）
- Hoffman-Wielandt：$\sum |\lambda_i - \mu_i|^2 \leq \|E\|_F^2 \leq n\|E\|_2^2$

因此 HW 不等式**严格强于** Weyl 不等式的平方和版本。

### 证明思路（Birkhoff-von Neumann 桥接）

核心方法：将**分析问题**（特征值偏移）化为**凸优化**（双随机矩阵上的线性函数），再用 **Birkhoff 定理**转化为**组合问题**（指派问题）。

1. **酉对角化**：正规矩阵 $A = U\Lambda U^*$，$B = V M V^*$（$\Lambda, M$ 为对角特征值矩阵，$U, V$ 酉）
2. **Frobenius 展开**：令 $W = U^*V$（酉矩阵），则
   $$\|A - B\|_F^2 = \sum_{i,j} |W_{ij}|^2 |\lambda_i - \mu_j|^2$$
3. **双随机矩阵**：$S_{ij} = |W_{ij}|^2$ 是双随机矩阵（行列和均为1，元素非负）
4. **Birkhoff-von Neumann 定理**：$\sum_{i,j} S_{ij}|\lambda_i - \mu_j|^2$ 是 $S$ 的线性函数，在 Birkhoff 多面体（双随机矩阵集合）的顶点（= 置换矩阵）处取极小值。因此存在排列 $\pi$：
   $$\min_\pi \sum_i|\lambda_i - \mu_{\pi(i)}|^2 \leq \sum_{i,j} S_{ij}|\lambda_i - \mu_j|^2 = \|A-B\|_F^2$$

**指派问题解读**：左端的最优配对问题恰好是经典**指派问题**（assignment problem），可用匈牙利算法（Hungarian algorithm）在 $O(n^3)$ 时间求解。HW 定理给出其最优解的上界。

**与 von Neumann 迹不等式的联系**：两者证明技术完全相同（SVD/对角化 → 双随机矩阵 → Birkhoff 定理 → 排序不等式），是"双随机矩阵 + Birkhoff 定理"方法论的两个典范应用。

### 正规性限制

定理**仅适用于正规矩阵**（$A^*A = AA^*$）。对非正规矩阵，特征值可对扰动任意敏感：

- $n$ 阶 Jordan 块 $J_n$（特征值全为0）受 $\varepsilon$ 扰动后，特征值偏移为 $\varepsilon^{1/n} \gg \varepsilon$
- 需要 **Bauer-Fike 定理**（涉及特征向量矩阵条件数 $\kappa(V)$）或**伪谱**理论处理非正规情形

### 最优输运联系

HW 不等式左端等于两个经验谱测度之间的 **2-Wasserstein 距离的平方**（除以 $n$）：

$$W_2^2(\mu_A, \mu_B) = \frac{1}{n} \min_\pi \sum_i |\lambda_i - \mu_{\pi(i)}|^2 \leq \frac{\|A-B\|_F^2}{n}$$

这将矩阵扰动理论与最优输运理论连接，为谱测度的 Wasserstein 连续性提供了矩阵层面的刻画。

## 应用

**数值特征值算法（QR算法等）**：后向误差分析的核心工具——算法输出的特征值是近似矩阵 $\hat A = A + E$ 的精确特征值，HW 保证整体误差 $\leq \|E\|_F$。

**高维统计（协方差矩阵）**：样本协方差 $\hat\Sigma = \Sigma + E$ 的特征值（主成分方差）与总体特征值之间的 Frobenius 整体偏差有界。

**随机矩阵理论**：Wigner 半圆律的证明中，截断/中心化操作的正当性由 HW 保证——$\|A-B\|_F$ 的控制直接给出特征值分布的整体控制。

**量子信息**：密度矩阵特征值（量子态谱）的 Frobenius 扰动控制，与量子保真度和纠缠度量的连续性直接相关。

**网络科学**：图邻接矩阵/Laplacian（实对称矩阵，正规矩阵特例）在边扰动下，谱整体偏移由 $\|E\|_F$ 控制，为动态网络分析提供鲁棒性保证。

## 局限性

1. **正规性本质性**：非正规矩阵无类似结论
2. **整体不精确**：不控制单个特征值（需 Weyl 不等式），且不涉及特征向量/不变子空间（需 Davis-Kahan 定理）
3. **不提供最优配对的构造**：需额外运行匈牙利算法找到 $\pi$
4. **Frobenius 范数仅给 $\ell^2$-整体控制**：$\ell^1$ 或 $\ell^\infty$ 控制需其他工具

## 来源

- raw/books/矩阵分析/13_hoffman_wielandt_theorem_1953.md

## 相关

- [[赫尔穆特·维兰特]]
- [[矩阵扰动理论]]
- [[正规矩阵]]
- [[Weyl特征值不等式]]
- [[Von Neumann迹不等式]]
- [[优化控制序]]
