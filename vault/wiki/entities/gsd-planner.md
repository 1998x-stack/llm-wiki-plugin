---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: ["gsd", "subagent", "planning", "xml", "architecture", "Agent系统"]
aliases: ["gsd-planner", "GSD Planner", "规划子智能体"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
    confidence: 0.9
  - target: "[[Multi-Agent Orchestration]]"
    type: implements
    confidence: 0.9
  - target: "[[GSD Planner Checker]]"
    type: complement
    confidence: 0.8
  - target: "[[XML Plan]]"
    type: generates
    confidence: 0.9
---

# gsd-planner

## 概述
GSD 系统中的规划[[Subagents-in-Claude-Code|子智能体]]，负责基于研究结果生成 [[XML 结构化 Prompt|XML 结构化计划]]。它是整个 GSD 工作流中关键的架构决策环节。

## 关键内容

1. **输入数据**：
   - PROJECT.md（技术约束和禁令）
   - REQUIREMENTS.md（阶段必须实现的需求）
   - CONTEXT.md（用户实现偏好决策）
   - RESEARCH.md（四维研究结论）

2. **核心职责**：
   - 综合所有输入，理解"需要做什么"和"如何做"
   - 将工作分解为 2-3 个原子 XML 计划
   - 每个计划控制在单个 200k 上下文可完成的规模内
   - 分析计划间依赖关系，标记 `<depends_on>` 标签
   - 确保垂直切片（每个计划是功能完整的端到端切片）

3. **输出产物**：
   - N-01-[[XML Plan|PLAN.md]], N-02-[[XML Plan|PLAN.md]] 等 XML 结构计划文件
   - 计划间的依赖关系定义

4. **模型分配策略**：
   - 在 balanced 模式下使用 Opus 模型，因为计划阶段是关键架构决策时刻
   - 需要高质量的分解、任务边界定义和技术选型判断

5. **工作特点**：
   - 串行执行（非并行）
   - 需要精确的上下文构建
   - 产出结构化的 XML 计划供执行器使用

## 来源
- [[04-multi-agent-orchestration]] — 多智能体编排架构
- [[GSD Framework]] — GSD 框架文档

## 相关
- [[GSD]] — part_of
- [[Multi-Agent Orchestration]] — implements
- [[GSD Planner Checker]] — complement
- [[XML Plan]] — generates
- [[gsd-executor]] — works_with