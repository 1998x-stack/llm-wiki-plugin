---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["强化学习", "DQN", "Q值过估计"]
aliases: ["DDQN", "Double Q-learning DQN", "深度双Q网络"]
relates_to:
  - target: "DQN"
    type: extends
    confidence: 0.98
  - target: "[[强化学习]]"
    type: part_of
    confidence: 0.9
  - target: "[[Dueling DQN]]"
    type: compares_to
    confidence: 0.85
  - target: "[[优先经验回放]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# Double DQN

## 概述
Double DQN（van Hasselt et al., [[DeepMind]], AAAI 2016）针对 DQN 的 Q 值系统性过估计问题，通过解耦动作选择与 Q 值评估来消除偏差。核心改动仅需一行代码：用在线网络选择动作，用[[目标网络]]评估该动作的 Q 值，在 49 款 Atari 游戏中将中位数得分从 79% 提升至 117%。

## 关键内容

1. **过估计的数学根源（Jensen 不等式）**：
   当 Q(s',a') 是含噪声的无偏估计时，`E[max_{a'} Q(s',a')] ≥ max_{a'} E[Q(s',a')]`。
   即 max 的期望大于等于期望的 max，只要存在估计噪声就会系统性高估。

2. **过估计的危害**：偏差通过 TD bootstrapping 传播，导致策略退化和训练不稳定。

3. **解决方案——解耦选择与评估**：
   - **DQN 目标**（选择和评估都用[[目标网络]]）：
     `y_DQN = r + γ · Q_{θ̄}(s', argmax_{a'} Q_{θ̄}(s', a'))`
   - **Double DQN 目标**（在线网络选择，[[目标网络]]评估）：
     `y_DDQN = r + γ · Q_{θ̄}(s', argmax_{a'} Q_θ(s', a'))`

4. **实现极简**：利用 DQN 已有的在线网络 θ 与[[目标网络]] θ̄ 两套结构，仅修改目标[[计算]]一行，无需额外参数。

5. **实验结果**：在 49 款 Atari 游戏中 41 款优于 DQN；Q 值过估计从平均 300% 高估降至接近真实值；Wizard of Wor 等游戏提升超 2 倍。

6. **局限性**：过估计未完全消除（两网络仍高度相关），且在某些低估情形下表现略差。

## 来源
- [[rl_02_double_dueling_per]] — Deep Reinforcement Learning with Double Q-learning (arXiv:1509.06461, AAAI 2016)

## 相关
- DQN — extends
- [[强化学习]] — part_of
- [[Dueling DQN]] — compares_to
- [[优先经验回放]] — compares_to
