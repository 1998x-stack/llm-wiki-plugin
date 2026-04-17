---
type: concept
title: "Agent 循环"
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-16
source_count: 1
tags: [AI, Agent, 架构, 设计模式, LLM, Agent系统]
aliases:
  - Agent Loop
  - Agent心跳
  - Agent Loop 模式
relates_to:
  - target: "[[Pi-Agent]]"
    type: implemented_by
    confidence: 0.95
  - target: "[[事件驱动Agent架构]]"
    type: related_to
    confidence: 0.9
  - target: "[[Agent Harness模式]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# Agent 循环

## 概述

Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `toolUse` 则执行工具并将结果注入下一轮，直至任务完成。

## 关键内容

### 基本结构

```
while (true):
    response = LLM(messages + tools_definition)

    if response.stopReason == "stop":
        break          # LLM 认为任务完成，输出文本

    if response.stopReason == "toolUse":
        tool_results = execute_tools(response.toolCalls)
        messages.append(tool_results)
        # 继续循环，让 LLM 基于工具结果继续推理
```

### 魔鬼在细节里

基本结构简单，但工业级实现需解决五类问题：

| 问题 | 处理策略 |
|------|---------|
| 工具执行**失败** | 将错误作为工具结果反馈给 LLM，让其自我修正 |
| 工具参数**不合法** | 运行前用 AJV/JSON Schema 验证，生成详细错误消息 |
| 执行中**实时推送进度** | `onUpdate` 回调流式推送（bash 实时输出等） |
| 用户在执行中**发出新指令** | 消息队列（转向消息 / 跟进消息）而非丢弃 |
| **中断**正在运行的 Agent | AbortSignal 传递给工具执行函数 |

### 工具参数验证

在工具执行之前用 TypeBox schema + AJV 校验参数，验证失败时生成详细错误消息反馈给 LLM，允许模型**自我修正**而非崩溃：

```
工具调用参数验证失败（bash）：
  - command: 期望 string，收到 number (123)
请使用正确的参数重新调用工具。
```

### 消息队列与并发交互

用户在 Agent 执行过程中发出的新消息被**队列化**，在合适时机注入：

| 模式 | 注入时机 | 用途 |
|------|----------|------|
| **转向消息**（steering） | 下次 LLM 调用之前 | 在 Agent 运行过程中调整方向 |
| **跟进消息**（follow-up） | 整个 `session_end` 之后 | 等当前任务完成后追加新任务 |

### 为何不内置 max_steps？

> "我从未发现 max_steps 这类限制有用。Agent 要么完成任务，要么卡住了——如果卡住了，max_steps 无法修复它，只会在错误的地方截断执行。" — [[Mario-Zechner]]

限制步数是用机械手段掩盖 Agent 能力不足，而非真正解决问题。

## 代表实现

- [[Pi-Agent]] 的 `pi-agent-core` 包：最简实现，约 < 500 行 TypeScript
- [[DeepAgents]]：LangGraph 实现，以[[ROS (Robot Operating System)|中间件]]链增强循环能力

## 来源

- [[raw/articles/ai-tools/pi-agent/03-pi-agent-core.md]]

## 相关

- [[Agent Harness模式]] — 在 Agent 循环上叠加中间件、后端等能力的工程模式
- [[事件驱动Agent架构]] — 驱动循环状态变化通知上层 UI 的机制
- [[Pi-Agent]] — 代表性极简实现
