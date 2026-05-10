---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 任务规划, 技能编排, AI模型集成]
aliases: ["HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace"]
relates_to: []
supersedes: null
---

# HuggingGPT

## 概述
HuggingGPT是由Shen等人提出的系统，将HuggingFace上数千个专门AI模型作为可调用的工具，用[[ChatGPT]]作为任务规划器和编排器。它是AI模型作为工具编排器的典型代表。

## 关键内容

1. **四阶段工作流**：
   - Task Planning（任务规划）：[[ChatGPT]]解析用户意图，分解为子任务列表
   - Model Selection（模型选择）：从HuggingFace模型卡描述中检索最合适的模型
   - Task Execution（并行执行）：无依赖任务并行执行，有依赖任务按序执行
   - Response Generation（结果整合）：将所有子任务结果整合为最终回答

2. **核心创新**：
   - 将大量专业AI模型作为可调用工具库
   - 用大[[Language-Model|语言模型]]作为高级任务规划和编排器
   - 支持并行执行和结果传递

3. **[[Skills|技能]]描述格式**：
   - 任务类型、描述、输入输出格式等元数据
   - 为LLM选择合适[[Skills|技能]]提供依据

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace", NeurIPS 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Task-Planning]] — relates_to
- [[Skill-Orchestration]] — relates_to
- [[Model-Selection]] — relates_to