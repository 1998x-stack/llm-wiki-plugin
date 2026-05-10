---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [protocol, communication, streaming]
aliases: ["SSE 传输协议", "Server-Sent Events", "SSE", "服务器发送事件"]
relates_to: []
supersedes: null
---

# SSE 传输协议

## 概述
SSE（Server-Sent Events）传输协议是 [[MCP（Model Context Protocol）]]支持的三种传输模式之一，提供远程 HTTP 流式通信能力，适用于实时推送场景。

## 关键内容

1. **基本特征**：
   - 远程 HTTP 流式传输模式
   - 适用于实时推送场景
   - 是 [[MCP（Model Context Protocol）]]支持的传输模式之一

2. **与其他传输模式对比**：
   - `stdio`：本地进程，原生隔离，不经过网络
   - `SSE`：远程 HTTP 流式，实时推送（当前正在编辑的页面）
   - `HTTP`：远程 HTTP 非流式，简单请求-响应

3. **适用场景**：
   - 需要实时数据推送的[[服务]]
   - 远程 [[MCP 服务器]]的流式响应
   - 长连接场景下的双向通信

4. **技术特点**：
   - 基于 HTTP 协议
   - [[服务]]器主动向客户端推送数据
   - 单向通信（[[服务]]器到客户端）

## 来源
- [[05_to_08_combined.md]] — 07 · MCP（Model Context Protocol）

## 相关
- [[MCP]] — relates_to
- [[Model Context Protocol]] — relates_to
- [[HTTP 传输协议]] — relates_to
- [[Stdio 传输协议]] — relates_to