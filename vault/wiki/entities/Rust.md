---
type: entity
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["编程语言", "系统编程", "工具与框架"]
aliases: ["Rust Programming Language"]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[TypeScript]]"
    type: compares_to
    confidence: 0.9
supersedes: null
---

# Rust

系统级编程语言，以内存安全（无 GC）、零成本抽象和真并发为核心特性。由 Mozilla 研究院发起，现为 Rust Foundation 维护。

## 关键内容

1. **内存安全无 GC**：所有权系统 + 借用检查器在编译期消除数据竞争和悬垂指针，无需运行时 GC 抖动——对延迟敏感的工具（如 CLI Agent）至关重要。
2. **系统调用直连**：可直接绑定 [[Landlock]]/[[seccomp]] 等 Linux 内核 API，无需 Node native addon 的繁琐桥接。这是 [[Codex CLI]] 从 [[TypeScript]] 迁移到 Rust 的核心动因。
3. **单一静态二进制**：零运行时依赖分发，对比 Node.js 需要捆绑 V8 引擎。
4. **真并发**：[[Tokio]] 运行时提供 async/await + 多线程调度，突破事件循环单线程瓶颈。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — Rust 重写决策章节

## 相关

- [[Codex CLI]] — 以 Rust 重写的本地编码 Agent
- [[TypeScript]] — Codex 原版使用的语言，被 Rust 取代
- [[Tokio]] — Rust 生态的异步运行时
