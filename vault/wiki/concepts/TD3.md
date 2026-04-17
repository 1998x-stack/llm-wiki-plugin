---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [强化学习, Actor-Critic, 连续控制, 双Critic, 深度强化学习]
aliases: [Twin Delayed Deep Deterministic, 双延迟深度确定性策略梯度]
relates_to:
  - target: DDPG
    type: extends
  - target: Double DQN
    type: uses
  - target: Actor-Critic方法
    type: extends
  - target: 目标网络
    type: uses
supersedes: DDPG
---

# TD3

## 概述

TD3（Twin Delayed [[DDPG|Deep Deterministic Policy Gradient]]）由 McGill University 于 ICML 2018 发表（arXiv:1802.09477）。TD3 系统诊断了 DDPG 的三大失效机制——Critic 过估计、[[强化学习三大范式|Actor-Critic]] 正反馈循环、策略更新频率过高——并分别提出三个修复：双 Critic 取最小值、目标策略平滑化、延迟策略更新。在 MuJoCo 6 个任务上相比 DDPG 平均提升 50-100%，成为确定性策略连续控制的强基线。

## 关键内容

1. **双 Critic（Clipped Double Q-learning）**：维护两个独立 Critic Q_φ₁、Q_φ₂，目标值取 min：y = r + γ·min(Q_φ̄₁(s',ã), Q_φ̄₂(s',ã))。悲观估计宁可低估也不过估计，防止 Actor 利用 Critic 错误高点；两个 Critic 独立用相同目标更新，Actor 梯度仅用第一个 Critic。
2. **目标策略平滑化**：目标动作加截断噪声 ã = clip(μ_θ̄(s') + clip(ε,-c,c), a_min, a_max)，ε~N(0,σ)，c=0.5。对 Q 函数进行隐式正则化，类似 Label Smoothing，防止 Q 函数在动作尖峰处过拟合。
3. **延迟策略更新**：Critic 每步更新，Actor 和[[目标网络]]每 d=2 步才更新一次。让 Critic 有足够时间收敛后再指导 Actor，打破过估计→Actor利用→Critic恶化的循环。

## 来源
- [[raw/assets/RL-Analysis/rl_05_a3c_ddpg_td3_sac.md]] — Part C：TD3 完整分析

## 相关
- DDPG — extends
- [[Double DQN]] — uses
- [[Actor-Critic方法]] — extends
- [[目标网络]] — uses
- SAC — compares_to
- [[经验回放]] — uses
