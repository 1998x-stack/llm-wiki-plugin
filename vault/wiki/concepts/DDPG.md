---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [强化学习, Actor-Critic, 确定性策略, 连续控制, 深度强化学习]
aliases: [Deep Deterministic Policy Gradient, 深度确定性策略梯度]
relates_to:
  - target: Actor-Critic方法
    type: extends
  - target: 经验回放
    type: uses
  - target: 目标网络
    type: uses
  - target: DQN
    type: extends
  - target: TD3
    type: compares_to
supersedes: null
---

# DDPG

## 概述

DDPG（Deep Deterministic Policy Gradient）由 [[DeepMind]] 于 ICLR 2016 发表（arXiv:1509.02971）。核心贡献：将 DQN 的[[经验回放]]与[[目标网络]]引入连续动作空间，结合确定性[[策略梯度定理]]（DPG，Silver et al. 2014），首次实现连续控制任务的端到端深度[[强化学习]]。确定性策略 a=μ_θ(s) 避免了 DQN 在连续空间中的 argmax 不可行问题，OU 噪声提供探索。软[[目标网络]]更新（τ=0.005）比 DQN 的硬复制更稳定。

## 关键内容

1. **四网络结构**：在线 Actor μ_θ、目标 Actor μ_θ̄、在线 Critic Q_φ、目标 Critic Q_φ̄。Critic 计算 TD 目标：y = r + γ·Q_φ̄(s', μ_θ̄(s'))；Actor 最大化期望 Q 值：∇J = ∇_a Q_φ(s,a)|_{a=μ_θ(s)} · ∇_θ μ_θ(s)。[[目标网络]]软更新：θ̄ ← τθ + (1-τ)θ̄。
2. **OU 噪声探索**：确定性策略无内在随机性，通过 Ornstein-Uhlenbeck 过程添加时间相关噪声 dN = θ(μ-N)dt + σdW，适合物理控制；实践中也常用简单高斯噪声。
3. **主要缺陷**：Critic 系统性过估计 Q 值（比真实值高 200-600%），Actor 利用过估计区域形成正反馈循环，训练不稳定，OU 噪声超参数难调。这些问题由 TD3 系统性修复。

## 来源
- [[raw/assets/RL-Analysis/rl_05_a3c_ddpg_td3_sac.md]] — Part B：DDPG 完整分析

## 相关
- [[Actor-Critic方法]] — extends
- [[经验回放]] — uses
- [[目标网络]] — uses
- DQN — extends
- TD3 — compares_to
- SAC — compares_to
- [[DeepMind]] — 作者机构
