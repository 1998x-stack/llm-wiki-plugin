---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [superpowers, multi-agent, "context management", "agent systems", "AI engineering", AI工程]
aliases: ["Context Window Pollution", "上下文窗口污染", "上下文污染"]
relates_to:
  - target: "[[上下文窗口]]"
    type: part_of
    confidence: 0.9
  - target: "[[Context Management]]"
    type: related_to
    confidence: 0.9
  - target: "[[subagent-driven-development Skill]]"
    type: addressed_by
    confidence: 1.0
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: addressed_by
    confidence: 0.95
---

# Context Window Pollution

## 概述
[[Context Window]] Pollution 是指在 Agent 系统中，当主 Agent 在完成 brainstorming 和 plan writing 后，其[[上下文窗口]]积累了大量需求讨论、设计方案权衡、被否定方案、用户偏好说明等历史信息，这些历史会占用宝贵的上下文空间、污染推理路径并降低执行精度的现象。

## 关键内容
1. **发生机制**：
   - 主 Agent 在完成 brainstorming + [[writing-plans Skill|writing-plans]] 之后，积累了大量的历史信息
   - 包括：需求讨论、设计方案权衡辩论、被否定的替代方案、用户偏好说明等
   - 这些历史会占用上下文空间，压缩实际任务能"看到"的代码量

2. **负面影响**：
   - **占用空间**：占用宝贵的上下文空间，压缩实现任务能"看到"的代码量
   - **污染推理**：实现可能被"应该用方案 B 但被否定了"这样的历史干扰
   - **降低精度**：[[Attention Dilution|注意力分散]]在协调和执行两种完全不同的认知模式之间

3. **解决方案：[[Orchestrator Agent|Orchestrator]]-Subagent 模式**：
   - **主 Agent（[[Orchestrator Agent|Orchestrator]]）**：负责读计划、维护状态、构建[[子 Agent & 多 Agent 系统|子 Agent]] 上下文、协调评审；上下文为完整的计划 + 项目背景
   - **[[子 Agent & 多 Agent 系统|子 Agent]]（Implementer，每任务一个）**：只做当前任务；上下文仅为当前任务所需的最小信息；生命周期为任务完成即销毁
   - [[子 Agent & 多 Agent 系统|子 Agent]] 的上下文由主 Agent **精确构造**，不继承主 Agent 的对话历史

4. **官方原则**：
   > "They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work."

5. **防止措施**：
   - 使用 Subagent-Driven Development [[Skills|技能]]来避免上下文污染
   - 采用[[Two-Stage Review|两阶段评审]]确保质量和规格合规性
   - 保持[[子 Agent & 多 Agent 系统|子 Agent]] 的上下文清洁和专注

## 来源
- [[05-subagent-driven-development]] — Context Window Pollution 问题的详细分析与解决方案

## 相关
- [[subagent-driven-development Skill]] — addresses_context_pollution
- [[Orchestrator-Subagent-Pattern]] — addresses_context_pollution
- [[上下文窗口]] — part_of
- [[Context Management]] — related_to
- [[Multi-Agent Orchestration]] — relates_to