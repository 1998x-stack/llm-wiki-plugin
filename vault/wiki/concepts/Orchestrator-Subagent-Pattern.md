---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags:
  - AI
  - 架构
aliases:
  - "Orchestrator-Subagent Pattern"
  - "协调器 - 子智能体模式"
  - "编排器 - 子代理模式"
relates_to: []
supersedes: null
---

# Orchestrator-Subagent Pattern

## 概述

协调器 - [[Subagents-in-Claude-Code|子智能体]]（Orchestrator-Subagent）是由层级结构定义的多智能体模式。一个智能体担任团队负责人，负责规划工作、分配任务并整合结果。[[Subagents-in-Claude-Code|子智能体]]则承担具体职责并反馈结果。[[Claude-Code]] 采用此模式。

## 关键内容

### 工作原理

1. **主智能体接收任务** → 确定处理方式
2. **任务分配**：
   - 直接处理部分子任务
   - 分发其他子任务给[[Subagents-in-Claude-Code|子智能体]]
3. **[[Subagents-in-Claude-Code|子智能体]]执行** → 完成工作并返回结果
4. **协调者整合** → 将结果整合为最终输出

### 适用场景

**清晰的任务分解**：
- 任务分解清晰且子任务间相互依赖度极低
- 协调者maintains 整体目标的连贯视图
- [[Subagents-in-Claude-Code|子智能体]]专注于具体职责

**具体应用**：
- 自动化[[Code-Review-for-Claude-Code|代码审查]]（安全检查/测试覆盖率/代码风格/架构一致性）
- [[Claude-Code]] 的代码库搜索和独立问题调查
- 多文件协调修改

### 实际案例

**自动化[[Code-Review-for-Claude-Code|代码审查]]系统**：
- **协调者**：接收 PR，确定需要执行的检查
- **[[Subagents-in-Claude-Code|子智能体]]**：
  - 安全子代理：检查漏洞、注入风险、身份验证问题
  - 测试子代理：验证测试覆盖率
  - 风格子代理：评估代码风格一致性
  - 架构子代理：判断架构一致性
- **整合**：协调者收集结果，整合为统一的审查意见

### 优势

- 层级结构清晰，易于理解和管理
- 协调者对整体目标保持连贯视图
- [[Subagents-in-Claude-Code|子智能体]]专注于具体职责
- 适用于广泛的问题，协调开销最低

### 局限性

**信息瓶颈**：
- 子代理发现的相关信息需经协调者传递
- 关键细节在多次传递中可能丢失
- 协调者必须识别依赖关系并适当路由信息

**吞吐量限制**：
- 顺序执行限制吞吐量（除非显式并行化）
- 产生多智能体令牌成本，却无法获得速度优势

### 与 Agent Teams 的对比

| 维度 | Orchestrator-Subagent | Agent Teams |
|------|----------------------|-------------|
| **子任务时长** | 简短、有界 | 持续、多步骤 |
| **上下文积累** | 无（每次从零开始） | 有（积累领域知识） |
| **适用场景** | 清晰分解的独立任务 | 需要持续多步骤工作的任务 |
| **示例** | [[Code-Review-for-Claude-Code|代码审查]]检查 | 代码库迁移 |

### 设计建议

**任务分解**：
- 确保子任务间依赖度极低
- 明确定义每个子任务的输入和输出
- 协调者maintains 整体目标的连贯视图

**并行化**：
- 显式请求并行执行独立子任务
- 三个子代理同时工作通常能在更短时间内完成

**信息路由**：
- 识别子任务间的依赖关系
- 协调者适当路由相关信息
- 避免关键细节在传递中丢失

## 来源

- [[raw/articles/ai-engineering/claude-blog/Multi-agent coordination patterns_ Five approaches and when to use them.md]] — Cara Phillips 撰写

## 相关

- [[Multi-Agent-Coordination-Patterns]] — 五种模式之一（part_of）
- [[Subagents-in-Claude-Code]] — 实现技术（implements）
- [[Code-Review-for-Claude-Code]] — 应用场景（uses）
- [[Agent-Teams-Pattern]] — 替代模式（compares_to）
- [[Generator-Verifier-Pattern]] — 替代模式（compares_to）
