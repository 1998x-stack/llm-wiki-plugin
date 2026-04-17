---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["hls", "Haskell Language Server", "Haskell 语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
supersedes: null
entity_type: tool
---

# hls（Haskell Language Server）

## 概述
Haskell 官方语言服务器，提供完整的 Haskell 语言 LSP 支持，包括类型检查、代码补全、重构、诊断等功能。

## 关键内容

1. **定位**：Haskell 生态的官方 LSP 实现，取代早期的 haskell-ide-engine (hie)。

2. **特性**：类型检查、代码补全、重构、诊断、Inlay Hints、Call Hierarchy 等完整 LSP 能力。

## 来源
- [[07_lua_haskell_ruby_php_lsp]] — Lua/Haskell/Ruby/PHP LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
