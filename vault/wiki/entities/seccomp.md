---
type: entity
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["工具", "安全", "Linux内核", "工具与框架"]
aliases: ["Secure Computing Mode", "seccomp-bpf"]
relates_to:
  - target: "[[Codex沙箱系统]]"
    type: implements
    confidence: 0.95
  - target: "[[Landlock]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# seccomp

Linux 内核的系统调用过滤机制（Secure Computing Mode），通过 BPF 规则白名单/黑名单限制进程可调用的内核 API。

## 关键内容

1. **系统调用级隔离**：seccomp 在进程与内核之间设置过滤层，只允许预定义的系统调用通过，从根本上缩小攻击面。
2. **在 [[Codex CLI|Codex]] 中的角色**：[[Codex沙箱系统]] 在 Linux 平台上将 seccomp 与 [[Landlock]] 组合使用——seccomp 管"能做什么操作"，[[Landlock]] 管"能访问什么文件"。
3. **seccomp-bpf**：现代版本基于 Berkeley Packet Filter 语法，支持复杂的过滤规则（参数匹配、位掩码等）。
4. **Rust 绑定优势**：Rust 可直接调用 seccomp syscall，无需 Node.js native addon 的桥接层。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — 沙箱执行层章节 & Rust 重写决策
- [[raw/articles/ai-tools/codex/03_codex_sandbox_system.md]] — 第 2.2 节：seccomp 作为第二层系统调用过滤

## 相关

- [[Codex沙箱系统]] — 使用 seccomp 作为 Linux 平台系统调用过滤方案
- [[Landlock]] — 与 seccomp 配合使用的文件系统隔离机制
