---
type: concept
status: active
confidence: 0.5
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 研究, 强化学习]
aliases: [Reinforcement Learning from Human Feedback, 基于人类反馈的强化学习]
relates_to:
  - 强化学习
  - 奖励函数
supersedes: null
---

# RLHF

## 概述
RLHF（Reinforcement Learning from Human Feedback）即基于人类反馈的强化学习，是强化学习在大模型时代的延伸。核心创新是将奖励函数的设置交给人类反馈，解决了传统强化学习中奖励函数设计的核心痛点。

## 关键内容
1. **与强化学习的关系**：RLHF本质是强化学习的延伸，继承了"环境反馈+奖励机制+自主学习最优策略"的核心逻辑。
2. **解决的核心痛点**：传统强化学习中奖励函数设置极难，尤其语言类和机器人控制场景，不合理的奖励函数会让整个训练完全偏离预期。RLHF将奖励函数设计交给人类反馈，绕过了这一难题。
3. **落地难点**：强化学习训练需要海量环境交互和极高算力成本，这是实验室方案无法落地到商用场景的核心原因。RLHF同样面临成本约束问题。
4. **应用方向**：大模型对齐（alignment）的核心技术路径，通过人类偏好标注训练reward model，再用PPO等算法优化策略。

## 来源
- [[raw/articles/essays/thinking-series/011-算法面试]] — 强化学习研究方向讨论

## 相关
- [[强化学习]] — part_of
- [[奖励函数]] — uses
- [[PPO]] — uses
