---
type: concept
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: ["强化学习", "深度学习", "DQN"]
aliases: ["Deep Q-Network", "深度Q网络", "Playing Atari with Deep Reinforcement Learning"]
relates_to:
  - target: "[[强化学习]]"
    type: part_of
    confidence: 0.98
  - target: "[[经验回放]]"
    type: uses
    confidence: 0.98
  - target: "[[目标网络]]"
    type: uses
    confidence: 0.98
  - target: "[[Double DQN]]"
    type: extends
    confidence: 0.95
  - target: "[[Dueling DQN]]"
    type: extends
    confidence: 0.95
  - target: "[[优先经验回放]]"
    type: extends
    confidence: 0.95
  - target: "[[DeepMind]]"
    type: part_of
    confidence: 0.9
  - target: "[[Rainbow]]"
    type: extends
    confidence: 0.95
supersedes: null
---

# DQN

## 概述
DQN（Deep Q-Network）是 [[DeepMind]] 于 2013/2015 年发表的深度[[强化学习]]奠基算法，将卷积神经网络与 Q-learning 结合，通过[[经验回放]]和[[目标网络]]两项工程创新，首次在 Atari 2600 游戏上从原始像素端到端学习超人类策略，开启深度[[强化学习]]的黄金十年。

## 关键内容

1. **三大核心挑战与解决方案**：数据时序相关 → [[经验回放]]（均匀随机采样）；目标值不稳定 → [[目标网络]]（每 C=10,000 步硬更新）；奖励尺度差异 → 奖励裁剪至 [-1,1]。

2. **网络架构（Nature DQN 2015）**：输入 84×84×4（连续4帧灰度图），经三层卷积（32/64/64 filters，stride 4/2/1）+ FC 512 → 输出 |A| 个 Q 值，一次前向传播获得所有动作的 Q 值。

3. **TD 目标**：使用[[目标网络]]计算 `y_t = r_t + γ · max_{a'} Q_{θ̄}(s', a')`，Huber loss + RMSProp（lr=2.5e-4）更新在线网络；ε 从 1.0 线性衰减到 0.1（前 100 万步）。

4. **实验结果（49 款 Atari 游戏）**：29/49 超越人类；Breakout 超人类 1293%，Boxing 1775%；Montezuma's Revenge 因稀疏奖励完全失败（0分）。

5. **[[Ablation Study|消融实验]]**：去掉[[目标网络]]或[[经验回放]]均显著降低性能，两者同时去掉则常常发散。

6. **核心缺陷**：Q 值过估计（max 操作引入正偏差）→ [[Double DQN]]；均匀采样低效 → [[优先经验回放]]；无价值分解 → [[Dueling DQN]]；六大改进集成 → [[Rainbow]]（2018）。

7. **工程遗产**：确立的范式（深度网络函数逼近 + 经验[[经验回放|回放缓冲区]] + [[目标网络]] + ε-greedy + 奖励归一化）被几乎所有后续 off-policy 深度 RL 算法继承。

## 来源
- [[rl_02_double_dueling_per]] — DQN 三大改进分析（Double DQN · Dueling DQN · PER）
- [[rl_01_dqn]] — V-01 DQN 完整分析，含算法伪代码、数学推导、超参数分析、消融实验

## 相关
- [[强化学习]] — part_of
- [[经验回放]] — uses
- [[目标网络]] — uses
- [[Double DQN]] — extends
- [[Dueling DQN]] — extends
- [[优先经验回放]] — extends
- [[DeepMind]] — part_of
- [[Rainbow]] — extends
