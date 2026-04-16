---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [强化学习, Actor-Critic, 最大熵, 连续控制, 深度强化学习, SAC]
aliases: [Soft Actor-Critic, 软演员评论家]
relates_to:
  - target: 最大熵强化学习
    type: implements
  - target: Actor-Critic方法
    type: extends
  - target: TD3
    type: extends
  - target: 经验回放
    type: uses
  - target: 目标网络
    type: uses
supersedes: DDPG
---

# SAC

## 概述

SAC（Soft [[强化学习三大范式|Actor-Critic]]）由 UC Berkeley 于 ICML 2018 发表（arXiv:1801.01290，v2 arXiv:1812.05905）。SAC 将[[最大熵强化学习]]框架与 off-policy [[强化学习三大范式|Actor-Critic]] 结合，用随机策略替代确定性策略，实现自动探索。v2 版本引入温度参数 α 的自动调整，彻底免除最难调的超参数。在 MuJoCo 连续控制任务上超越 [[DDPG]]、[[TD3]] 和 [[PPO]]，是目前连续控制的默认选择。

## 关键内容

1. **软 Critic 更新**：目标值包含熵项：y = r + γ·[min(Q_φ̄₁(s',ã'), Q_φ̄₂(s',ã')) - α log π(ã'|s')]，ã'~π(·|s')。继承 [[TD3]] 双 Critic 取 min，同时将熵正则纳入 Bellman 目标而非 Actor 损失。
2. **重参数化技巧**：随机 Actor 输出均值和方差，通过 a = tanh(μ_θ(s) + σ_θ(s)⊙ε)，ε~N(0,I) 实现可微采样，梯度直接传入网络。Actor 损失：L(θ) = E[α log π(ã|s) - min Q(s,ã)]，同时优化奖励和熵。
3. **自动温度（v2 核心）**：L(α) = E[-α log π(a|s) - α H̄]，H̄ = -dim(A)（连续）。α 自动升高鼓励探索（策略过确定时），自动降低专注利用（熵已足够时），无需手动调整。训练稳定性、样本效率、探索性三者统一。

## 来源
- [[raw/assets/RL-Analysis/rl_05_a3c_ddpg_td3_sac.md]] — Part D：SAC 完整分析

## 相关
- [[最大熵强化学习]] — implements
- [[Actor-Critic方法]] — extends
- [[TD3]] — extends
- [[DDPG]] — compares_to
- [[经验回放]] — uses
- [[目标网络]] — uses
- [[重要性采样]] — relates_to
