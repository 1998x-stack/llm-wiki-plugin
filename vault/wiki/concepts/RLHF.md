---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [NLP, alignment, reinforcement-learning, 强化学习]
aliases: [Reinforcement Learning from Human Feedback]
relates_to:
  - target: PPO（近端策略优化）
    relation: uses
  - target: InstructGPT
    relation: applied_to
  - target: 奖励模型
    relation: uses
supersedes: null
---

# RLHF

## 概述
基于人类反馈的[[强化学习]]，通过人类偏好信号对齐大[[Language-Model|语言模型]]输出。

## 关键内容

1. **三步流程**：监督微调收集示范数据 → 训练[[奖励模型]]学习人类偏好 → 使用 [[PPO（近端策略优化）]] 优化策略。
2. **对齐目标**：使模型输出更符合人类[[价值观]]和偏好，减少有害、虚假或不 helpful 的内容。
3. **[[ChatGPT]] 核心**：RLHF 是 [[ChatGPT]] 成功的关键技术，确立了大[[Language-Model|语言模型]]部署的标准实践。

## 来源
- [[ai_papers_timeline.md]] — 2022 年时间线条目

## 相关
- [[PPO（近端策略优化）]] — uses
- [[InstructGPT]] — applied_to
- [[奖励模型]] — uses
