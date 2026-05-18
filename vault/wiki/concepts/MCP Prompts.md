---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude, mcp, api, integration, AI工程]
aliases: ["MCP Prompt", "MCP Server"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[HTTP 传输协议]]"
    type: uses
    confidence: 0.7
  - target: "[[Stdio 传输协议]]"
    type: uses
    confidence: 0.8
  - target: "[[MCPorter]]"
    type: extends
    confidence: 0.6
supersedes: null
---

# MCP Prompts

## 概述
MCP ([[Model Context Protocol]]) Prompts 是通过 MCP servers 暴露的命令，可通过[[Slash Commands|斜杠命令]]形式调用外部[[服务]]的功能。

## 关键内容

1. **命令格式**：
   - `/mcp__<server-name>__<prompt-name> [arguments]`
   - 例如：`/mcp__github__list_prs`、`/mcp__github__pr_review 456`

2. **[[Permissions|权限]]管理**：
   - `mcp__github` - 访问整个 [[GitHub]] MCP server
   - `mcp__github__*` - 通配符访问全部工具
   - `mcp__github__get_issue` - 访问某个特定工具

3. **应用场景**：
   - 与外部[[服务]]集成（如 [[GitHub]]、JIRA）
   - 执行需要认证的操作
   - 自动化外部系统任务

## 来源
- [[Claude How To Slash Commands Reference]] — 官方文档

## 相关
- [[Slash Commands]] — part_of
- [[Skills]] — related_to
- [[Claude Code]] — part_of