---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [reinforcement learning, policy optimization, deep rl]
aliases: ["PPO", "Proximal Policy Optimization", "近端策略优化"]
relates_to:
  - target: "[[Proximal Policy Optimization Algorithms (2017 论文)]]"
    type: described_in
  - target: "[[John Schulman]]"
    type: created_by
  - target: "[[OpenAI]]"
    type: developed_at
  - target: "[[Policy Gradient Methods]]"
    type: improvement_of
  - target: "[[Trust Region Policy Optimization]]"
    type: simplified_from
  - target: "[[Actor-Critic Methods]]"
    type: variant_of
supersedes: null
---

# Proximal Policy Optimization

## 概述
Proximal Policy Optimization (PPO) 是一种[[策略梯度定理|策略梯度]]方法，通过限制策略更新幅度来稳定[[强化学习]]训练过程。

## 关键内容

1. **信任域约束**：PPO通过裁剪策略比率来防止策略更新过大，使用[[PPO|PPO-Clip]]目标函数限制新旧策略之间的差异，避免训练不稳定。

2. **[[算法]]改进**：相比TRPO（[[TRPO|信赖域策略优化]]），PPO简化了实现复杂度，同时保持了相似的性能和稳定性，成为当前[[强化学习]]的主流[[算法]]之一。

3. **广泛应用**：PPO在游戏AI、机器人控制、自然语言处理等多个领域得到广泛应用，尤其是在需要长期规划和复杂决策的任务中表现突出。

## 来源
- [[ai_papers_timeline.md]] — 2017年PPO提出
- [[Proximal Policy Optimization Algorithms (2017 论文)]] — John Schulman等OpenAI团队的工作

## 相关
- [[Proximal Policy Optimization Algorithms (2017 论文)]] — described_in
- [[John Schulman]] — created_by
- [[OpenAI]] — developed_at
- [[Policy Gradient Methods]] — improvement_of
- [[Trust Region Policy Optimization]] — simplified_from
- [[Actor-Critic Methods]] — variant_of