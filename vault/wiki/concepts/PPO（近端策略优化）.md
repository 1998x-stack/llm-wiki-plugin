---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [reinforcement-learning, policy-optimization, PPO]
aliases: [PPO, Proximal Policy Optimization]
relates_to:
  - target: John Schulman
    relation: relates_to
  - target: RLHF
    relation: used_in
  - target: InstructGPT
    relation: applied_to
supersedes: null
---

# PPO（近端策略优化）

## 概述
通过裁剪策略更新实现稳定高效训练的[[强化学习]][[算法]]，是 RLHF 的核心优化器。

## 关键内容

1. **裁剪目标函数**：限制策略更新幅度，避免单次更新过大导致性能崩溃。
2. **实现简单**：相比 TRPO 等复杂[[算法]]，PPO 实现简单、调参友好。
3. **RLHF 应用**：被用于 [[InstructGPT]] 中的 RLHF 对齐，将人类偏好学习融入大[[Language-Model|语言模型]]训练。

## 来源
- [[ai_papers_timeline.md]] — 2017 年时间线条目

## 相关
- [[John Schulman]] — relates_to
- [[RLHF]] — used_in
- [[InstructGPT]] — applied_to
