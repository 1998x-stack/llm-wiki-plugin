---
type: tool
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [macos, security, sandbox, apple, AI工程]
aliases: [Apple App Sandbox, macOS Sandbox]
relates_to:
  - Claude Code 沙箱机制: implements
  - seccomp-BPF: compares_to
supersedes: null
---

# App Sandbox

## 概述
App Sandbox 是 Apple 提供的 macOS 安全框架，通过声明式[[权限模型]]（entitlements）和系统级执行保证，限制应用程序对文件系统、网络、硬件等系统资源的访问范围。

## 关键内容

1. **声明式[[权限模型]]**：开发者通过 entitlements 文件声明应用需要的[[Permissions|权限]]，系统在运行时强制执行这些限制。[[Permissions|权限]]包括文件访问、网络请求、硬件访问等类别。

2. **系统级执行保证**：App Sandbox 由 macOS 内核强制执行，应用自身无法绕过或修改[[Claude Code 沙箱机制|沙箱]]限制，提供了比应用层[[Permissions|权限]]检查更强的安全保障。

3. **在 [[Claude Code]] 中的应用**：macOS 版本的 [[Claude Code]] [[Claude Code 沙箱机制|沙箱]]利用 App Sandbox 框架实现文件系统隔离和网络访问控制，确保 Agent 操作被限制在项目目录和预定义资源范围内。

4. **与 Linux [[seccomp-BPF]] 的比较**：App Sandbox 是 Apple 生态的专有框架，提供高层声明式 API；[[seccomp-BPF]] 是 Linux 内核的系统调用过滤机制，更底层但更灵活。两者都提供内核级强制执行保证。

5. **性能影响**：App Sandbox 的[[Permissions|权限]]检查开销极小，文件访问 < 5% 额外开销，对交互式使用几乎不可感知。

## 来源
- [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) — Anthropic Engineering Blog, 2025 年 10 月 20 日

## 相关
- [[Claude Code 沙箱机制]] — implements
- [[seccomp-BPF]] — compares_to
