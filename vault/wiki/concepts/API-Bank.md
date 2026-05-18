---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 评估基准, API文档, AI工程]
aliases: ["API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs"]
relates_to: []
supersedes: null
---

# API-Bank

## 概述
API-Bank是由Li等人提出的首个端到端评估工具增强LLM的综合基准。它涵盖了从单个API调用到复杂任务规划的完整流程，揭示了工具文档质量对LLM工具使用能力的关键影响。

## 关键内容

1. **三层评估体系**：
   - L1：正确调用单个API（53个API）
   - L2：顺序调用多个API完成复杂任务
   - L3：规划+检索+调用的完整Pipeline

2. **关键发现**：
   - GPT-4在L1可达94%，在L3下降到53%
   - 工具文档质量对准确率影响极大，差文档会导致性能下降20%+
   - 工具描述歧义是导致工具选择错误的首要原因（43%的错误）

3. **对[[Skills|技能]]文件设计的启示**：
   - 工具文档质量是整个系统的瓶颈
   - 详细描述何时触发、如何使用、注意事项是必需的
   - 不仅仅是美观要求，而是决定LLM能否正确使用[[Skills|技能]]的关键

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs", EMNLP 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Tool-Evaluation]] — relates_to
- [[Documentation-Quality]] — relates_to
- [[API-Integration]] — relates_to