---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [强化学习, Actor-Critic, 异步, 并行, 深度强化学习]
aliases: [Asynchronous Advantage Actor-Critic, A2C, 异步优势演员评论家]
relates_to:
  - target: Actor-Critic方法
    type: extends
  - target: 经验回放
    type: contradicts
  - target: 策略梯度定理
    type: uses
  - target: 广义优势估计
    type: uses
supersedes: null
---

# A3C

## 概述

A3C（Asynchronous Advantage [[强化学习三大范式|Actor-Critic]]）由 [[DeepMind]] 于 ICML 2016 发表（arXiv:1602.01783）。核心洞察：多个并行 [[Worker Agent|Worker]] 与不同环境实例异步交互，天然产生不相关数据，可替代[[经验回放]]解决训练稳定性问题。这使 A3C 无需经验[[经验回放|回放缓冲区]]，同时支持 on-policy [[算法]]和连续动作空间，用 CPU 集群即可达到与 DQN（GPU）相当的 Atari 性能，且训练时间从 8-10 天缩短至约 1 天（16 CPU）。

## 关键内容

1. **异步并行架构**：维护全局共享网络（Actor 头 + Critic 头），多个 [[Worker Agent|Worker]] 各持局部副本，独立与环境交互后[[计算]]梯度，异步（lock-free）更新全局参数。每个 [[Worker Agent|Worker]] 循环：复制全局参数 → 执行 t_max 步 → [[计算]]梯度 → 更新全局。
2. **[[多步回报|n步回报]] + 熵正则化**：[[策略梯度定理|策略梯度]] = ∑_t ∇log π(a_t|s_t)·(R_t - V(s_t)) + β·∇H(π)，其中 R_t 为 n 步 bootstrapped 回报，熵项（β=0.01）鼓励探索避免策略过早收敛。
3. **局限性**：梯度陈旧（stale gradients）、on-policy 导致样本低效、对超参数敏感。同步版本 A2C 缓解了训练噪声问题，是现代 PPO 实现的基础。

## 来源
- [[raw/assets/RL-Analysis/rl_05_a3c_ddpg_td3_sac.md]] — Part A：A3C 完整分析

## 相关
- [[Actor-Critic方法]] — extends
- [[经验回放]] — contradicts
- [[策略梯度定理]] — uses
- [[广义优势估计]] — uses
- DDPG — compares_to
- [[DeepMind]] — 作者机构
