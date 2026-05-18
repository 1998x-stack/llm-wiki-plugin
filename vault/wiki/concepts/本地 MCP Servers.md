---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude-code, mcp, local-services, tool-system, integration, AI工程]
aliases: ["Local MCP Servers", "本地MCP服务器", "本地 MCP Server"]
relates_to:
  - target: "[[MCP]]"
    type: implements
    confidence: 0.9
  - target: "[[Stdio 传输协议]]"
    type: uses
    confidence: 0.9
  - target: "[[HTTP 传输协议]]"
    type: compares_to
    confidence: 0.7
  - target: "[[Claude Code]]"
    type: part_of
    confidence: 0.85
---
# 本地 MCP Servers

## 概述
本地 MCP ([[Model Context Protocol]]) [[服务]]器，是在本地机器上运行的 MCP [[服务]]，通常作为子进程与 [[Claude Code]] 通信，提供高效的本地工具集成能力。

## 关键内容
1. **特点**：
   - 在本地机器上运行
   - 通过子进程与 [[Claude_Code|Claude]] 通信
   - 低延迟，高性能
   - 无需网络连接

2. **工作方式**：
   - [[Claude_Code|Claude]] 启动本地工具作为子进程
   - 通过 [[Stdio 传输协议]]进行通信
   - 适用于本地开发和调试

3. **典型应用**：
   - 本地文件系统操作工具
   - 本地开发环境集成
   - 本地数据库客户端
   - 本地 Git 工具封装

4. **与远程 MCP 对比**：
   - 本地 MCP：低延迟，高效率，适用于本地工具
   - 远程 MCP：支持远程[[服务]]，需要网络连接和认证

5. **[[Configuration|配置]]示例**：
   ```toml
   [mcp_servers.local_tool]
   command = "node"
   args = ["local-server.js"]
   ```

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 本地服务介绍

## 相关
- [[MCP]] — implements
- [[Stdio 传输协议]] — uses
- [[HTTP 传输协议]] — compares_to
- [[Claude Code]] — part_of
- [[MCP协议层]] — related_to