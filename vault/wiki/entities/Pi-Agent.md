---
type: entity
title: "Pi Agent"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 3
tags:
  - 工具
  - AI
  - Agent
  - 技术
aliases:
  - Pi
  - pi-mono
  - Pi Agent Toolkit
relates_to:
  - target: "[[Mario-Zechner]]"
    type: caused
    confidence: 0.95
  - target: "[[OpenClaw]]"
    type: uses
    confidence: 0.95
  - target: "[[Claude-Code]]"
    type: contradicts
    confidence: 0.8
  - target: "[[Agent Harness模式]]"
    type: implements
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: implements
    confidence: 0.9
  - target: "[[LLM-Wire-Protocol统一模式]]"
    type: implements
    confidence: 0.95
  - target: "[[跨Provider上下文迁移]]"
    type: implements
    confidence: 0.9
  - target: "[[Agent循环]]"
    type: implements
    confidence: 0.95
  - target: "[[事件驱动Agent架构]]"
    type: implements
    confidence: 0.95
supersedes: null
---

# Pi Agent

## 概述

Pi Agent 是由 [[Mario-Zechner]] 创建的极简 AI 编程代理工具包（TypeScript Monorepo），以 4 个工具 + < 1000 token 系统提示实现了与重型 Agent 可比的编程能力。核心理念：投资于 [[Agent Harness模式|Harness]] 的简洁性和可控性，而非堆砌功能。

## 关键内容

### 1. 四层架构

Pi 由四个严格单向分层的包组成：

| 层 | 包名 | 职责 |
|----|------|------|
| L0 | `pi-ai` | 统一 LLM 通信层，支持 300+ 模型（零内部依赖） |
| L1 | `pi-agent-core` | Agent 循环：工具调用、执行、事件流（只依赖 pi-ai） |
| L2 | `pi-coding-agent` | 完整编程代理：会话管理、工具、扩展系统 |
| L2 | `pi-tui` | 终端 UI 框架：差分渲染消除闪烁 |

每层只依赖下层，由构建系统强制执行。任何层可独立使用、替换或测试。

### 2. 四大设计哲学

1. **「不需要就不构建」**——子代理、计划模式、权限弹窗等均通过扩展系统实现而非内置
2. **严格单向分层**——构建系统强制，L0 零依赖向上到 L2
3. **[[Context-Engineering]] 第一公民**——每个进入 LLM 的 token 均可见可控，系统提示 < 1000 token，无"秘密注入"
4. **会话 JSONL 第一公民**——JSONL 格式持久化，可序列化、可后处理、可跨 Provider 迁移

### 3. 与竞品的关键差异

| 维度 | Claude Code | Pi |
|------|------------|-----|
| 系统提示 | 数千 token | < 1000 token |
| 内置工具 | 20+ | 4 |
| 多 Provider | 否 | 300+ 模型 |
| 会话格式 | 私有 | 开放 JSONL |
| 可自托管 | 否 | 是 |

### 3. pi-agent-core：Agent 循环的最简实现

`pi-agent-core`（L1 层）是 Pi 工具包的核心传动系统，将一次性 LLM 调用组装成能持续运转的 [[Agent循环]]：

- **[[事件驱动Agent架构]]**：所有状态变化（text_delta、tool_call_start、tool_result 等）通过 `subscribe/emit` 模式发射，支持多订阅者——同一 Agent 核心可驱动终端 UI、Web UI、IM 机器人，零修改
- **双通道设计**：工具结果分为 `output`（LLM 可见，计入 token）和 `details`（UI 可见，结构化数据，不占 LLM token）
- **工具参数验证**：执行前用 TypeBox + AJV 校验，失败时生成详细错误消息反馈给 LLM，允许模型**自我修正**
- **消息队列**：用户在 Agent 执行中发出的新消息被队列化为"转向消息"（下次 LLM 调用前注入）或"跟进消息"（session_end 后执行）
- **会话持久化**：`session.serialize()` 序列化完整状态，`restoreAgentSession()` 在新进程中恢复

### 4. Terminal-Bench 验证

Pi 在 Terminal-Bench 排行榜上击败了许多工具集更丰富的 Agent，验证了核心命题：**Agent 性能瓶颈在于 Harness 设计质量和上下文精确性，而非工具数量。**

## 来源

- [[raw/articles/pi-agent/01-overview-philosophy.md]]
- [[raw/articles/pi-agent/02-pi-ai.md]]
- [[raw/articles/pi-agent/03-pi-agent-core.md]]

## 相关

- [[Mario-Zechner]] — 创造者
- [[OpenClaw]] — Pi 作为核心引擎
- [[Claude-Code]] — 设计哲学对立
- [[Agent Harness模式]] — Pi 是极简 Harness 的代表实现
- [[Context-Engineering]] — 核心设计哲学
- [[LLM-Wire-Protocol统一模式]] — pi-ai 四协议统一
- [[跨Provider上下文迁移]] — pi-ai 最独特能力
- [[Agent循环]] — pi-agent-core 的核心心跳
- [[事件驱动Agent架构]] — pi-agent-core 驱动多 UI 的机制
