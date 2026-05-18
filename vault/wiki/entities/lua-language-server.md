---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架", Lua编程]
aliases: ["lua-language-server", "LuaLS", "sumneko lua", "Lua 语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
supersedes: null
entity_type: tool
---

# lua-language-server

## 概述
Lua 最主流的 LSP [[服务]]器，由 sumneko（孙蒙可）开发，现由 LuaLS 组织维护，使用 Lua/C++ 实现，2022 年通过注释系统重写大幅提升类型推断能力。

## 关键内容

1. **历史**：2019 年 1.x [[VS Code]] 插件初始版本，2021 年 2.x [[语义分析]]重写，2022-07 3.0.0 注释系统重写（类型推断大幅提升），2024-10 3.11.x 当前稳定版。

2. **实现**：核心用 Lua 编写，外围用 C++，兼顾开发效率和性能。

3. **特性**：类型推断、[[语义分析]]、Workspace diagnostics、Lazy loading、类型系统增强。

## 来源
- [[07_lua_haskell_ruby_php_lsp]] — Lua/Haskell/Ruby/PHP LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
