---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["rust-analyzer", "RA", "Rust 语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "rls"
    type: supersedes
    confidence: 0.9
  - target: "[[Salsa]]"
    type: depends_on
    confidence: 0.9
supersedes: rls
entity_type: tool
---

# rust-analyzer

## 概述
Rust 官方语言[[服务]]器，2022 年合并进 rust-lang 组织，取代 rls 成为 Rust 生态的标准 LSP 实现，采用 Salsa 增量[[计算]]框架实现高效的代码分析。

## 关键内容

1. **历史演进**：2018 年 Aleksey Kladov (@matklad) 启动实验项目，2020 年 Rust 官方宣布其为 rls 继任者，2022 年合并进 rust-lang 组织，2023 年随 rustup 默认分发。

2. **架构设计**：采用 Salsa 增量[[计算]]框架（基于依赖追踪的增量分析，只重算变更部分）、Resilient 解析（即使代码有语法错误也能提供[[服务]]）、离散数据结构 CST（保留所有空白/注释信息）、无 panic 设计。

3. **核心模块**：`rust-analyzer/`（LSP Server 入口）、`ide/`（IDE 功能层，无 LSP 依赖）、`hir/`（高层中间表示，含 hir_def/hir_ty/hir_expand）、`syntax/`（CST 解析器，基于 rowan 库）。

4. **发布节奏**：每周滚动发布，2025 年接近 1.0 稳定性。

## 来源
- [[03_rust_lsp]] — Rust LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- rls — supersedes
- [[Salsa]] — depends_on
