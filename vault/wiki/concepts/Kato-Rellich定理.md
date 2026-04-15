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
- Kato-Rellich theorem
- Kato定理
- 相对有界扰动
- 量子Hamilton算子自伴性
relates_to:
- target: '[[加藤敏夫]]'
  type: implements
  confidence: 0.95
- target: '[[矩阵扰动理论]]'
  type: extends
  confidence: 0.9
- target: '[[Weyl特征值不等式]]'
  type: extends
  confidence: 0.75
- target: '[[正规矩阵]]'
  type: uses
  confidence: 0.7
supersedes: null
---

# Kato-Rellich定理

## 概述

[[加藤敏夫|Kato]]-Rellich定理是算子[[矩阵扰动理论|扰动理论]]的基础定理，由 Franz Rellich（1940年代）和[[加藤敏夫]]（1951年）共同建立。**核心结论：若 $A$ 是 Hilbert 空间上的自伴算子，$B$ 是 $A$-有界的对称算子且相对界 $a < 1$，则 $A + B$ 在 $D(A)$ 上自伴。** 其在量子力学中的应用是革命性的：[[加藤敏夫|加藤]]1951年利用该定理一举证明了所有有限粒子系统（含 Coulomb 相互作用）的 Schrödinger Hamilton 算子的本质自伴性——解决了 von Neumann 未能解决的问题，为量子力学全部[[数值分析|数值计算]]提供了数学合法性。

## 关键内容

### 定理精确陈述

**设** $A$ 为 Hilbert 空间 $\mathcal{H}$ 上的自伴算子（定义域 $D(A)$），$B$ 为对称算子（$D(A) \subset D(B)$）且存在常数 $a < 1$ 和 $b \geq 0$ 使得：

$$\|Bu\| \leq a\|Au\| + b\|u\|, \quad \forall u \in D(A)$$

（称 $B$ 是 $A$-**有界的**，且 $A$-**界**（relative bound）为 $a$）

则 $A + B$ 在定义域 $D(A)$ 上**自伴**，且 $A + B$ 是**本质自伴的**当且仅当 $A$ 是本质自伴的。

**关键条件**：相对界 $a < 1$（严格小于1）。若 $a = 1$，结论一般不成立。

### 量子力学中的应用

**核心应用**：多体 Schrödinger 算子的自伴性（[[加藤敏夫|加藤]]，1951）

考虑 $N$ 个量子粒子的 Hamilton 算子：
$$H = -\sum_{i=1}^N \frac{\hbar^2}{2m_i}\Delta_i + \sum_{i<j} \frac{e_i e_j}{|x_i - x_j|}$$

在 $L^2(\mathbb{R}^{3N})$ 上，动能算子 $T = -\Delta$ 是自伴的，而 Coulomb 势能 $V = \sum_{i<j} e_i e_j / |x_i - x_j|$ 是 $T$-有界的且相对界 $< 1$（由 Hardy 不等式：$\|r^{-1}u\|_2 \leq c\|\nabla u\|_2$）。

由 [[加藤敏夫|Kato]]-Rellich 定理，$H = T + V$ 自伴。

**历史意义**：这证明了原子（氢原子、氦原子等）、分子（H₂, NH₃等）的 Hamilton 算子的数学合法性，解决了 von Neumann 悬而未决的问题，为量子化学和量子力学的全部理论计算提供了基础。

### 与有限维矩阵扰动的类比

| | 有限维（[[矩阵扰动理论]]） | 无穷维（[[加藤敏夫|Kato]]-Rellich） |
|--|------------------------|----------------------|
| 结构 | Hermitian [[矩阵]] | 自伴算子 |
| 扰动条件 | $\|E\|_F$ 小 | $B$ 是 $A$-有界且相对界 $<1$ |
| 结论 | 特征值连续变化 | $A+B$ 仍自伴 |
| 工具 | [[格奥尔格·弗罗贝尼乌斯|Frobenius]] 范数，谱范数 | 算子域，图范数 |
| 代表结果 | [[赫尔曼·外尔|Weyl]] 不等式，Hoffman-[[赫尔穆特·维兰特|Wielandt]] | [[加藤敏夫|Kato]]-Rellich 定理 |

有限维情形：Hermitian [[矩阵]] $A$ 和任意 Hermitian 扰动 $B$ 之和仍是 Hermitian 的（自动成立）。无穷维情形：这需要专门的定理来保证，因为算子的定义域可能改变。

### 解析扰动理论（Rellich-Kato）

当 $B(\kappa) = \kappa B^{(1)} + \kappa^2 B^{(2)} + \cdots$ 解析依赖于参数 $\kappa$ 时，$T(\kappa) = A + B(\kappa)$ 的离散特征值可展开为 $\kappa$ 的收敛幂级数：

$$\lambda(\kappa) = \lambda_0 + \kappa\lambda_1 + \kappa^2\lambda_2 + \cdots$$

这就是量子力学 [[瑞利勋爵|Rayleigh]]-Schrödinger 微扰级数的严格数学基础：
- $\lambda_1 = \langle \psi_0, B^{(1)}\psi_0\rangle$（一阶微扰修正）
- $\lambda_2 = \sum_{n\neq 0} |\langle\psi_n, B^{(1)}\psi_0\rangle|^2 / (\lambda_0 - \lambda_n)$（二阶修正）

### KLMN 定理（更广泛的二次型方法）

对于比 [[加藤敏夫|Kato]]-Rellich 更奇异的扰动（如量子力学中的 $1/r^2$ 势），可用二次型方法：

**KLMN 定理**（[[加藤敏夫|Kato]]-Lax-Milgram-Nelson）：若下半有界闭二次型 $a$ 的扰动 $b$ 满足 $|b[u,u]| \leq \varepsilon a[u,u] + C_\varepsilon\|u\|^2$（$\varepsilon < 1$），则 $a + b$ 仍是下半有界闭二次型，对应的算子自伴。

### 本质谱的稳定性（Weyl-von Neumann-Kato）

**[[赫尔曼·外尔|Weyl]]-von Neumann 定理的[[加藤敏夫|加藤]]版**：本质谱 $\sigma_{\text{ess}}(T)$ 在**相对紧扰动**（relatively compact perturbation）下保持不变：

$$\sigma_{\text{ess}}(T + K) = \sigma_{\text{ess}}(T)$$

**含义**：紧扰动（对应有限秩或"衰减到无穷"的势能）不改变连续谱，只能改变离散特征值的有限个——这是量子力学"散射态不受有限范围势能影响"的数学表述。

## 影响

**Davis-Kahan $\sin\Theta$ 定理（1970）**：建立于[[加藤敏夫|加藤]]的子空间间距理论，给出特征子空间旋转的定量界：$\|\sin\Theta\| \leq \|E\|/\delta$。是现代 PCA 一致性理论和谱聚类稳定性的核心工具。

**Reed-Simon（1972-1978）**：四卷本数学物理教材系统引用[[加藤敏夫|加藤]]框架，[[加藤敏夫|Kato]]-Rellich 是第二卷的核心。

**量子化学**：从 Hartree-Fock 方法到密度泛函理论，量子化学的一切[[数值分析|数值计算]]都依赖于多体 Schrödinger 算子的自伴性——由 [[加藤敏夫|Kato]] 定理保证。

## 来源

- [[raw/books/矩阵分析/15_kato_perturbation_theory_1966.md]]

## 相关

- [[加藤敏夫]]
- [[矩阵扰动理论]]
- [[Weyl特征值不等式]]
- [[正规矩阵]]
- [[Hoffman-Wielandt定理]]
