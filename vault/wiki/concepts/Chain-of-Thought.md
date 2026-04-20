---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI工程, 推理机制, Prompt工程]
aliases:
- Chain-of-Thought
- CoT
- 思维链
- 链式思考
- 思维链提示
relates_to:
- target: '[[Think 工具]]'
  type: compares_to
  confidence: 0.9
- target: '[[Extended Thinking]]'
  type: compares_to
  confidence: 0.85
- target: '[[外化工作记忆]]'
  type: compares_to
  confidence: 0.8
- target: '[[上下文工程]]'
  type: part_of
  confidence: 0.8
supersedes: null
---

# Chain-of-Thought

## 概述
Chain-of-Thought（CoT，思维链）是一种 Prompt 工程技术，通过引导模型逐步展示推理过程来提升其在复杂任务上的表现，是显式推理机制的早期形式。

## 关键内容

### 核心定义

Chain-of-Thought 通过在 prompt 中添加"让我们逐步思考"或提供推理示例，引导模型将复杂推理分解为多个中间步骤。这种方法在数学、逻辑推理和复杂问答任务中表现显著。

### 与 Think 工具的对比

| 特性 | CoT 提示 | Think 工具 |
|------|---------|-----------|
| 触发 | 通过 prompt 隐式引导 | 显式工具调用 |
| 时机 | 固定在响应开始 | **动态**，在需要时才触发 |
| 可见性 | 混在响应文本中 | 结构化工具调用，易于追踪 |
| 适用性 | 单步推理 | 多步工具调用链中的动态推理 |

Think 工具本质上是**结构化的、按需触发的 CoT**。

### 与 Extended Thinking 的对比

Extended Thinking 与 CoT 都旨在增强模型的推理能力，但实现方式不同：
- CoT 的推理步骤直接输出在响应文本中，对用户可见
- Extended Thinking 的推理过程对用户不可见，是平台内置能力
- CoT 是通用的 prompt 技术，适用于任何 LLM；Extended Thinking 是 Claude 特有功能

### 外化工作记忆的视角

从认知科学角度，CoT 可以理解为一种**外化工作记忆**的实现：
- 模型将中间推理步骤写入输出，相当于"写下来帮助思考"
- 后续的推理可以引用前面的推理步骤
- 但 CoT 的外化是线性的、不可结构化的，而 Think 工具提供了结构化的外化空间

### 演变脉络

推理机制的演进可以概括为：
1. **CoT 提示**：通过 prompt 引导模型展示推理步骤（通用、线性、可见）
2. **Think 工具**：结构化的、按需触发的推理空间（工具化、动态、可追踪）
3. **Extended Thinking**：平台内置的深度推理能力（内置、前置、不可见）

三者各有适用场景，核心原则一致：**为模型提供显式的中间推理空间**。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/03_think_tool.md]] — The "think" tool: Enabling Claude to stop and think in complex tool use situations

## 相关

- [[Think 工具]] — compares_to（Think 工具是结构化的、按需触发的 CoT）
- [[Extended Thinking]] — compares_to（都是显式推理机制，但 CoT 通过 prompt 实现，Extended Thinking 是平台内置能力）
- [[外化工作记忆]] — compares_to（CoT 是外化工作记忆的一种实现方式，但线性且不可结构化）
- [[上下文工程]] — part_of（CoT 是上下文工程中增强推理能力的核心技术）
