---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI工程, 推理机制, Claude]
aliases:
- Extended Thinking
- 扩展思考
- 扩展思维
relates_to:
- target: '[[Think 工具]]'
  type: compares_to
  confidence: 0.95
- target: '[[Chain-of-Thought]]'
  type: compares_to
  confidence: 0.8
- target: '[[上下文工程]]'
  type: part_of
  confidence: 0.75
- target: '[[Anthropic]]'
  type: part_of
  confidence: 0.9
supersedes: null
---

# Extended Thinking

## 概述
Extended Thinking 是 Anthropic Claude 的一种推理机制，允许模型在开始生成响应之前进行深度规划和分析，特别适用于数学、编程和复杂计划任务。

## 关键内容

### 核心定义

Extended Thinking 让模型在**开始生成之前**进行全面的推理规划。与 Think 工具不同，Extended Thinking 的推理发生在模型输出任何内容之前，主要基于用户查询本身进行深度分析。

### 与 Think 工具的本质区别

| 特性 | Extended Thinking | Think 工具 |
|------|------------------|-----------|
| 触发时机 | 模型开始生成**之前** | 已开始生成**之中** |
| 适用场景 | 深度计划、数学、编程 | 长工具调用链中处理工具输出 |
| 信息基础 | 主要基于用户查询 | 基于**外部工具返回的新信息** |
| 推理深度 | 更全面 | 更聚焦于新发现信息 |
| 最优领域 | 非工具场景（编码/数学/物理） | 策略密集、顺序决策场景 |

直觉类比：Extended Thinking 像是专家**开始工作前**的深度规划；Think 工具像是专家在**看到化验结果后**的即时分析。

### τ-Bench 评估表现

在 τ-Bench 航空域测试中：
- 基准（无 think，无 ET）：pass@1 = 0.332
- **Extended Thinking**：pass@1 = **0.412**
- Think 工具（无 prompt 优化）：pass@1 = 0.404
- Think 工具 + 优化 prompt：pass@1 = 0.584

Extended Thinking 单独使用性能与 Think 工具（无 prompt 优化）相近（0.412 vs 0.404），但在策略复杂的航空域中不如 Think 工具 + 优化 prompt 的组合。

零售域策略相对简单，Extended Thinking（pass@1 = 0.770）略低于 Think 工具（pass@1 = 0.812），说明在简单策略场景中，提供思考空间本身就足够。

### 最新发展（2025 年 12 月更新）

Extended Thinking 能力已大幅提升，在大多数场景下 Anthropic 现推荐使用 Extended Thinking 替代专用的 Think 工具。随着 Extended Thinking 的不断完善，专用 Think 工具的使用场景可能会进一步收窄。

### 适用场景

1. **深度计划任务**：需要在工作开始前制定完整策略
2. **数学问题求解**：需要多步推理和验证
3. **编程任务**：需要理解复杂代码库和设计实现方案
4. **物理问题**：需要系统性分析和计算

### 与 Chain-of-Thought 的关系

Extended Thinking 与 Chain-of-Thought（CoT）有相似之处，都是让模型进行显式推理。但 Extended Thinking 是 Claude 平台的内置能力，而 CoT 是通过 prompt 工程实现的通用技术。Extended Thinking 的推理过程对用户不可见，而 CoT 的推理步骤会直接输出在响应中。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/03_think_tool.md]] — The "think" tool: Enabling Claude to stop and think in complex tool use situations

## 相关

- [[Think 工具]] — compares_to（两种不同的推理机制，Extended Thinking 在工作前规划，Think 工具在工具调用中分析）
- [[Chain-of-Thought]] — compares_to（都是显式推理机制，但实现方式和可见性不同）
- [[上下文工程]] — part_of（Extended Thinking 是上下文工程中增强推理能力的技术）
- [[Anthropic]] — part_of（Extended Thinking 是 Anthropic Claude 平台的特性）
