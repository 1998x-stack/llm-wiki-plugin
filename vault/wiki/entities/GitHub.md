---
type: company
status: active
confidence: 0.85
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [开发工具, 代码托管, 协作平台]
aliases: [GitHub, Github]
relates_to:
  - target: "[[MCP协议层]]"
    type: uses
  - target: "[[Codex CLI]]"
    type: uses
  - target: "[[Cursor]]"
    type: uses
supersedes: null
---

# GitHub

## 概述
全球最大代码托管与开发者协作平台，提供 Git [[仓库]]管理、Pull Request、Issue 追踪、CI/CD 等功能，在 Agent 生态中通过 [[MCP Prompts|MCP Server]] 暴露为可调用的工具[[服务]]。

## 关键内容

1. **作为 [[MCP Prompts|MCP Server]] 集成**：通过 `@modelcontextprotocol/server-github` 包，GitHub API 被封装为 MCP 工具，任何支持 MCP 的 Agent（如 [[Codex CLI]]、[[Cursor]]）均可直接调用，无需定制集成代码。

2. **MCP 工具示例**：
   - 读取 GitHub PR 内容（`read-only` annotation → 自动放行）
   - 关闭 GitHub Issues（`destructive` annotation → 强制审批，即使 `approval_policy = "never"`）
   - 代码搜索、[[仓库]]管理、文件操作等

3. **安全控制**：MCP 工具的 `annotations` 字段标记操作性质——`read-only: true` 自动放行，`destructive: true` 强制触发 [[Approval Gate UI]] 审批流程，构成 [[纵深防御]] 的一环。

4. **[[Environment Variables|环境变量]][[Configuration|配置]]**：通过 config.toml 中的 `env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }` 传递认证凭据，受 [[Codex配置系统]] 管理。

## 来源
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[MCP协议层]] — uses
- [[Codex CLI]] — uses
- [[Cursor]] — uses
