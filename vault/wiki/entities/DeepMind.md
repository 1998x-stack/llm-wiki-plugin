---
type: entity
entity_type: company
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI研究", "强化学习", "深度学习"]
aliases: ["Google DeepMind", "DeepMind Technologies"]
relates_to:
  - target: "[[DQN]]"
    type: part_of
    confidence: 0.98
  - target: "[[强化学习]]"
    type: extends
    confidence: 0.85
supersedes: null
---

# DeepMind

## 概述
DeepMind Technologies 是英国 AI 研究公司，2010 年创立，2014 年被 [[Google]] 收购（现为 [[Google]] DeepMind）。以深度[[强化学习]]研究著称，代表成果包括 [[DQN]]（2013/2015 Atari）、AlphaGo（2016）、AlphaFold（2021）等，是现代 AI 最重要的研究机构之一。

## 关键内容

1. **[[DQN]] 论文团队**：Volodymyr Mnih、Koray Kavukcuoglu、David Silver 等，2013 年 N[[逆倾向评分|IPS]] Workshop 发表，2015 年 Nature 发表完整版（Human-level control through deep [[强化学习|RL]]，Nature 518, 529-533）。

2. **代表性成果**：
   - [[DQN]]（2013/2015）— 深度[[强化学习]]奠基，首次从像素学习 Atari 游戏超人类策略
   - AlphaGo（2016）— 首个战胜围棋世界冠军的 AI
   - AlphaFold（2021）— 解决蛋白质结构预测，被誉为生物学重大突破

3. **工程贡献**：[[DQN]] 确立的工程范式（[[经验回放]] + [[目标网络]] + 深度卷积网络）被几乎所有后续 off-policy 深度 [[强化学习|RL]] 算法沿用，并催生 [[Rainbow]]（2018）等系列改进工作。

## 来源
- [[rl_01_dqn]] — V-01 DQN 完整分析，DeepMind Atari 研究历史背景

## 相关
- [[DQN]] — part_of
- [[强化学习]] — extends
