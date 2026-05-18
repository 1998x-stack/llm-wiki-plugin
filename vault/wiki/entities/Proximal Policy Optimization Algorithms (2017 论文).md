---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, reinforcement-learning, PPO, 强化学习]
aliases: [Schulman et al. 2017]
relates_to:
  - target: John Schulman
    relation: authored_by
  - target: PPO（近端策略优化）
    relation: introduced
  - target: InstructGPT
    relation: enabled
supersedes: null
---

# Proximal Policy Optimization Algorithms (2017 论文)

## 概述
提出 PPO [[算法]]的论文，通过裁剪策略更新实现稳定高效的深度[[强化学习]]训练。

## 关键内容

1. **裁剪目标函数**：通过限制策略更新幅度，避免单次更新过大导致性能崩溃，实现稳定的训练过程。
2. **实现简单**：相比 TRPO 等复杂[[算法]]，PPO 实现简单、调参友好，成为深度[[强化学习]]的主流选择。
3. **RLHF 应用**：PPO 被用于 [[InstructGPT]] 中的 RLHF 对齐，将人类偏好学习融入大[[Language-Model|语言模型]]训练。

## 来源
- [[ai_papers_timeline.md]] — 2017 年时间线条目

## 相关
- [[John Schulman]] — authored_by
- [[PPO（近端策略优化）]] — introduced
- [[InstructGPT]] — enabled
