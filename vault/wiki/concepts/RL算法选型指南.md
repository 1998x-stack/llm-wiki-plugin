---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "算法选型", "实践指南"]
aliases: ["RL算法选型", "强化学习算法选择", "算法选型决策树"]
relates_to:
  - target: "[[强化学习三大范式]]"
    type: extends
  - target: "SAC"
    type: compares_to
  - target: "PPO"
    type: compares_to
  - target: "[[Rainbow]]"
    type: compares_to
  - target: "TD3"
    type: compares_to
supersedes: null
---

# RL算法选型指南

## 概述
[[强化学习]]算法选型的核心维度是动作空间类型（离散/连续）与任务需求（稳定性/性能/样本效率）。连续动作首选 SAC（自动调参，稳定性最优）；离散动作+视觉输入首选 [[Rainbow]]；RLHF 和多任务场景首选 PPO。选型需权衡超参数敏感性、计算资源与收敛保证。

## 关键内容

1. **离散动作空间选型**：
   - 视觉/像素输入 + 追求最高性能 → [[Rainbow]]（Atari 中位数得分 223%）
   - 视觉输入 + 简单实现 → DQN / [[Double DQN]]
   - 低维向量 + 样本效率优先 → DQN + PER
   - 低维向量 + 稳定性优先 → PPO（离散版本）
   - 稀疏奖励/探索困难 → PPO + 内在奖励（ICM/RND）

2. **连续动作空间选型**：
   - 稳定性 + 自动调参（首选） → SAC（超参敏感性极低，MuJoCo 最优）
   - 极限性能 + 可控探索 → TD3（HalfCheetah ~9600, Walker2D ~4680）
   - 多任务 / RLHF → PPO（连续版本，工业标准）
   - 资源受限 / 快速原型 → DDPG

3. **特殊场景**：
   - 安全约束 RL（单调改进保证） → TRPO / CPO
   - 多智能体 / 分布式计算 → A3C / IMPALA / MAPPO
   - 人类反馈（RLHF） → PPO（InstructGPT/ChatGPT 标准方案）
   - 学术研究（方法论完备性） → SAC（软贝尔曼收敛保证）
   - 分布式大规模训练 → IMPALA / Ape-X

4. **超参数敏感性对比**（敏感性由低到高）：
   - SAC：极低（自动温度 α，几乎免调）
   - PPO：低（clip ε 和 GAE λ 鲁棒）
   - TRPO：低（信赖域 δ 自动处理）
   - DQN/TD3：中
   - [[Rainbow]]：高（六组件各有超参）
   - DDPG：高（OU噪声 σ 极敏感）

5. **计算资源需求**：
   - GPU 密集：DQN/[[Rainbow]]（单GPU+大回放缓冲）
   - CPU 并行：A3C（天然多核，无需 GPU）
   - 均衡：PPO（多环境并行，低-中 GPU）
   - 二阶方法：TRPO（CG 计算，CPU 高需求）

6. **MuJoCo 基准**（参考分）：SAC HalfCheetah ~10100 > TD3 ~9600 > DDPG ~8600 >> PPO ~1800；Atari 基准：[[Rainbow]] 223% > SAC(离散) ~180% > PPO ~100-150% > DQN 79%。

## 来源
- [[raw/assets/RL-Analysis/rl_06_final_comparison]] — F-01：强化学习算法终极对比分析

## 相关
- [[强化学习三大范式]] — extends
- SAC — compares_to
- PPO — compares_to
- [[Rainbow]] — compares_to
- TD3 — compares_to
- DDPG — compares_to
- TRPO — compares_to
