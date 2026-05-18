---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude-code, protocol, transport, stdio, mcp, integration, AI工程]
aliases: ["Stdio Transport", "Stdio Transport Protocol", "MCP Stdio Connection"]
relates_to:
  - target: "[[MCP]]"
    type: implements
    confidence: 0.85
  - target: "[[HTTP 传输协议]]"
    type: compares_to
    confidence: 0.75
  - target: "[[本地 MCP Servers]]"
    type: enables
    confidence: 0.8
---
# Stdio 传输协议

## 概述
MCP ([[Model Context Protocol]]) 的标准输入输出 (Stdio) 传输协议，作为本地连接的主要方式，通过子进程通信实现 [[Claude_Code|Claude]] 与 [[MCP 服务器]]间的交互。

## 关键内容
1. **工作原理**：
   - [[Claude_Code|Claude]] 启动 [[MCP 服务器]]作为子进程
   - 通过标准输入输出管道进行通信
   - 无额外网络开销

2. **[[Configuration|配置]]方式**：
   ```toml
   [mcp_servers.example]
   command = "node"
   args = ["server.js"]
   ```

3. **优势**：
   - 本地进程通信，性能最优
   - 无需网络[[Configuration|配置]]
   - 适用于本地工具集成

4. **适用场景**：
   - 本地运行的 [[MCP 服务器]]
   - 无需跨网络访问的工具
   - 与 [[Claude_Code|Claude]] 同机部署的[[服务]]

5. **与 HTTP 对比**：
   - Stdio：本地进程，高性能，无认证
   - HTTP：远程[[服务]]，支持认证，网络通信

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 传输方式介绍

## 相关
- [[MCP]] — implements
- [[HTTP 传输协议]] — compares_to
- [[本地 MCP Servers]] — enables
- [[MCP协议层]] — related_to