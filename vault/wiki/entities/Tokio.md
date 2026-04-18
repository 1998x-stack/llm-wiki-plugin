---
type: entity
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["工具", "异步运行时", "Rust生态", "工具与框架"]
aliases: ["Tokio Runtime", "Tokio async"]
relates_to:
  - target: "[[Rust]]"
    type: part_of
    confidence: 0.95
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Tokio

[[Rust]] 生态中最主流的异步运行时库，提供 async/await 支持、任务调度、I/O 多路复用和定时器。

## 关键内容

1. **真并发能力**：Tokio 多线程运行时突破单线程事件循环局限，是 [[Codex CLI]] 选择 Rust 而非 [[TypeScript]] 的关键因素之一。
2. **对比 Node.js 事件循环**：Node.js 单线程事件循环在同一时刻只能处理一个任务；Tokio 可在多个 OS 线程上并行调度异步任务。
3. **在 [[Codex CLI|Codex]] 中的角色**：[[Codex CLI|Codex]] 的并发操作（并行 subagent 调度、MCP 通信、沙箱进程管理）均依赖 Tokio 运行时。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — Rust vs TypeScript 并发对比

## 相关

- [[Rust]] — Tokio 所属的编程语言生态
- [[Codex CLI]] — 使用 Tokio 作为异步运行时的编码 Agent
