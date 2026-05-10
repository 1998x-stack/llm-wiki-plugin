---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [强化学习, Actor-Critic, 策略梯度, 深度强化学习]
aliases: [Actor-Critic, AC方法, 演员-评论家]
relates_to:
  - target: 策略梯度定理
    type: uses
  - target: 价值函数
    type: uses
  - target: 广义优势估计
    type: uses
  - target: 强化学习三大范式
    type: part_of
supersedes: null
---

# Actor-Critic方法

## 概述

[[强化学习三大范式|Actor-Critic]]（[[强化学习三大范式|演员-评论家]]）方法是[[强化学习]]中结合[[策略梯度定理|策略梯度]]（Actor）与[[价值函数]]估计（Critic）的混合架构。Actor 负责选择动作，Critic 负责评估当前策略的价值，用于降低[[策略梯度定理|策略梯度]]的方差。相比纯[[策略梯度定理|策略梯度]]方法，AC 通过 Critic 提供基线，减少估计噪声；相比纯价值方法，AC 直接优化策略，天然支持连续动作空间。现代深度[[强化学习]]中绝大多数 SOTA 方法（A3C、DDPG、TD3、SAC、PPO）均属于 [[强化学习三大范式|Actor-Critic]] 家族。

## 关键内容

1. **架构分工**：Actor 网络参数化策略 π_θ(a|s)，Critic 网络估计[[价值函数]] V_φ(s) 或 Q_φ(s,a)；Actor 用 Critic 的输出[[计算]][[价值函数|优势函数]]指导更新方向。
2. **[[价值函数|优势函数]]**：A(s,a) = Q(s,a) - V(s)，衡量某动作相对于平均水平的优劣，作为[[策略梯度定理|策略梯度]]的权重，替代原始回报以降低方差。
3. **演化路线**：A3C（异步并行）→ DDPG（确定性策略 + [[经验回放]]）→ TD3（双 Critic + 延迟更新）→ SAC（最大熵框架），每代解决前代的核心缺陷。

## 来源
- [[raw/assets/RL-Analysis/rl_05_a3c_ddpg_td3_sac.md]] — Actor-Critic Methods 完整分析（A3C/DDPG/TD3/SAC）

## 相关
- [[策略梯度定理]] — uses
- [[价值函数]] — uses
- [[广义优势估计]] — uses
- A3C — extends
- DDPG — extends
- TD3 — extends
- SAC — extends
- [[强化学习三大范式]] — part_of
