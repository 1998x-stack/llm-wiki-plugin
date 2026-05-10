---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [protocol, ai-integration, external-services]
aliases: ["MCP", "Model Context Protocol", "模型上下文协议"]
relates_to: 
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[External Services]]"
    type: connects
  - target: "[[Boris Cherny]]"
    type: implemented_in
  - target: "[[MCP]]"
    type: relates_to
    confidence: 1.0
supersedes: null
---

# Model Context Protocol

## 概述
Model Context Protocol (MCP) 是 [[Claude Code]] 连接外部世界的标准化协议，提供统一接口替代碎片化的专用集成方案。这是一种标准化协议，用于接入外部[[服务]]到AI模型环境中，使模型能够与各种外部系统进行交互。

## 关键内容

1. **标准化接入**：提供统一的协议规范，使得不同类型的外部[[服务]]可以通过一致的方式接入AI系统。

2. **基本架构**：
   - 客户端：[[Claude Code]]
   - [[服务]]端：[[MCP Prompts|MCP Server]]（封装外部[[服务]]访问逻辑，如 [[GitHub]] / DB / Browser 等）
   - 通信：JSON-RPC 通过 stdio/SSE/HTTP

3. **传输模式**：
   - `stdio`：本地进程，原生隔离，不经过网络
   - `SSE`：远程 HTTP 流式，实时推送
   - `HTTP`：远程 HTTP 非流式，简单请求-响应

4. **[[Configuration|配置]]管理**：
   - 用户级[[Configuration|配置]]：~/.claude.json
   - 项目级[[Configuration|配置]]：./.mcp.json（提交到 Git）
   - 项目级 MCP 补充（不覆盖）用户级 MCP

5. **外部[[服务]]集成**：允许AI模型访问如[[GitHub]]、数据库、监控系统(Sentry)、通讯工具([[Slack]])等各种外部[[服务]]。

6. **在[[Claude Code]]中的应用**：[[Claude Code]]使用[[MCP（Model Context Protocol）|MCP协议]]来标准化外部[[服务]]接入，使其能够连接到各种第三方[[服务]]，扩展其功能边界。

7. **[[Connect]]能力基元**：作为[[Claude Code四大能力基元]]之一的"[[Connect]]"的基础，MCP使模型可以连接到外部[[服务]]。

8. **Token 保护机制**：
   - 警告阈值：10,000 tokens
   - 默认上限：25,000 tokens
   - 最佳实践：让 [[MCP 服务器]]分页/过滤响应，而非增加上限

## 来源
- [[05_to_08_combined.md]] — 07 · MCP（Model Context Protocol）
- [[01_system_overview.md]] — Tech Stack部分和四大能力基元部分

## 相关
- [[Claude Code]] — relates_to
- [[External Services]] — implements
- [[AI Integration]] — relates_to
- [[MCP]] — relates_to
- [[SSE 传输协议]] — relates_to
- [[HTTP 传输协议]] — relates_to
- [[Stdio 传输协议]] — relates_to