---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "DQN", "网络架构", "价值分解"]
aliases: ["Dueling Network", "对抗网络DQN", "决斗DQN"]
relates_to:
  - target: "[[DQN]]"
    type: extends
    confidence: 0.98
  - target: "[[强化学习]]"
    type: part_of
    confidence: 0.9
  - target: "[[Double DQN]]"
    type: compares_to
    confidence: 0.85
  - target: "[[优先经验回放]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# Dueling DQN

## 概述
Dueling [[DQN]]（Wang et al., [[DeepMind]], ICML 2016）将 Q 值分解为状态价值 V(s) 和动作优势 A(s,a) 两个独立流，通过网络架构改进而非目标函数改动来提升学习效率。在动作选择不关键的状态下，V(s) 可从所有动作经验中高效学习，避免对每个 (s,a) 对重复采样。

## 关键内容

1. **核心洞察——Q 值分解**：
   `Q^π(s,a) = V^π(s) + A^π(s,a)`
   其中 V^π(s) 是与动作无关的状态价值，A^π(s,a) 是动作优势（均值为 0）。

2. **分离学习的优势**：在很多状态（如 Atari 赛车前方无障碍时），动作选择对结果几乎无影响，此时 V(s) 的高效更新远比 Q(s,a) 的低效更新重要。

3. **网络架构**：共享卷积特征提取层后分叉为两个流：
   - **价值流**：输出标量 V(s;θ,β)
   - **优势流**：输出 |A| 维向量 A(s,a;θ,α)
   - **去均值合并**（解决不可辨识问题）：
     `Q(s,a;θ,α,β) = V(s;θ,β) + [A(s,a;θ,α) - (1/|A|) Σ_{a'} A(s,a';θ,α)]`

4. **不可辨识问题**：朴素合并 Q = V + A 时，V 和 A 的绝对值不唯一（可同时加减常数）。去均值操作强制 A 均值为 0，使 V 真正代表状态价值，梯度更稳定。

5. **实验结果**：49 款 Atari 游戏中 57%（28/49）优于 [[Double DQN]]；平均得分比 [[Double DQN]] 提升约 15-20%；在 Centipede 等动作不关键游戏提升最显著。

6. **正交性**：架构改动与 [[Double DQN]]（目标计算）和 [[优先经验回放|PER]]（采样策略）完全正交，可任意叠加。

## 来源
- [[rl_02_double_dueling_per]] — Dueling Network Architectures for Deep Reinforcement Learning (arXiv:1511.06581, ICML 2016)

## 相关
- [[DQN]] — extends
- [[强化学习]] — part_of
- [[Double DQN]] — compares_to
- [[优先经验回放]] — compares_to
