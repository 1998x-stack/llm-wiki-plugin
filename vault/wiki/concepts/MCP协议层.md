---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [MCP Layer, Model Context Protocol, MCP协议]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.9
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.75
  - target: "[[Codex多Agent调度]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# MCP协议层

[[Codex CLI]] 的工具连接协议层。MCP（Model Context Protocol）是 Anthropic 提出的开放协议，让工具与 Agent 解耦——"USB-C 接口"设计。[[Codex CLI|Codex]] 同时扮演 **MCP 客户端**（连接外部工具）和 **MCP 服务端**（将自身暴露给其他 Agent）两个角色。

## 核心价值

传统方式每个工具都需要定制集成代码。MCP 方式：Agent 通过统一协议连接任意 MCP 兼容工具，工具复用，无需定制。

## Codex 双重身份

**作为 MCP Client**：启动时连接 config.toml 声明的 MCP 服务器，通过 `tools/list` 发现工具，注入 LLM system prompt，将 LLM 的 tool_call 请求路由到对应服务器。

**作为 MCP Server**：

```bash
codex mcp-server  # 启动后暴露 codex_exec、codex_review 等工具
```

其他 Agent（Cursor、另一个 Codex 实例）可将整个 Codex Agent 作为工具节点调用——实现 Agent 可组合性。

## MCP Client 配置

```toml
# ~/.codex/config.toml
[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]
enabled = true

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }
```

## 传输协议

| 协议 | 特点 | 适用场景 |
|------|------|---------|
| stdio | 最常用，Codex 启动子进程通信，无端口冲突 | 本地工具 |
| HTTP/SSE | 支持 bearer-token 认证 | 远程服务 |
| WebSocket | 双向实时，适合服务器主动推送 | 实时场景 |

## Plugins 系统

2026 年引入的基于 MCP 的插件系统：自动从 plugin registry 同步（无需手动配置）、统一处理认证、自动版本管理、TUI 内 `/plugins` 面板集成。

## 安全控制

MCP 工具调用受 Approval 机制保护：
- `read-only: true` → 自动放行
- `destructive: true` → 强制审批（即使 `approval_policy = "never"`）

**环境变量隔离**（Shell Environment Policy）：精细控制哪些 env var 传递给子进程，防止密钥泄露。默认自动排除包含 `KEY/SECRET/TOKEN` 的变量。

## 工程哲学

> **MCP Layer 把"工具集成"从编程问题变成配置问题。** Codex 同时是客户端和服务端，实现了 Agent 的"可组合性"——任何 Codex 实例都可以成为更大 Agent 系统的一个工具节点。

## 来源

- `raw/articles/ai-tools/codex/06_codex_mcp_layer.md`
