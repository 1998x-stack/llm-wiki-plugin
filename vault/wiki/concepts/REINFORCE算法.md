---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "策略梯度", "算法"]
aliases: ["REINFORCE", "蒙特卡洛策略梯度", "Williams 1992"]
relates_to:
  - target: "[[策略梯度定理]]"
    type: implements
    confidence: 0.95
  - target: "[[广义优势估计]]"
    type: extends
    confidence: 0.85
  - target: "TRPO"
    type: extends
    confidence: 0.9
  - target: "[[强化学习三大范式]]"
    type: part_of
    confidence: 0.85
supersedes: null
---

# REINFORCE算法

## 概述
Williams (1992) 提出的最早[[策略梯度定理|策略梯度]][[算法]]，使用蒙特卡洛（MC）完整轨迹回报 G_t 直接估计[[策略梯度定理|策略梯度]]。理论简洁，支持连续动作和随机策略，但方差极高、样本效率低，是后续 TRPO、PPO 等[[算法]]的出发点。

## 关键内容

1. **核心更新规则**：
   `θ ← θ + α Σ_t γ^t ∇_θ log π_θ(a_t|s_t) · G_t`
   其中 G_t = Σ_{k=t}^{T} γ^{k-t} r_k 是从 t 时刻起的折扣回报（MC 估计）。

2. **Log-trick 推导**：
   利用 ∇p = p·∇log p，将梯度转化为期望形式，使得无需知道环境动力学 P(s'|s,a)，只需能采样轨迹即可估计梯度。

3. **基线（Baseline）减方差**：
   引入与动作无关的基线 b(s_t)（通常取 V^π(s_t)）后，更新为：
   `θ ← θ + α Σ_t ∇_θ log π_θ(a_t|s_t) · (G_t - b(s_t))`
   基线不引入偏差（期望为零），但显著降低方差，此时 G_t - V(s_t) ≈ [[价值函数|优势函数]] A(s_t, a_t)。

4. **优点**：理论保证无偏梯度；支持连续动作和随机策略；探索自然内嵌；可处理部分可观测问题。

5. **局限性**：方差极高需大量样本；每个 episode 结束才能更新（只支持 on-policy，不能在线学习）；步长难以选择，收敛慢。

## 来源
- [[raw/assets/RL-Analysis/rl_04_reinforce_trpo_ppo]] — P-01：REINFORCE 完整分析（Williams 1992）

## 相关
- [[策略梯度定理]] — implements
- [[广义优势估计]] — extends
- TRPO — extends
- [[强化学习三大范式]] — part_of
