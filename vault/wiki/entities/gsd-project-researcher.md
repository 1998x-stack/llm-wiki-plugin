---
type: entity
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, researcher, project-analysis]
aliases: ["gsd-project-researcher", "GSD Project Researcher", "GSD项目研究智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: provides_input_for
    confidence: 0.8
  - target: "[[gsd-phase-researcher]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# gsd-project-researcher

## 概述
GSD框架中的项目级领域研究智能体，专门负责对整个项目级别的技术需求进行深入研究，在new-project阶段被并行调用（支持×4并行）。

## 关键内容

1. **职责范围**：
   - 进行项目级别的技术栈研究
   - 分析项目整体架构约束和最佳实践
   - 识别项目特有的技术和业务挑战
   - 为[[gsd-planner]]提供项目级的背景信息

2. **执行特征**：
   - 在new-project阶段被调用
   - 支持×4并行执行以提升效率
   - 专注于项目级别的宏观分析

3. **与[[gsd-phase-researcher]]的区别**：
   - gsd-project-researcher：关注项目级的宏观技术分析
   - [[gsd-phase-researcher]]：关注特定阶段的具体技术问题

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-planner]] — 提供输入支持
- [[gsd-phase-researcher]] — 功能类似但范围不同