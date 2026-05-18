---
type: concept
status: active
confidence: 0.6
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [deprecated, protocol, transport, sse, mcp, legacy, 推荐系统]
aliases: ["SSE Transport", "Server-Sent Events Transport", "SSE 传输", "MCP SSE Connection"]
relates_to:
  - target: "[[MCP]]"
    type: implements
    confidence: 0.6
  - target: "[[HTTP 传输协议]]"
    type: superseded_by
    confidence: 0.8
  - target: "[[Stdio 传输协议]]"
    type: compares_to
    confidence: 0.5
  - target: "[[WebSocket 传输协议]]"
    type: compares_to
    confidence: 0.6
---
# SSE 传输

## 概述
MCP ([[Model Context Protocol]]) 的 [[SSE 传输协议|Server-Sent Events]] (SSE) 传输协议，一种已被弃用的传输方式，曾用于单向[[服务]]器到客户端的消息推送。

## 关键内容
1. **历史地位**：
   - 在早期 MCP 版本中使用的传输协议
   - 现已被 HTTP 和其他更稳定的传输方式取代

2. **工作原理**：
   - 基于 HTTP 的单向通信
   - [[服务]]器向客户端推送消息
   - 保持长连接以持续传输数据

3. **局限性**：
   - 仅支持单向通信（[[服务]]器到客户端）
   - 连接稳定性不如现代协议
   - 维护和调试困难

4. **现状**：
   - 已被弃用，不再推荐使用
   - 新[[Configuration|配置]]应优先选择 HTTP 或 Stdio 方式
   - 仅在维护旧系统时可能遇到

5. **替代方案**：
   - [[HTTP 传输协议]]：双向通信，更好的认证支持
   - [[WebSocket 传输协议]]：实时双向通信
   - [[Stdio 传输协议]]：本地进程高效通信

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 传输方式历史介绍

## 相关
- [[MCP]] — implements
- [[HTTP 传输协议]] — superseded_by
- [[Stdio 传输协议]] — compares_to
- [[WebSocket 传输协议]] — compares_to
- [[MCP协议层]] — related_to