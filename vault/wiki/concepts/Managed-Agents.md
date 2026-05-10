---
type: concept
title: Managed Agents
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 技术, 方法论, AI工程]
aliases:
- Claude Managed Agents
- 托管智能体
- Managed Agents
relates_to:
- target: '[[元控制框架]]'
  type: implements
  confidence: 1.0
- target: '[[脑手分离架构]]'
  type: uses
  confidence: 1.0
- target: '[[Agent Harness模式]]'
  type: extends
  confidence: 0.95
- target: '[[会话日志]]'
  type: uses
  confidence: 0.95
- target: '[[Context-Engineering]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# Managed Agents

## 概述

[[Claude_Code|Claude]] Managed [[Agents]] 是 [[Anthropic]] 在 [[Claude_Code|Claude]] Platform 中提供的托管[[服务]]，代表用户运行长周期 Agent。它通过一组抽象接口（会话、控制框架、沙箱）将 Agent 各组件解耦，使各组件的实现可独立替换而不影响其他部分。

## 关键内容

### 设计动机

[[Agent Harness模式]] 编码了关于"[[Claude_Code|Claude]] 不能独立做什么"的假设，但这些假设会随模型进步而**过时**。例如：[[Claude-Sonnet-4-5|Claude Sonnet 4.5]] 会在接近上下文限制时过早结束任务（[[上下文焦虑]]），因此在 harness 中加入了[[上下文重置]]；但同样的 harness 用于 [[Claude_Code|Claude]] Opus 4.5 时，该行为消失了——重置变成了死重。

Managed [[Agents]] 的目标是设计一组**能超越任何特定实现的接口**，包括 [[Anthropic]] 今天运行的那些实现。

### 三大抽象组件

| 组件 | 角色 | 接口 |
|------|------|------|
| **会话（Session）** | 所有发生事件的追加日志 | `getEvents()`, `emitEvent(id, event)` |
| **控制框架（Harness）** | 调用 [[Claude_Code|Claude]] 并路由工具调用的循环 | `wake(sessionId)`, `getSession(id)` |
| **沙箱（Sandbox）** | [[Claude_Code|Claude]] 可运行代码和编辑文件的执行环境 | `execute(name, input) → string`, `provision({resources})` |

### 核心设计原则

- **对接口形态有主见，对背后实现无主见**
- 每个组件可独立失败或替换
- 遵循[[操作系统]]"程序未思之程序"的设计哲学——通过虚拟化硬件为尚不存在的程序提供通用抽象

### 架构演进

1. **初始设计**：所有组件放在单个容器中（会话、harness、沙箱共享环境）
2. **问题暴露**：容器变成"宠物"——失败时需人工修复，无法调试，无法连接客户 VPC（详见 [[宠物与牲畜模式]]）
3. **解耦方案**：将"大脑"（[[Claude_Code|Claude]] + harness）与"手"（沙箱）和"会话"（事件日志）分离

### 性能收益

解耦后 p50 TTFT 下降约 **60%**，p95 TTFT 下降超过 **90%**。因为不需要沙箱的会话可立即开始推理，无需等待容器[[Configuration|配置]]。

### 安全边界

在耦合设计中，[[Claude_Code|Claude]] 生成的不可信代码与凭证运行在同一容器中。解耦后：
- Git 令牌在沙箱初始化时注入本地 git remote，Agent 从不直接处理令牌
- 自定义工具通过 MCP 调用，OAuth 令牌存储在安全保险库中，由专用代理代为调用
- Harness 从不知晓任何凭证

### 与 Context Engineering 的关系

会话作为**存在于 [[Claude_Code|Claude]] [[上下文窗口]]之外的上下文对象**，提供了与 [[Context-Engineering]] 互补的机制：不是通过压缩或裁剪做不可逆的上下文决策，而是保证上下文可持久化、可查询、可回溯。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/Scaling Managed Agents_ Decoupling the brain from the hands.md]] — Anthropic Engineering Blog

## 相关

- [[元控制框架]] — implements（Managed Agents 是 meta-harness 的具体实现）
- [[脑手分离架构]] — uses（核心架构模式）
- [[Agent Harness模式]] — extends（超越特定 harness 的通用接口层）
- [[会话日志]] — uses（会话作为外部上下文对象）
- [[Context-Engineering]] — related_to（互补的上下文管理策略）
