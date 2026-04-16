---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["lsp4j", "Eclipse LSP4J", "Java LSP 库"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.9
  - target: "[[eclipse.jdt.ls]]"
    type: uses
    confidence: 0.85
supersedes: null
entity_type: tool
---

# lsp4j

## 概述
Eclipse 基金会维护的 Java LSP 库，为 Java 语言服务器开发提供协议定义和基础设施，是 [[eclipse.jdt.ls]] 等 Java LSP 实现的基础。

## 关键内容

1. **定位**：Java 生态中的 LSP SDK，提供 LSP 协议的 Java 类型定义和基础实现。

2. **使用方**：[[eclipse.jdt.ls]]、kotlin-language-server 等 Java/Kotlin LSP 服务器均基于 lsp4j 构建。

## 来源
- [[06_java_csharp_kotlin_lsp]] — Java/C#/Kotlin LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[eclipse.jdt.ls]] — uses
