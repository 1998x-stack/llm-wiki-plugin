---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [NLP, alignment, RLHF, AI工程]
aliases: [InstructGPT]
relates_to:
  - target: Long Ouyang
    relation: relates_to
  - target: RLHF
    relation: implements
  - target: PPO（近端策略优化）
    relation: uses
  - target: GPT 系列
    relation: extends
supersedes: null
---

# InstructGPT

## 概述
使用 RLHF 对齐的大[[Language-Model|语言模型]]，是 [[ChatGPT]] 的直接技术前身。

## 关键内容

1. **RLHF 三步流程**：监督微调（SFT）→ [[奖励模型]]训练 → [[PPO（近端策略优化）]] 优化。
2. **对齐效果**：在遵循指令、减少有害输出、提高真实性方面显著优于原始 [[GPT-3]]。
3. **[[ChatGPT]] 基础**：该方法论成为 [[ChatGPT]] 的核心技术，确立了大[[Language-Model|语言模型]]对齐的标准实践。

## 来源
- [[ai_papers_timeline.md]] — 2022 年时间线条目

## 相关
- [[Long Ouyang]] — relates_to
- [[RLHF]] — implements
- [[PPO（近端策略优化）]] — uses
- [[GPT 系列]] — extends
