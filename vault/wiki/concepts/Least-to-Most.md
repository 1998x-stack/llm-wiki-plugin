---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, reasoning]
aliases: ["最少到最多", "Least-to-Most", "L2M"]
relates_to: []
supersedes: null
---

# Least-to-Most

## 概述
Least-to-Most 是一种复杂分步任务解决策略，通过将复杂任务分解为子问题并递进解决。

## 关键内容

1. **基本原理**：
   - 将复杂任务分解为一系列更简单的子问题
   - 按照从最少信息到最多信息的顺序逐步解决问题
   - 每个子问题的解决为下一个子问题提供必要的上下文

2. **技术特点**：
   - 任务分解策略：将复杂任务拆分为可管理的子任务
   - 递进式解决：前一个子问题的解作为后一个子问题的输入
   - 适合复杂分步任务的解决

3. **应用场景**：
   - 复杂分步任务
   - 需要多阶段推理的问题
   - 任务依赖性强的场景

## 来源
- [[AI-Agent--01_prompt_engineering]] — 高级技术部分中的 Least-to-Most

## 相关
- [[In-Context-Learning]] — relates_to
- [[Chain-of-Thought]] — relates_to
- [[Prompt-Engineering]] — relates_to