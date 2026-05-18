---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, reasoning, AI工程]
aliases: ["思维链", "Chain-of-Thought", "CoT"]
relates_to: []
supersedes: null
---

# Chain-of-Thought

## 概述
Chain-of-Thought (CoT) 是一种 [[Prompt Engineering]] 技术，通过引导模型逐步展示推理过程来提高复杂推理任务的准确性。

## 关键内容

1. **基本原理**：
   - CoT 通过在 Prompt 中加入"请一步一步思考，然后给出答案"这样的指令，激活模型的中间推理步骤。
   - 这种技术显著提升了模型在数学、逻辑推理等复杂任务上的准确率。

2. **实现方式**：
   - 通过自然语言指令引导："请一步一步思考"
   - 在 Few-shot 示例中展示推理步骤
   - 与其他高级推理技术结合使用

3. **应用场景**：
   - 数学问题求解
   - 逻辑推理任务
   - 复杂决策制定
   - 需要多步骤分析的问题

## 来源
- [[AI-Agent--01_prompt_engineering]] — Chain-of-Thought（思维链）部分

## 相关
- [[Prompt-Engineering]] — extends
- [[Tree-of-Thought]] — compares_to
- [[Self-Consistency]] — extends