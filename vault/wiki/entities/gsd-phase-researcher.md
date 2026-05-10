---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, researcher, phase-analysis, technology-study]
aliases: ["gsd-phase-researcher", "GSD Phase Researcher", "GSD阶段研究智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: precedes
    confidence: 0.9
  - target: "[[GSD Planning Directory]]"
    type: produces_output_for
    confidence: 0.7
supersedes: null
---

# gsd-phase-researcher

## 概述
GSD框架中最常被调用的[[Subagents-in-Claude-Code|子智能体]]，专门负责阶段专属领域的研究工作，在计划阶段会并行启动4个实例分别研究不同维度。

## 关键内容

1. **研究维度分工**：
   - **stack**：研究阶段涉及的技术栈，包括API文档、版本限制、兼容性问题
   - **features**：研究功能实现的最佳方案，对比不同技术选型
   - **architecture**：研究架构模式，确保与现有代码保持一致
   - **pitfalls**：研究已知问题、性能陷阱、版本兼容性问题

2. **输入输出**：
   - 输入根据研究类型变化：PROJECT.md（技术约束）+ CONTEXT.md（实现偏好）+ 阶段描述/功能需求/架构信息等
   - 输出：针对不同维度的研究结论，为后续规划提供依据

3. **并行执行特点**：
   - 每次plan-phase都并行spawn 4个实例
   - 每个实例专注单一维度，避免[[Attention Dilution|注意力分散]]
   - 不同维度需要不同的搜索策略和关注点
   - 每个维度的深度研究保证了整体规划质量

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-planner]] — 研究成果用于计划生成