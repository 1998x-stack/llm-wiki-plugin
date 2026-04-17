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
- Ky Fan inequality
- Fan不等式
- Ky Fan极值原理
- Fan k-范数
- Fan控制定理
- Ky Fan dominance
relates_to:
- target: '[[樊畿]]'
  type: implements
  confidence: 0.95
- target: '[[Weyl特征值不等式]]'
  type: extends
  confidence: 0.95
- target: '[[极大极小定理]]'
  type: extends
  confidence: 0.9
- target: '[[优化控制序]]'
  type: caused
  confidence: 0.9
- target: '[[Von Neumann迹不等式]]'
  type: extends
  confidence: 0.85
- target: '[[奇异值分解]]'
  type: depends_on
  confidence: 0.85
supersedes: null
---

# Ky Fan不等式

## 概述

[[樊畿|Ky Fan]]不等式（1949–1951）由[[樊畿]]在三篇 PNAS 论文中建立，将[[Weyl特征值不等式]]从单个特征值的逐项控制提升为**特征值部分和的整体控制**。核心内容：(1) **Fan极值原理**——前 $k$ 个最大特征值之和等于 Hermitian [[矩阵]]在所有 $k$ 维子空间上"限制迹"的最大值；(2) **Fan部分和不等式**——$\sum_{i=1}^k\lambda_i(A+B) \leq \sum_{i=1}^k\lambda_i(A)+\sum_{i=1}^k\lambda_i(B)$；(3) **Fan控制定理**——所有 [[樊畿|Ky Fan]] $k$-范数的控制等价于所有酉不变范数的控制。这套理论统一了特征值不等式与酉不变范数，是[[优化控制序]] (Majorization) 理论的核心组成，并直接催生了 Horn 猜想的提出。

## 关键内容

### 定理一：Ky Fan 极值原理

设 $A$ 为 $n \times n$ Hermitian [[矩阵]]，特征值降序排列 $\lambda_1 \geq \cdots \geq \lambda_n$。则：

$$\sum_{i=1}^{k} \lambda_i(A) = \max_{\dim V = k} \operatorname{tr}(P_V A P_V) = \max_{\substack{v_1,\ldots,v_k \\ \text{标准正交}}} \sum_{j=1}^k \langle Av_j, v_j\rangle$$

其中 $P_V$ 是到 $k$ 维子空间 $V$ 的正交投影。

**与 Courant-[[恩斯特·菲舍尔|Fischer]] 比较**：
- Courant-[[恩斯特·菲舍尔|Fischer]]：$\lambda_k = \max_{\dim V=k} \min_{x\in V, \|x\|=1} \langle Ax,x\rangle$（极大**极小**）
- Fan极值原理：$\sum_{i=1}^k\lambda_i = \max_{\dim V=k} \operatorname{tr}(P_VAP_V)$（纯粹**极大**）

Fan 的形式更简洁：把内层的"在 $V$ 中取极小"替换为"对 $V$ 求迹"，同时刻画了前 $k$ 个特征值的**和**而非单个特征值。

### 定理二：Ky Fan 部分和不等式

设 $A, B$ 为 $n \times n$ Hermitian [[矩阵]]，对任意 $1 \leq k \leq n$：

$$\sum_{i=1}^{k} \lambda_i(A+B) \leq \sum_{i=1}^{k} \lambda_i(A) + \sum_{i=1}^{k} \lambda_i(B)$$

**与 Weyl 不等式的关系**：
- $k=1$：退化为 $\lambda_1(A+B) \leq \lambda_1(A)+\lambda_1(B)$（Weyl 特例）
- $k=n$：两端均为 $\operatorname{tr}(A+B) = \operatorname{tr}(A)+\operatorname{tr}(B)$（等式）
- 随 $k$ 增大，不等式逐渐趋向等式——Fan不等式是连接 Weyl（$k=1$）与迹等式（$k=n$）的一族不等式

**证明**（极值原理的直接推论）：由极值原理，存在最优子空间 $V^*$ 使左端取最大值；在该子空间上，两项分别 $\leq$ 对应的部分和上界，相加即得。

**Majorization 表述**：Fan 不等式等价于弱[[优化控制序]] $\lambda(A+B) \prec_w \lambda(A)+\lambda(B)$（详见[[优化控制序]]）。

### 定理三：Ky Fan $k$-范数与控制定理

**定义**（Fan $k$-范数）：对任意 $n \times n$ [[矩阵]] $X$：
$$\|X\|_{(k)} = \sum_{i=1}^{k} \sigma_i(X), \quad 1 \leq k \leq n$$

其中 $\sigma_1 \geq \cdots \geq \sigma_n \geq 0$ 为[[奇异值分解|奇异值]]（[[奇异值分解]]）。

| $k$ | Fan $k$-范数 | 别名 |
|-----|------------|------|
| $1$ | $\sigma_1(X)$ | 谱范数（算子范数、$\ell^\infty$ Schatten） |
| $2,\ldots,n-1$ | $\sum_{i=1}^k\sigma_i$ | 中间 Fan 范数 |
| $n$ | $\sum_{i=1}^n\sigma_i$ | 核范数（迹范数，Schatten 1-范数） |

**Fan 控制定理**：对 $n \times n$ [[矩阵]] $A, B$，以下等价：

$$\|A\|_{(k)} \leq \|B\|_{(k)}, \; \forall k = 1,\ldots,n \quad \Longleftrightarrow \quad \||A\|| \leq \||B\||, \; \forall \text{ 酉不变范数 } \||\cdot|\|$$

**意义**：有限个 Fan $k$-范数的比较完全决定了无限多个酉不变范数的比较。Fan 范数是酉不变范数锥的"极端射线"——它们是"最尖锐"的酉不变范数。

### 证明方法

三种核心技术的有机结合：

1. **变分方法**：将特征值部分和化为 Grassmann 流形上的优化问题
2. **维数论证**：若 $\dim V + \dim W > n$，则 $V \cap W \neq \{0\}$；用于在子空间交点处建立约束
3. **Courant-[[恩斯特·菲舍尔|Fischer]] 推广**：将单向量 [[瑞利勋爵|Rayleigh]] 商替换为 $k$ 维子空间上的限制迹

### 后续影响

**Horn 猜想（1962→1999）**：Alfred Horn 受 Fan 不等式启发，提出 Hermitian [[矩阵]]特征值和的完整充要约束（递归不等式系统）。Fan 不等式对应于最简单的情形（连续前 $k$ 项）。Klyachko（1998）和 Knutson-Tao（1999）通过 Schubert 演算、蜂巢模型最终解决。

**Lidskii-Mirsky-[[赫尔穆特·维兰特|Wielandt]] 定理（1950）**：$\lambda(A)-\lambda(B) \prec \lambda(A-B)$，用 [[优化控制序|majorization]] 统一了扰动不等式。

**Thompson-Freede 定理（1971）**：将 Fan 类型不等式推广到非连续指标集，预示了 Horn 猜想的完整形式。

## 应用

**量子信息**：密度[[矩阵]]特征值的 [[优化控制序|majorization]] 关系是量子纠缠转换可行性的充要条件（Nielsen 1999）；von Neumann 熵次可加性依赖 Fan 型特征值控制。

**主成分分析**：PCA 寻求最大化数据协方差[[矩阵]]在 $k$ 维子空间上的限制迹——这正是 Fan 极值原理。

**核范数正则化**（推荐系统/[[矩阵]]补全）：核范数（Fan $n$-范数）作为秩的凸松弛，其理论基础在 Fan 控制定理中。

**MIMO 通信**：信道[[矩阵]][[奇异值分解|奇异值]]决定子[[信道容量]]，Fan 范数为容量部分和提供框架。

## 来源

- [[raw/books/矩阵分析/12_ky_fan_matrix_inequalities_1951.md]]

## 相关

- [[樊畿]]
- [[Weyl特征值不等式]]
- [[优化控制序]]
- [[Von Neumann迹不等式]]
- [[极大极小定理]]
- [[奇异值分解]]
