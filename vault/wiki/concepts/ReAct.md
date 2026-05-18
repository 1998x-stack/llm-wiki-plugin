---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, reasoning, AI工程]
aliases: ["推理与行动", "Reasoning and Acting", "ReAct"]
relates_to: []
supersedes: null
---

# ReAct

## 概述
ReAct (Reasoning and Acting) 是一种结合推理和行动的技术，通过交错执行 Reasoning 和 Acting 来完成任务。

## 关键内容

1. **基本原理**：
   - ReAct 框架将推理和行动交替进行
   - Reasoning 步骤负责计划和反思
   - Acting 步骤负责与环境交互，如访问外部工具或数据库

2. **技术特点**：
   - 交错执行推理和行动步骤
   - 允许模型基于推理结果采取具体行动
   - 支持工具调用和外部环境交互
   - 反馈循环允许模型根据行动结果调整后续推理

3. **应用场景**：
   - 需要工具调用的任务
   - 与外部环境交互的推理任务
   - 需要实时信息获取的问答系统

## 来源
- [[AI-Agent--01_prompt_engineering]] — 高级技术部分中的 ReAct

## 相关
- [[Chain-of-Thought]] — relates_to
- [[Tool-Usage]] — implements
- [[Prompt-Engineering]] — relates_to