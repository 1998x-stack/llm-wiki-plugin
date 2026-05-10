---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, roadmap, project-planning]
aliases: ["gsd-roadmapper", "GSD Roadmapper", "GSD路线图智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: precedes
    confidence: 0.8
  - target: "[[GSD Planning Directory]]"
    type: contributes_to
    confidence: 0.8
supersedes: null
---

# gsd-roadmapper

## 概述
GSD框架中的路线图生成智能体，负责将高层次的项目需求分解为具体的阶段计划，通常在new-project阶段被调用。

## 关键内容

1. **核心职责**：
   - 将高层次的项目需求分解为具体的路线图阶段
   - 识别项目的整体结构和阶段划分
   - 为后续的详细规划阶段奠定基础
   - 串行执行，确保路线图的连贯性

2. **执行时机**：
   - 主要在new-project阶段被调用
   - 作为[[gsd-planner]]的前置步骤
   - 为整个项目的开发周期提供宏观规划

3. **输出产物**：
   - 项目的阶段性划分
   - 各阶段的目标和依赖关系
   - 为后续的详细规划提供框架

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-planner]] — 后续规划步骤