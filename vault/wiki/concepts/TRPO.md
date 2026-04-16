---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "策略梯度", "算法", "优化"]
aliases: ["Trust Region Policy Optimization", "信赖域策略优化", "TRPO 2015"]
relates_to:
  - target: "[[REINFORCE算法]]"
    type: supersedes
    confidence: 0.9
  - target: "[[PPO]]"
    type: supersedes
    confidence: 0.9
  - target: "[[策略梯度定理]]"
    type: extends
    confidence: 0.95
  - target: "[[重要性采样]]"
    type: uses
    confidence: 0.9
  - target: "[[广义优势估计]]"
    type: uses
    confidence: 0.85
  - target: "[[KL散度]]"
    type: uses
    confidence: 0.95
supersedes: null
---

# TRPO

## 概述
Schulman et al. (ICML 2015) 提出的信赖域策略优化算法。通过在 KL 散度约束的信赖域内最大化代理目标，提供策略单调改进的理论保证。使用[[共轭梯度法]] + 回溯线搜索求解，计算开销大，是 [[PPO]] 的前身。

## 关键内容

1. **核心动机**：普通梯度上升步长难以控制——步长太小收敛慢，步长太大策略崩溃且难以恢复。根本原因是参数空间小步长对应策略空间大变化（高度非线性）。

2. **单调改进定理（Kakade & Langford 2002）**：
   `J(π̃) ≥ L_π(π̃) - C · D_KL^max(π || π̃)`
   只要最大 KL 散度受约束，策略改进即有单调保证 J(π̃) ≥ J(π)。

3. **约束优化问题**：
   最大化代理目标 `L_{θ_old}(θ) = E [ (π_θ/π_θ_old) · A^{π_old} ]`，约束 `E_s[KL(π_old || π_θ)] ≤ δ`（典型 δ=0.01）。

4. **求解方法**：[[共轭梯度法]]近似计算 F^{-1}g（F 为 Fisher 信息[[矩阵]]），避免 O(n²) 的显式[[矩阵]]构造；随后用回溯线搜索找满足约束的最大步长。

5. **局限性**：共轭梯度（10-50次迭代）+ 线搜索计算开销极大；不兼容参数共享的 [[强化学习三大范式|Actor-Critic]]；不支持标准 mini-[[bat]]ch SGD；实现极为复杂，逐渐被 [[PPO]] 取代。

## 来源
- [[raw/assets/RL-Analysis/rl_04_reinforce_trpo_ppo]] — P-02：TRPO 完整分析（Schulman et al. ICML 2015）

## 相关
- [[REINFORCE算法]] — supersedes
- [[PPO]] — supersedes（被 PPO 取代）
- [[策略梯度定理]] — extends
- [[重要性采样]] — uses
- [[广义优势估计]] — uses
- [[KL散度]] — uses
