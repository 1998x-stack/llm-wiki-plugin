---
type: entity
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["rls", "Rust Language Server", "Rust 首个语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.9
  - target: "[[rust-analyzer]]"
    type: supersedes
    confidence: 0.95
supersedes: null
entity_type: tool
---

# rls（Rust Language Server）

## 概述
Rust 官方首个 LSP 实现，2017 年发布，2022 年被 [[rust-analyzer]] 取代后正式弃用，是 [[rust-analyzer|Rust 语言服务器]]发展的起点。

## 关键内容

1. **历史**：2017 年发布作为 Rust 首个官方语言[[服务]]器，2020 年 [[rust-analyzer]] 被宣布为其继任者，2022-09 正式弃用。

2. **局限性**：相比 [[rust-analyzer]]，rls 在增量分析、错误恢复、解析精度等方面存在不足，导致社区转向 [[rust-analyzer]]。

3. **被取代原因**：[[rust-analyzer]] 采用 Salsa 增量[[计算]]框架、Resilient 解析、CST 数据结构等创新设计，在性能和用户体验上全面超越 rls。

## 来源
- [[03_rust_lsp]] — Rust LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[rust-analyzer]] — supersedes
