---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["gopls", "Go Language Server", "Go 官方语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
supersedes: null
entity_type: tool
---

# gopls

## 概述
Go 官方语言服务器，由 [[Google]] Go 团队在 `golang.org/x/tools` 中维护，提供完整的 Go 语言 LSP 支持，包括代码补全、跳转定义、诊断、重构等功能。

## 关键内容

1. **历史**：2018-01 启动（原名 langserver-go），2019-05 v0.1.0 首次发布，2023-04 v0.11.0 泛型完整支持，2025-01 v0.17.x 当前稳定版。

2. **架构**：位于 `golang.org/x/tools/gopls`，包含 LSP 协议层（server.go/cache/source）、语言分析核心（completion/hover/rename）、CLI 命令（check/format 等）、配置管理。

3. **关键特性**：Go modules 支持、[[Semantic Tokens（语义标记）|语义高亮]]、Call Hierarchy、Inlay Hints、Workspace symbols、零配置 workspace、多工作区支持。

## 来源
- [[04_go_lsp]] — Go LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
