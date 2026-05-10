---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["vtsls", "VTSLS", "VS Code TypeScript Language Server"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "[[typescript-language-server]]"
    type: compares_to
    confidence: 0.8
supersedes: null
entity_type: tool
---

# vtsls

## 概述
[[VS Code]] [[TypeScript]] 扩展包装的 [[TypeScript]] 语言[[服务]]器，比 [[typescript-language-server]] 功能更强，提供更完整的 [[TypeScript]]/JavaScript LSP 体验。

## 关键内容

1. **定位**：基于 [[VS Code]] 内部 [[TypeScript]] 语言[[服务]]实现，提供比开源 [[typescript-language-server]] 更丰富的功能。

2. **与 [[typescript-language-server]] 对比**：vtsls 利用 [[VS Code]] 内部的 TS 扩展，提供更强的类型推断和代码分析能力。

3. **生态位置**：在 [[TypeScript]] LSP 生态中，与 [[typescript-language-server]]、biome、deno lsp、eslint-lsp 等并存。

## 来源
- [[02_typescript_lsp]] — TypeScript/JavaScript LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[typescript-language-server]] — compares_to
