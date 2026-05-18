---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [MCP, "Claude Code", 工具集成, API协议, 外部工具, 工具与框架]
aliases: ["Model Context Protocol", "MCP协议"]
relates_to:
  - target: "[[Claude Code]]"
    type: implements
  - target: "[[外部工具集成]]"
    type: extends
  - target: "[[API协议]]"
    type: implements
supersedes: null
---

# MCP（Model Context Protocol）

## 概述
MCP（[[Model Context Protocol]]）是 [[Claude Code]] 访问外部工具、[[服务]]和 API 的标准协议，允许将 [[GitHub]]、数据库、文件系统、聊天系统等外部系统集成到 [[Claude_Code|Claude]] 环境中。

## 关键内容

1. **MCP 架构**：
   - 由 [[Claude Code]]、MCP server 和外部工具或数据源三部分构成
   - [[Claude_Code|Claude]] 通过 MCP 协议向 server 发起工具调用，并把结果带回当前会话

2. **MCP 生态**：
   - 支持 [[GitHub]] 集成、数据库集成、文件系统集成
   - 支持组织内部工具和第三方[[服务]]

3. **传输方式**：
   - HTTP 传输（推荐）
   - Stdio 传输（本地）
   - WebSocket 传输（适用于需要实时双向通信的场景）
   - [[SSE 传输]]（已弃用）

4. **安全特性**：
   - 支持 [[OAuth 2.0 认证]]
   - 通过[[Environment Variables|环境变量]]管理认证信息
   - 最小[[Permissions|权限]]原则的安全控制

5. **[[Configuration|配置]]管理**：
   - 支持项目级和用户级的不同作用域
   - 提供命令行工具进行[[服务]]器管理（添加、列出、删除等）
   - 支持动态工具更新和实时感知变化

6. **使用方式**：
   - 可将 [[MCP Prompts]] 暴露为 [[Slash Commands]]（如 `/mcp__github__list_prs`）
   - 支持通过 `@` 提及使用 MCP 资源
   - 可作为[[代码执行]]接口减少上下文膨胀

## 来源
- [[claude-howto MCP 文档]] — 概念介绍、架构说明

## 相关
- [[Claude Code]] — implements
- [[外部工具集成]] — extends
- [[API协议]] — implements
- [[MCP 服务器]] — relates_to
- [[MCP 传输方式]] — relates_to
- [[Subagents]] — relates_to
- [[Skills]] — relates_to
- [[Slash Commands]] — relates_to