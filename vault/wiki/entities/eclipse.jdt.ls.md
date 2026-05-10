---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["eclipse.jdt.ls", "JDT Language Server", "Java Language Server"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "[[lsp4j]]"
    type: depends_on
    confidence: 0.85
supersedes: null
entity_type: tool
---

# eclipse.jdt.ls

## 概述
基于 Eclipse JDT 的 Java 语言[[服务]]器，由 Red Hat 维护，是最主流的 Java LSP 实现，支持 Java 8-23 全版本。

## 关键内容

1. **历史**：2016-10 首次发布（随 [[VS Code]] Java 插件），2024-10 v1.40.x 支持 Java 23，当前稳定版。

2. **架构**：基于 Eclipse Equinox OSGi 容器，包含 JDT Core（Java 解析、类型解析）、JDT UI（[[重构]]、代码生成）、M2Eclipse（Maven 集成）、Buildship（Gradle 集成）、LSP 协议层（自定义扩展）。

3. **生态位置**：Java 生态中最主流的 LSP 实现，被 [[VS Code]] Java 扩展包、VSCodium、Oni2 等广泛采用。

## 来源
- [[06_java_csharp_kotlin_lsp]] — Java/C#/Kotlin LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[lsp4j]] — depends_on
