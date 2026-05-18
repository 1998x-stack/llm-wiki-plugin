---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [MCP, 传输协议, "Claude Code", 连接方式, AI工程]
aliases: ["MCP Transport Protocols", "MCP 传输方式"]
relates_to:
  - target: "[[MCP（Model Context Protocol）]]"
    type: part_of
  - target: "[[HTTP 传输协议]]"
    type: includes
  - target: "[[Stdio 传输协议]]"
    type: includes
  - target: "[[WebSocket 传输协议]]"
    type: includes
supersedes: null
---

# MCP 传输方式

## 概述
[[MCP（Model Context Protocol）]]支持多种传输方式来连接 [[Claude Code]] 与外部 [[MCP 服务器]]，每种方式适用于不同的部署场景和需求。

## 关键内容

1. **HTTP 传输（推荐）**：
   - 适合远程 [[MCP 服务器]]连接
   - 支持认证头和 bearer-token
   - 具有良好的防火墙兼容性
   - 便于在不同环境中[[Configuration|配置]]

2. **Stdio 传输（本地）**：
   - 适用于本地 Node.js [[服务]]器
   - 通过标准输入输出进行通信
   - 无网络开销，性能较高
   - 适合开发和测试环境

3. **WebSocket 传输**：
   - 适用于需要实时双向通信的场景
   - 支持续长连接和实时消息推送
   - 适合需要频繁交互的工具

4. **[[SSE 传输]]（已弃用）**：
   - [[SSE 传输协议|Server-Sent Events]] 方式
   - 仅支持单向通信（[[服务]]器到客户端）
   - 已被其他传输方式取代

5. **选择准则**：
   - 远程[[服务]]：优先选择 HTTP
   - 本地[[服务]]：优先选择 Stdio
   - 实时交互：选择 WebSocket
   - 避免使用 SSE（已弃用）

## 来源
- [[claude-howto MCP 文档]] — 传输方式说明

## 相关
- [[MCP（Model Context Protocol）]] — part_of
- [[HTTP 传输协议]] — includes
- [[Stdio 传输协议]] — includes
- [[WebSocket 传输协议]] — includes
- [[SSE 传输]] — includes
- [[外部工具集成]] — relates_to