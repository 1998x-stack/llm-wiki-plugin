---
type: tool
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [linux, security, sandbox, kernel]
aliases: [seccomp, Secure Computing Mode, BPF 系统调用过滤]
relates_to:
  - Claude Code 沙箱机制: implements
  - App Sandbox: compares_to
supersedes: null
---

# seccomp-BPF

## 概述
seccomp-BPF 是 Linux 内核的安全机制，通过 Berkeley Packet Filter 规则过滤系统调用，允许进程限制自身可使用的系统调用集合，是构建沙箱和容器隔离的核心技术。

## 关键内容

1. **工作原理**：进程通过 prctl() 或 seccomp() 系统调用安装过滤规则，BPF 虚拟机在内核中对每个系统调用执行规则匹配，决定允许、拒绝或终止进程。

2. **在 Claude Code 中的应用**：Linux 版本的 Claude Code 沙箱使用 seccomp-BPF 过滤危险系统调用，如 setuid/setgid（权限提升）、网络接口修改、原始设备访问等。

3. **与 namespace 的配合**：seccomp-BPF 负责系统调用过滤，Linux namespace 负责文件系统、网络、PID 的隔离。两者结合提供完整的沙箱环境。

4. **与 App Sandbox 的比较**：seccomp-BPF 是 Linux 内核的底层机制，需要手动编写过滤规则；App Sandbox 是 macOS 的高层框架，使用声明式 entitlements。两者都提供内核级强制执行。

5. **性能影响**：seccomp-BPF 的系统调用过滤开销极低，文件访问 < 5% 额外开销，进程启动 ~10ms namespace 设置延迟，对交互式使用几乎不可感知。

6. **在容器技术中的广泛应用**：Docker、gVisor、Firecracker 等容器和微虚拟机技术都依赖 seccomp-BPF 作为安全边界的基础组件。

## 来源
- [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) — Anthropic Engineering Blog, 2025 年 10 月 20 日

## 相关
- [[Claude Code 沙箱机制]] — implements
- [[App Sandbox]] — compares_to
- [[纵深防御]] — part_of
