---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架", C++编程]
aliases: ["ccls", "CCLS", "C++ Language Server"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.9
  - target: "[[clangd]]"
    type: compares_to
    confidence: 0.8
supersedes: null
entity_type: tool
---

# ccls

## 概述
高性能 [[clangd|C/C++ 语言服务器]]，是 cquery（已停更）的继任者，在 [[C++]]17 支持上表现优秀，是 [[clangd]] 的主要替代方案。

## 关键内容

1. **历史**：cquery 停更后，ccls 作为其继任者继续开发，专注于高性能和 [[C++]] 标准支持。

2. **定位**：[[clangd]] 的高性能替代方案，特别适合大型 [[C++]] 项目。

3. **与 [[clangd]] 对比**：ccls 在 [[C++]]17 支持上表现更优秀，但 [[clangd]] 功能更全、官方维护。

## 来源
- [[05_cpp_lsp]] — C/C++ LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[clangd]] — compares_to
