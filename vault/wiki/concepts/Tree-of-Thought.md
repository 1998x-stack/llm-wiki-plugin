---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, reasoning, AI工程]
aliases: ["树状思维", "Tree-of-Thought", "ToT"]
relates_to: []
supersedes: null
---

# Tree-of-Thought

## 概述
Tree-of-Thought (ToT) 是一种高级推理技术，通过树形搜索推理路径来解决复杂规划问题。

## 关键内容

1. **基本原理**：
   - ToT 扩展了 [[Chain-of-Thought]] 的线性推理，允许模型探索多个推理路径。
   - 采用树形结构进行搜索，可以回溯和探索不同的解决方案分支。

2. **技术特点**：
   - 相比于线性的 [[Chain-of-Thought]]，提供更复杂的多路径推理
   - 适用于需要规划和探索多种可能性的复杂问题
   - 结合了搜索[[算法]]和神经网络的推理能力

3. **应用场景**：
   - 复杂规划问题
   - 需要多路径探索的决策任务
   - 需要全局优化的推理任务

## 来源
- [[AI-Agent--01_prompt_engineering]] — 高级技术部分中的 Tree-of-Thought

## 相关
- [[Chain-of-Thought]] — extends
- [[ReAct]] — compares_to
- [[In-Context-Learning]] — relates_to