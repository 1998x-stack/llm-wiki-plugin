---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [agent-pattern, workflow, prompt-engineering, AI工程]
aliases: ["提示链", "Prompt Chain", "Chain of Prompts"]
relates_to:
  - "[[AI Agent 架构模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
  - "[[工具组合模式]] — compares_to"
supersedes: null
---

# Prompt Chaining

## 概述
将复杂[[任务分解]]为顺序执行的多个 LLM 调用步骤，每个步骤处理前一步的输出，可在中间插入程序化检查点（gate）以确保质量。

## 关键内容
1. **工作流程**：Input → [LLM1] → Gate? → [LLM2] → Gate? → [LLM3] → Output。每个 LLM 调用处理上一个的输出，可在中间步骤插入程序化检查（gate）。
2. **适用场景**：任务能被清晰拆分为固定子任务，以延迟换取更高精度。适合需要多阶段处理的场景，如内容生成→翻译、大纲→检验→正文。
3. **典型案例**：生成营销文案 → 翻译成目标语言；写文档大纲 → 检验大纲 → 基于大纲撰写正文。每个中间 gate 可以验证输出质量，不合格则终止或重试。
4. **与软件工程的对应**：Prompt Chaining 对应软件工程中的 Chain of Responsibility 模式和 Pipeline 模式，数据沿固定路径流动，每阶段进行特定处理。
5. **优势与权衡**：优势在于每步骤可独立优化和调试，gate 提供[[质量保障|质量控制]]点；代价是增加端到端延迟，适合精度优先于速度的场景。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.2 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — part_of (五种核心模式之一)
- [[Routing 模式]] — compares_to (同为工作流模式)
- [[Agent vs Workflow]] — relates_to (属于工作流范式)
- [[工具组合模式]] — compares_to (提示词链 vs 工具链编排)
