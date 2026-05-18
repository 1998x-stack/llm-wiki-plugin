---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude-code, protocol, transport, websocket, mcp, real-time, AI工程]
aliases: ["WebSocket Transport", "WebSocket Transport Protocol", "MCP WebSocket Connection"]
relates_to:
  - target: "[[MCP]]"
    type: implements
    confidence: 0.8
  - target: "[[HTTP 传输协议]]"
    type: compares_to
    confidence: 0.7
  - target: "[[Stdio 传输协议]]"
    type: compares_to
    confidence: 0.65
  - target: "[[SSE 传输协议]]"
    type: compares_to
    confidence: 0.7
  - target: "[[实时双向通信]]"
    type: enables
    confidence: 0.85
---
# WebSocket 传输协议

## 概述
MCP ([[Model Context Protocol]]) 的 WebSocket 传输协议，支持实时双向通信，适用于需要[[服务]]器主动推送消息的场景。

## 关键内容
1. **特性**：
   - 支持实时双向通信
   - [[服务]]器可主动向 [[Claude_Code|Claude]] 推送消息
   - 长连接，低延迟

2. **适用场景**：
   - 需要[[服务]]器主动通知的场景
   - 实时状态更新
   - 长时间运行的任务状态反馈

3. **与 HTTP/Stdio 对比**：
   - WebSocket：双向通信，实时推送，长连接
   - HTTP：请求-响应模式，单向通信
   - Stdio：本地双向通信，无网络传输

4. **[[Configuration|配置]]特点**：
   - 需要建立持久连接
   - 支持心跳和连接保活
   - 适用于长时间运行的交互

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 传输方式介绍

## 相关
- [[MCP]] — implements
- [[HTTP 传输协议]] — compares_to
- [[Stdio 传输协议]] — compares_to
- [[实时双向通信]] — enables
- [[MCP协议层]] — related_to