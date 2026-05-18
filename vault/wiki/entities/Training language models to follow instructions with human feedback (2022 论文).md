---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, NLP, alignment, RLHF, AI工程]
aliases: [Ouyang et al. 2022, InstructGPT 论文]
relates_to:
  - target: Long Ouyang
    relation: authored_by
  - target: InstructGPT
    relation: introduced
  - target: PPO（近端策略优化）
    relation: applied
  - target: RLHF
    relation: introduced
supersedes: null
---

# Training language models to follow instructions with human feedback (2022 论文)

## 概述
[[InstructGPT]] 论文，展示使用 RLHF 对齐大[[Language-Model|语言模型]]，是 [[ChatGPT]] 的直接技术前身。

## 关键内容

1. **RLHF 三步流程**：监督微调（SFT）→ [[奖励模型]]训练 → [[PPO（近端策略优化）]] 优化，使模型输出符合人类偏好。
2. **对齐效果**：[[InstructGPT]] 在遵循指令、减少有害输出、提高真实性方面显著优于原始 [[GPT-3]]。
3. **[[ChatGPT]] 基础**：该论文的方法论成为 [[ChatGPT]] 的核心技术，确立了大[[Language-Model|语言模型]]对齐的标准实践。

## 来源
- [[ai_papers_timeline.md]] — 2022 年时间线条目

## 相关
- [[Long Ouyang]] — authored_by
- [[InstructGPT]] — introduced
- [[PPO（近端策略优化）]] — applied
- [[RLHF]] — introduced
