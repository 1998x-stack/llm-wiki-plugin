---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 任务编排, 评估基准, AI工程]
aliases: ["TaskBench: Benchmarking Large Language Models for Task Automation"]
relates_to: []
supersedes: null
---

# TaskBench

## 概述
TaskBench是由Shen等人提出的基准，用于评估LLM的任务自动化能力，特别关注任务编排能力。它从三个维度评估LLM在[[Skills|技能]]编排方面的能力。

## 关键内容

1. **三个评估维度**：
   - Tool Graph Construction（工具图构建）：能否正确识别任务依赖关系
   - Tool Selection（工具选择）：能否在多个可选工具中选最合适的
   - Parameter Prediction（参数预测）：能否正确填写工具调用的参数

2. **关键发现**：
   - GPT-4在工具图构建上显著优于其他模型（复杂依赖推理）
   - 工具描述歧义是导致工具选择错误的首要原因（43%的错误）
   - 工具数量超过20个时，所有模型性能均显著下降

3. **对[[Skills|技能]]文件设计的启示**：
   - 清晰的工具描述至关重要
   - 工具间依赖关系需要明确定义
   - 参数规范需要详细说明

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "TaskBench: Benchmarking Large Language Models for Task Automation", 2024

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Task-Orchestration]] — relates_to
- [[Tool-Evaluation]] — relates_to
- [[Skill-Dependency]] — relates_to