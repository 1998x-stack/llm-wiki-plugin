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
- 矩阵理论
aliases:
- Rayleigh Quotient
- 瑞利商
- Rayleigh-Ritz商
relates_to:
- target: '[[极大极小定理]]'
  type: used_by
  confidence: 0.95
- target: '[[矩阵理论]]'
  type: part_of
  confidence: 0.9
- target: '[[瑞利勋爵]]'
  type: implements
  confidence: 0.95
- target: '[[恩斯特·菲舍尔]]'
  type: used_by
  confidence: 0.9
supersedes: null
---

# Rayleigh商

## 概述

[[瑞利勋爵|Rayleigh]]商（[[瑞利勋爵|Rayleigh]] Quotient）是实对称[[矩阵]] A 关于非零向量 x 定义的标量函数：R(x) = xᵀAx / xᵀx。其值域恰好是 A 的特征值区间 [λ_min, λ_max]，在特征向量处取得相应特征值。由[[瑞利勋爵]]1877年在声学和振动分析中引入，用于将最小特征值（基频）表达为变分极小值；后被[[恩斯特·菲舍尔]]扩展为[[极大极小定理]]的核心工具，将所有特征值统一纳入变分框架。

## 关键内容

### 定义

对于 n×n 实对称[[矩阵]] A，[[瑞利勋爵|Rayleigh]]商为：

$$R(x) = \frac{x^T A x}{x^T x}, \quad x \in \mathbb{R}^n \setminus \{0\}$$

等价地，对 Hermite [[矩阵]]：

$$R(x) = \frac{x^* A x}{x^* x}, \quad x \in \mathbb{C}^n \setminus \{0\}$$

注：R(x) 对标量缩放不变（R(αx) = R(x)），可以等价地限制在单位球面上。

### 基本性质

设 A 的特征值降序为 λ₁ ≥ λ₂ ≥ … ≥ λₙ，对应正交特征向量 v₁,…,vₙ：

| 性质 | 表达式 |
|------|-------|
| 值域 | λₙ ≤ R(x) ≤ λ₁ |
| 最大值 | max R(x) = λ₁，在 v₁ 处取得 |
| 最小值 | min R(x) = λₙ，在 vₙ 处取得 |
| 特征向量处 | R(vᵢ) = λᵢ |
| 加权平均 | R(x) = Σλᵢyᵢ²/Σyᵢ²，其中 y = Qᵀx |

最后一式将 R(x) 表达为特征值的凸组合，权重由 x 在特征向量基下的坐标决定。

### Rayleigh 的物理起源

在弹性/声学系统中（刚度[[矩阵]] K，质量[[矩阵]] M），广义 [[瑞利勋爵|Rayleigh]]商为：

$$R(x) = \frac{x^T K x}{x^T M x}$$

物理意义：**弹性势能与动能的比**。基频的平方等于此商的最小值。这一物理直觉（系统的"最经济"振动模式最先被激发）使 [[瑞利勋爵|Rayleigh]] 在1877年引入了这个商。

### 在 Fischer 极大极小定理中的角色

[[恩斯特·菲舍尔|Fischer]] 定理的核心是在**子空间约束**下对 [[瑞利勋爵|Rayleigh]]商施加双重极值：

$$\lambda_k = \max_{\dim V = k} \min_{x \in V,\, x \neq 0} R(x)$$

[[瑞利勋爵|Rayleigh]]商的凸组合表达（加权平均形式）是证明两个步骤（上界和下界论证）的关键工具。

### 梯度与临界点

[[瑞利勋爵|Rayleigh]]商关于 x 的梯度为：

$$\nabla R(x) = \frac{2}{x^T x}\left(Ax - R(x) \cdot x\right)$$

临界点（∇R = 0）恰好是特征向量，临界值恰好是特征值。因此，**求 [[瑞利勋爵|Rayleigh]]商的驻点等价于求特征向量**。

### 实际计算：Rayleigh-Ritz 方法

在[[数值分析|数值计算]]中，[[瑞利勋爵|Rayleigh]] 商用于**特征值的迭代估计**：

1. 选取初始猜测向量 x₀
2. [[计算]] R(xₖ)（作为特征值近似）
3. 更新 x：如 [[瑞利勋爵|Rayleigh]] 商迭代（Rq = Axₖ - R(xₖ)xₖ 的法方程）
4. 收敛速度：[[瑞利勋爵|Rayleigh]]商迭代对单纯特征值**三次收敛**

**Lanczos [[算法]]**正是在 Krylov 子空间上对 [[瑞利勋爵|Rayleigh]]商做约束极值，快速[[计算]]大稀疏[[矩阵]]的极端特征值。

### 广义 Rayleigh商与主成分分析

在主成分分析（PCA）中，协方差[[矩阵]] C 的 [[瑞利勋爵|Rayleigh]]商 R(x) = xᵀCx / xᵀx 的最大值方向给出第一主成分。[[恩斯特·菲舍尔|Fischer]] 定理保证了最优 k 维投影子空间恰好是前 k 个特征向量张成的子空间，这是 PCA 最优性的数学根据。

## 意义

[[瑞利勋爵|Rayleigh]]商是将**"代数的"特征值**与**"几何的"子空间方向**联系起来的核心桥梁。它使得：

- 特征值可以通过优化（而非求多项式的根）来[[计算]]和估计
- 近似特征向量能给出特征值的近似（且误差阶高两级：方向误差 ε → 特征值误差 ε²）
- 有限维结果可以自然地推广到无穷维函数空间

## 来源

- [[raw/books/矩阵分析/06_fischer_minimax_theorem_1905.md]]

## 相关

- [[极大极小定理]]
- [[矩阵理论]]
- [[恩斯特·菲舍尔]]
- [[瑞利勋爵]]
