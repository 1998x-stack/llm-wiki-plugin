---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude-code, protocol, transport, http, mcp, integration, AI工程]
aliases: ["HTTP Transport", "HTTP Transport Protocol", "MCP HTTP Connection"]
relates_to:
  - target: "[[MCP]]"
    type: implements
    confidence: 0.85
  - target: "[[Stdio 传输协议]]"
    type: compares_to
    confidence: 0.75
  - target: "[[WebSocket 传输协议]]"
    type: compares_to
    confidence: 0.7
  - target: "[[SSE 传输]]"
    type: supersedes
    confidence: 0.7
  - target: "[[OAuth 2.0 认证]]"
    type: supports
    confidence: 0.8
---
# HTTP 传输协议

## 概述
MCP ([[Model Context Protocol]]) 的 HTTP 传输协议，作为推荐的连接方式，支持认证头和 bearer-token 等安全机制，适用于远程 [[MCP 服务器]]连接。

## 关键内容
1. **优势**：
   - 支持 bearer-token 认证
   - 适合远程[[服务]]连接
   - 更好的网络隔离和防火墙兼容性

2. **[[Configuration|配置]]方式**：
   ```toml
   [mcp_servers.example]
   endpoint = "http://localhost:8080"
   auth_header = "Bearer ${MCP_TOKEN}"
   ```

3. **认证支持**：
   - HTTP Basic Authentication
   - Bearer Token 认证
   - 自定义认证头

4. **与 Stdio 对比**：
   - HTTP：适合远程[[服务]]，支持认证
   - Stdio：适合本地进程，无网络开销

5. **适用场景**：
   - 远程 [[MCP 服务器]]
   - 需要认证的安全连接
   - 跨网络边界的工具集成

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 传输方式介绍

## 相关
- [[MCP]] — implements
- [[Stdio 传输协议]] — compares_to
- [[WebSocket 传输协议]] — compares_to
- [[OAuth 2.0 认证]] — supports
- [[SSE 传输]] — supersedes