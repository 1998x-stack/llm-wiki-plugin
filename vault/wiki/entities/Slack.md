---
type: company
status: active
confidence: 0.8
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [通讯工具, 协作平台, MCP集成]
aliases: [Slack]
relates_to:
  - target: "[[MCP协议层]]"
    type: uses
  - target: "[[MCP]]"
    type: implements
  - target: "[[Codex CLI]]"
    type: uses
supersedes: null
---

# Slack

## 概述
企业级团队通讯与协作平台，在 Agent 生态中通过 [[MCP Prompts|MCP Server]] 集成，使 AI Agent 能够读取消息、发送通知、管理频道。

## 关键内容

1. **作为 [[MCP Prompts|MCP Server]] 集成**：通过 [[Python]] 模块 `slack_mcp_server` 封装 Slack API，在 [[Codex CLI]] 的 config.toml 中声明为可选 [[MCP 服务器]]（默认 `enabled = false`，按需启用）。

2. **[[Configuration|配置]]方式**：
   ```toml
   [mcp_servers.slack]
   command = "python"
   args = ["-m", "slack_mcp_server"]
   enabled = false   # 按需启用
   ```

3. **传输协议**：通常通过 stdio 方式运行——[[Codex CLI|Codex]] 启动 Slack [[MCP Prompts|MCP Server]] 进程，通过 stdin/stdout 通信，优点是简单且无端口冲突。

4. **在 Agent 生态中的角色**：作为 Agent 与人类团队的通讯桥梁，Agent 可通过 Slack MCP 工具读取频道消息、发送通知、响应 @mention，实现人机协作闭环。

## 来源
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[MCP协议层]] — uses
- [[MCP]] — implements
- [[Codex CLI]] — uses
