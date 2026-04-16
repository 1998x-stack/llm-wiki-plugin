---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["typescript-language-server", "tsserver wrapper", "TS LSP"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "[[tsserver]]"
    type: depends_on
    confidence: 0.95
supersedes: null
entity_type: tool
---

# typescript-language-server

## 概述
TypeScript 最主流的 LSP 实现，由 Type[[Dieter Fox|Fox]] 维护，作为 TypeScript 内置 tsserver 的 LSP 适配层，将 tsserver 的内部协议包装为标准 LSP 协议。

## 关键内容

1. **架构**：编辑器 (LSP Client) → JSON-RPC (stdio) → typescript-language-server (Node.js) → TypeScript TSServer Protocol (IPC/pipe) → tsserver（TypeScript 内置语言服务）。

2. **版本演进**：2016-2019 早期 theia-ide 版本，2021-03 重写为 1.0.0（完善 LSP 3.16 支持），2022-06 3.0.0（Inlay Hints），2024-09 4.3.3（TS 5.6 支持）。

3. **能力覆盖**：代码补全、跳转定义、类型检查、重构、[[Semantic Tokens（语义标记）|语义高亮]]、Call Hierarchy、Inlay Hints 等。

## 来源
- [[02_typescript_lsp]] — TypeScript/JavaScript LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[tsserver]] — depends_on
