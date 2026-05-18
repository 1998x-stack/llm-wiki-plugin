---
type: concept
status: active
confidence: 0.7
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 架构模式, Agent系统, AI工程]
aliases: [App Server Pattern, WebSocket Server Mode]
relates_to:
  - target: "[[Codex CLI]]"
    type: part_of
    confidence: 0.95
  - target: "[[Codex TUI]]"
    type: compares_to
    confidence: 0.85
  - target: "[[LLM-Wire-Protocol统一模式]]"
    type: implements
    confidence: 0.9
supersedes: null
---

# App Server 模式

将 Agent 核心（core）与前端解耦的架构模式——通过本地 WebSocket [[服务]]器暴露会话状态和工具执行能力，允许多种前端（TUI、IDE Extension、Web App）接入同一个后端。

## 概述

App Server 模式实现了 [[Codex CLI]] 的前后端分离架构：`codex-rs/core` 作为独立进程运行，通过 WebSocket 协议向多个客户端广播事件和接收指令，TUI 只是众多前端之一。

## 架构

```
┌──────────────────────────────────────────┐
│          codex-rs/core                    │
│    (会话状态、Agent 循环、工具执行)         │
└──────┬───────────┬───────────┬───────────┘
       │           │           │
   TUI 前端    App Server   IDE Extension
  (终端渲染)   (WebSocket)   (VS Code)
```

## 客户端能力

- 发送 `!` shell 命令直接执行
- 监听文件系统变更事件
- 通过 bearer-token 鉴权连接远程 WebSocket [[服务]]器
- 接收 Agent 事件流（tool call、审批请求、输出结果）

## 与 Wire Protocol 的关系

App Server 是 [[LLM-Wire-Protocol统一模式]] 的具体实现：核心业务逻辑通过 protocol crate 与 UI 层完全解耦，支持 [[Python]]/[[TypeScript]] 客户端通过协议接入，[[Codex CLI|Codex]] 自身也可作为 [[MCP Prompts|MCP Server]] 被其他 Agent 调用。

## 来源

- [[raw/articles/ai-tools/codex/02_codex_tui_component.md]] — Codex CLI 深度解析 Vol.2：TUI 交互式终端的设计哲学

## 相关

- [[Codex CLI]] — part_of
- [[Codex TUI]] — compares_to
- [[LLM-Wire-Protocol统一模式]] — implements
