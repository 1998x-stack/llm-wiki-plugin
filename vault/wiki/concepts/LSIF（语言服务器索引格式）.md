---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["Language Server Index Format", "语言服务器索引格式"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: extends
    confidence: 0.9
  - target: "[[Sourcegraph]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# LSIF（语言服务器索引格式）

## 概述
Language Server Index Format 是 LSP 的离线版本，将语言[[服务]]器的分析结果序列化为图结构，用于代码搜索和静态代码导航，被 [[GitHub]] 和 Sourcegraph 广泛采用。

## 关键内容

1. **图结构模型**：LSIF 将代码分析结果表示为图：`vertex:document → contains → vertex:range → resultSet`，其中 resultSet 包含 definitionResult、referencesResult、hoverResult 等。

2. **与 LSP 的关系**：LSP 是实时交互协议（编辑器↔[[服务]]器），LSIF 是静态索引格式（预生成、可查询）。LSIF 相当于 LSP 的"快照"。

3. **生成工具**：各语言均有对应工具——Go（lsif-go）、[[TypeScript]]（lsif-tsc）、[[Python]]（lsif-py）、Java（lsif-java）、C++（lsif-clang）、Rust（[[rust-analyzer]] --dump-lsif）。

4. **应用场景**：[[GitHub]] 代码导航、Sourcegraph 代码搜索、静态代码分析工具。

## 来源
- [[00_lsp_overview]] — LSP 语言服务器协议总览与架构调研

## 相关
- [[LSP（语言服务器协议）]] — extends
- [[Sourcegraph]] — uses
- [[Semantic Tokens（语义标记）]] — compares_to（LSIF 用于静态导航，Semantic Tokens 用于实时着色）
