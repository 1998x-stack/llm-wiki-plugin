---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "方差", "偏差", "理论"]
aliases: ["强化学习方差偏差", "RL bias-variance tradeoff", "偏差方差权衡"]
relates_to:
  - target: "[[强化学习三大范式]]"
    type: part_of
  - target: "[[REINFORCE算法]]"
    type: compares_to
  - target: "DQN"
    type: compares_to
  - target: "[[广义优势估计]]"
    type: uses
supersedes: null
---

# RL方差偏差权衡

## 概述
[[强化学习]]中方差与偏差的权衡是三大范式差异的核心张力：Monte-Carlo 方法（[[REINFORCE算法|REINFORCE]]）无偏但方差极高；TD/Bootstrapping 方法（DQN）方差低但引入偏差；[[强化学习三大范式|Actor-Critic]] 方法通过 GAE 在两者之间取得折中。方差排序（高→低）：[[REINFORCE算法|REINFORCE]] >> A3C ≈ PPO > SAC > DDPG ≈ TD3 > DQN。

## 关键内容

1. **方差来源**：
   - Monte-Carlo 回报（[[REINFORCE算法|REINFORCE]]）：对整条轨迹求和，若单步方差为 σ²，T 步轨迹方差为 T·σ²，随 episode 长度线性增长
   - TD 更新（DQN）：仅单步 Bootstrap，批采样噪声是唯一方差来源，方差最低
   - 随机[[策略梯度定理|策略梯度]]（A3C/PPO）：用 GAE 替代 MC 回报大幅降低方差，但随机采样仍引入方差

2. **偏差来源**：
   - 函数逼近误差：所有深度 RL 方法均有，神经网络无法完美拟合真实价值
   - Bootstrapping 偏差：TD 方法用当前不准确的 Q 函数估计目标值，引入偏差
   - 过估计偏差：max 操作（DQN）系统性高估 Q 值；[[Double DQN]] 通过分离选择与评估网络缓解
   - 函数逼近 + Off-policy 组合：致命三角（Deadly Triad），DQN 的工程稳定化技术（[[目标网络]]+[[经验回放]]）是工程补丁而非理论保证

3. **各算法梯度估计对比**：
   - [[REINFORCE算法|REINFORCE]]：`ĝ = (1/N) Σ_τ [ Σ_t ∇_θ log π_θ(a_t|s_t) · G_t ]`，MC 回报 G_t 高方差
   - [[强化学习三大范式|Actor-Critic]]（A3C/PPO）：`ĝ = (1/N) Σ_t [ ∇_θ log π_θ(a_t|s_t) · Â_t^GAE ]`，GAE 优势降方差
   - DDPG/TD3（确定性）：`ĝ = (1/N) Σ_s [ ∇_θ μ_θ(s) · ∇_a Q_φ(s,a) ]`，无随机采样，链式法则
   - SAC（随机+重参数化）：`ĝ = (1/N) Σ_{s,ε} [ ∇_θ(α log π_θ(ã|s) - Q_φ(s,ã)) ]`，重参数化消除采样方差

4. **收敛理论保证对比**：
   - Q-learning（表格）：有限 MDP 收敛保证（Bellman 压缩算子）
   - DQN：无理论保证，工程稳定化（[[目标网络]]+[[经验回放]]）
   - [[REINFORCE算法|REINFORCE]]：局部最优收敛（[[策略梯度定理]]）
   - TRPO：单调改进保证（信赖域+KL 约束，前提：精确策略评估）
   - PPO：近似收敛保证（Clip 近似约束）
   - SAC：软 Q 迭代收敛（软贝尔曼压缩算子）
   - DDPG/TD3：无保证（DPG 定理有限适用）

5. **重参数化技巧**：SAC 将随机策略 a~π(·|s) 改写为 a = tanh(μ(s) + σ(s)⊙ε)，ε~N(0,I)，使梯度可通过确定性函数传播，避免直接对采样操作求导，将方差从 MC 采样降至仅批次噪声级别。

## 来源
- [[raw/assets/RL-Analysis/rl_06_final_comparison]] — 六、核心数学对比：梯度估计

## 相关
- [[强化学习三大范式]] — part_of
- [[REINFORCE算法]] — compares_to
- DQN — compares_to
- [[广义优势估计]] — uses
- SAC — compares_to
- [[最大熵强化学习]] — relates_to
