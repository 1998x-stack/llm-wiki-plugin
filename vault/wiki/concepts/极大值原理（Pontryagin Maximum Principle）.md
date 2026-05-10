---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 控制论]
aliases: ["Pontryagin Maximum Principle", "极大值原理", "最优控制必要条件"]
relates_to:
  - target: "[[动态规划]]"
    type: compares_to
    confidence: 0.9
  - target: "[[卡尔曼滤波]]"
    type: relates_to
    confidence: 0.8
  - target: "[[调速器稳定性理论]]"
    type: extends
    confidence: 0.85
supersedes: null
---

# 极大值原理（Pontryagin Maximum Principle）

## 概述
Pontryagin 于 1956 年提出的极大值原理将最优控制问题转化为 Hamilton 系统的求解，通过协态变量和 Hamiltonian 的逐点极大化条件，为受约束的动态优化问题提供了优美而强大的必要条件。

## 关键内容

1. **历史背景**：冷战期间弹道导弹和航天器轨迹优化是核心工程挑战。经典变分法无法处理控制变量有约束的实际问题。Pontryagin（14 岁失明的拓扑学家）从微分方程定性理论角度攻克此问题。

2. **核心贡献**：通过引入协态变量（costate variables）和 Hamiltonian 函数，将最优控制问题转化为 Hamilton 系统。极大值原理给出最优解的必要条件：最优控制必须在每个时刻使 Hamiltonian 达到最大值。

3. **与[[动态规划]]的对偶**：Pontryagin 极大值原理和 Bellman [[动态规划]]是最优控制理论的两大支柱——前者从微分方程视角出发，后者从递归决策视角出发，数学上对偶，[[计算]]和应用上各有优势。

4. **Bang-bang 控制**：极大值原理自然导出了 bang-bang 控制理论——最优控制往往在允许集合的边界上取值。

## 来源
- [[08-pontryagin-maximum-principle]] — Pontryagin 极大值原理

## 相关
- [[动态规划]] — compares_to
- [[卡尔曼滤波]] — relates_to
- [[调速器稳定性理论]] — extends
