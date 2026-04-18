---
type: entity
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["编程语言", "脚本语言", "工具与框架"]
aliases: ["TS", "TypeScript Language"]
relates_to:
  - target: "[[Rust]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.7
supersedes: null
---

# TypeScript

由 Microsoft 开发的 JavaScript 超集语言，添加静态类型系统。编译为 JavaScript 后在 V8 等引擎上运行。

## 关键内容

1. **[[Codex CLI|Codex]] 原版实现语言**：[[Codex CLI]] 最初以 TypeScript 实现，后于 2025 年由 [[OpenAI]] 以 [[Rust]] 重写。
2. **被取代的原因**：
   - V8 冷启动开销大，不适合 CLI 工具
   - GC 抖动影响确定性延迟
   - Node native addon 绑定系统调用（[[Landlock]]/[[seccomp]]）繁琐
   - 需要 Node.js runtime 依赖，无法分发单一二进制
   - 事件循环单线程模型限制真并发
3. **适用场景**：TypeScript 适合 Web 前端和快速原型，但在需要 OS 级系统调用绑定的安全关键场景中不如 Rust。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — TypeScript vs Rust 对比表

## 相关

- [[Rust]] — 在系统编程场景中取代 TypeScript 的语言
- [[Codex CLI]] — 原版用 TypeScript，2025 年迁移至 Rust
