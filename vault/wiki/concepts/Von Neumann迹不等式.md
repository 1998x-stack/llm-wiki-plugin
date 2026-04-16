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
- von Neumann trace inequality
- 迹不等式
- Von Neumann不等式
- trace inequality
relates_to:
- target: '[[约翰·冯·诺依曼]]'
  type: implements
  confidence: 0.95
- target: '[[奇异值分解]]'
  type: depends_on
  confidence: 0.95
- target: '[[矩阵理论]]'
  type: part_of
  confidence: 0.9
- target: '[[Weyl特征值不等式]]'
  type: extends
  confidence: 0.75
- target: '[[Schur分解]]'
  type: uses
  confidence: 0.7
supersedes: null
---

# Von Neumann迹不等式

## 概述

Von Neumann迹不等式（1937）由[[约翰·冯·诺依曼]]发表于 *Tomsk University Review*，建立了两个复[[矩阵]]迹内积绝对值的最优上界：**对任意 $n \times n$ 复[[矩阵]] $A$ 和 $B$，有 $|\operatorname{tr}(A^*B)| \leq \sum_{i=1}^n \sigma_i(A)\sigma_i(B)$**，其中 $\sigma_i$ 为降序[[奇异值分解|奇异值]]。等号成立当且仅当 $A$ 与 $B$ 的[[奇异值分解]]共享同一对酉[[矩阵]]（主轴完全对齐）。该定理揭示了[[矩阵]]迹内积完全被各自[[奇异值分解|奇异值]]所控制，奠定了酉不变范数理论基础，催生了核范数在[[矩阵]]补全和低秩优化中的应用。

## 关键内容

### 主定理

设 $A, B \in \mathbb{C}^{n \times n}$，[[奇异值分解|奇异值]]降序排列为 $\sigma_1(A) \geq \cdots \geq \sigma_n(A) \geq 0$（$B$ 类似），则：

$$|\operatorname{tr}(A^*B)| \leq \sum_{i=1}^n \sigma_i(A)\,\sigma_i(B)$$

**等价极值形式**：对固定的 $A, B$，

$$\max_{U,V \text{ 为酉[[矩阵]]}} \operatorname{Re}\,\operatorname{tr}(U A V B) = \sum_{i=1}^n \sigma_i(A)\,\sigma_i(B)$$

**等号成立条件**：存在酉[[矩阵]] $U, V$ 使 $A = U\Sigma_A V^*$ 且 $B = U\Sigma_B V^*$，即 $A$ 与 $B$ 共享奇异向量对。

### 证明思路

1. **[[奇异值分解|SVD]] 标准化**：$A = U_A\Sigma_A V_A^*$，$B = U_B\Sigma_B V_B^*$，代入后迹变为 $\operatorname{tr}(\Sigma_A W \Sigma_B)$，其中 $W = V_A^* U_B$ 为酉[[矩阵]]
2. **双随机[[矩阵]]**：酉[[矩阵]] $W$ 的元素模方构成双随机[[矩阵]] $M_{ij} = |W_{ij}|^2$（行列和均为1）
3. **Birkhoff定理**：双随机[[矩阵]]是置换[[矩阵]]的凸组合
4. **排序不等式**：凸组合中以恒等排列取得最大值（大配大、小配小），得到 $\sum_i\sigma_i(A)\sigma_i(B)$

Mirsky（1975）给出了只有4页的自足简化证明，成为现代教科书标准。

### 奇异值解释

迹不等式的直觉：$\operatorname{tr}(A^*B)$ 是[[矩阵]] $A$ 和 $B$ 之间的"广义内积"，度量其相似程度。[[奇异值分解|奇异值]] $\sigma_i$ 刻画[[矩阵]]沿各主轴的"伸缩强度"。不等式的含义：**不论两[[矩阵]]的主轴方向如何，它们的内积不超过各方向伸缩强度的最优有序匹配**——"大配大、小配小"永远是上界。

### 酉不变范数与对称规范函数

von Neumann 在同论文中建立了：

> [[矩阵]]范数 $\||\cdot|\|$ 酉不变（$\|UAV\| = \|A\|$ 对所有酉[[矩阵]] $U,V$）$\iff$ $\exists$ 向量空间 $\mathbb{R}^n$ 上的**对称规范函数** $g$，使 $\|A\| = g(\sigma_1(A),\ldots,\sigma_n(A))$

由此生成的范数族（Schatten 范数）：

| 名称 | 定义 | 别名 |
|------|------|------|
| 核范数（Schatten 1-范数） | $\sum_i \sigma_i(A)$ | 迹范数（trace norm） |
| [[格奥尔格·弗罗贝尼乌斯|Frobenius]] 范数（Schatten 2-范数） | $\sqrt{\sum_i \sigma_i(A)^2}$ | Hilbert-Schmidt 范数 |
| 谱范数（Schatten $\infty$-范数） | $\sigma_1(A)$（最大[[奇异值分解|奇异值]]） | 算子范数 |

### 主要推广

**[[樊畿|Ky Fan]] [[矩阵]]不等式（1949–1951）**：[[樊畿]]在普林斯顿与 von Neumann 的交流启发下，建立了特征值部分和的极值原理和 Fan $k$-范数（$\sum_{i=1}^k\sigma_i(A)$），并证明所有 [[樊畿|Ky Fan]] $k$-范数被控制 $\Leftrightarrow$ 所有酉不变范数被控制（Fan 控制定理）。这是 von Neumann 迹不等式思想在范数理论中的系统延伸。详见 [[Ky Fan不等式]]。

**Mirsky 1960**：Eckart-Young 低秩逼近最优性从 [[格奥尔格·弗罗贝尼乌斯|Frobenius]]/谱范数推广到所有酉不变范数——截断 [[奇异值分解|SVD]] 在任意酉不变范数下均给出最优低秩逼近。

**Kristof 1969**：推广到多[[矩阵]]乘积 $\operatorname{tr}(Z_1A_1Z_2A_2\cdots)$ 的极值问题。

**Schatten类（1960）**：将有限维理论推广到无穷维 Hilbert 空间上的紧算子，核范数推广为 Schatten 1-范数。

## 现代应用

**[[矩阵]]补全（推荐系统）**：核范数作为[[矩阵]]秩的凸松弛，用于从部分观测恢复低秩[[矩阵]]。[[Netflix Prize]] 问题的核心。Candes & Recht（2009）在不相干条件下证明核范数最小化精确恢复低秩[[矩阵]]。

**低秩[[矩阵]]逼近（数据压缩）**：截断 [[奇异值分解|SVD]] 在迹内积意义下保留最大"信息量"——von Neumann 迹不等式是其最优性证明的核心。图像压缩、信号降噪、基因组降维均依赖此框架。

**主成分分析（PCA）**：截断 [[奇异值分解|SVD]] 给出的子空间在迹内积意义下是最优投影。

**量子信息**：密度[[矩阵]]的迹范数（Schatten 1-范数）是量子态可区分度的基本度量，量子[[信道容量]]的核心工具。

**核范数正则化**：类比 L1 范数产生稀疏解，核范数正则化产生低秩解，广泛用于[[多任务学习]]、鲁棒 PCA、[[矩阵]]分类。

## 局限性

1. **有限维**：推广到无穷维 Hilbert 空间需要 Schatten 类条件
2. **等号难验证**：要求共享奇异向量，[[数值分析|数值计算]]中近乎不可达
3. **仅给上界**：不提供下界（Ruhe 1970 年补充正定[[矩阵]]下界）
4. **非交换结构**：推广到半单 Lie 群需全新工具（Tam 等，2015）

## 来源

- [[raw/books/矩阵分析/11_von_neumann_trace_inequality_1937.md]]

## 相关

- [[约翰·冯·诺依曼]]
- [[奇异值分解]]
- [[矩阵理论]]
- [[Weyl特征值不等式]]
- [[Schur分解]]
