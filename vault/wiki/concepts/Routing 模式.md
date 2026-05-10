---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["agent-pattern", "workflow", "classification"]
aliases: ["路由模式", "Classification Routing", "输入路由"]
relates_to:
  - "[[AI Agent 架构模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
supersedes: null
---

# Routing 模式

## 概述
对输入进行分类并路由到专业化的后续处理流程，实现关注点分离和差异化处理。

## 关键内容
1. **工作流程**：Input → [Classifier] → Route A: [LLM-A] / Route B: [LLM-B] / Route C: [LLM-C]。先对输入进行分类，然后路由到专门的处理分支。
2. **适用场景**：存在需要差异化处理的明确类别，且分类精度有保障。分类器可以是 LLM 本身，也可以是传统 ML 模型。
3. **典型案例**：客服路由（退款/技术支持/一般询问）；根据问题难度路由到不同模型（如 Haiku 处理简单问题 vs Sonnet 处理复杂问题）。
4. **关键前提**：分类精度必须有保障，否则错误路由会导致更差的结果。需要建立分类器的评估机制。
5. **与软件工程的对应**：Routing 对应 Strategy Pattern（策略模式），根据输入类型选择不同的处理策略。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.3 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — part_of (五种核心模式之一)
- [[Prompt Chaining]] — compares_to (同为工作流模式)
- [[Agent vs Workflow]] — relates_to (属于工作流范式)
