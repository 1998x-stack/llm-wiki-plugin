---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [multi-agent, orchestration, gsd-framework, ai-agents]
aliases: ["GSD Multi-Agent Orchestration", "GSD Subagent Orchestration"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[Multi-Agent Orchestration]]"
    type: extends
    confidence: 0.8
  - target: "[[Subagent 地址系统]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# GSD 多智能体编排架构

## 概述
GSD框架中的[[多智能体编排]]架构，采用专家分工和并行编排模式，通过11个专业化[[Subagents-in-Claude-Code|子智能体]]协作完成开发任务，主编排者不执行重型任务以保持[[上下文窗口]]效率。

## 关键内容

1. **核心设计原则**：
   - **专家分工**：每个[[Subagents-in-Claude-Code|子智能体]]承担特定职责，避免角色冲突
   - **并行编排**：多个研究智能体可并行执行，提升效率
   - **编排者轻量化**：主会话只负责协调，不执行重负载任务
   - **精确上下文构建**：每个[[Subagents-in-Claude-Code|子智能体]]只获得必要的上下文信息

2. **11个专家[[Subagents-in-Claude-Code|子智能体]]**：
   - `gsd-planner`：基于研究生成XML结构化计划
   - `gsd-roadmapper`：将需求分解为路线图阶段
   - `gsd-executor`：执行单个[[XML Plan|PLAN.md]]中的任务
   - `gsd-phase-researcher`：阶段专属领域研究（支持×4并行）
   - `gsd-project-researcher`：项目级领域研究（支持×4并行）
   - `gsd-research-synthesizer`：合并多份研究报告
   - `gsd-debugger`：诊断失败根因，生成修复计划
   - `gsd-codebase-mapper`：棕地代码库分析（支持×4并行）
   - `gsd-verifier`：验证代码库是否达成阶段目标
   - `gsd-plan-checker`：8维度计划质量验证
   - `gsd-integration-checker`：跨模块集成一致性检查

3. **编排模式与调度**：
   - [[波次并行执行]]：按依赖关系将任务分组，同[[波次并行执行]]，不同波次串行等待
   - 文件冲突检测：防止多个计划同时修改同一文件
   - 依赖关系拓扑排序：自动分析计划间的依赖并安排执行顺序

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD深度解析第四篇

## 相关
- [[GSD Framework]] — 整体框架
- [[Subagent 地址系统]] — 子智能体通信机制
- [[Orchestrator-Subagent-Pattern]] — 模式设计原理