---
type: entity
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-19
source_count: 2
tags: ["工具", "安全", "Linux内核", "工具与框架"]
aliases: ["Linux Landlock", "Landlock LSM"]
relates_to:
  - target: "[[Codex沙箱系统]]"
    type: implements
    confidence: 0.95
  - target: "[[seccomp]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# Landlock

Linux 内核的安全模块（Landlock LSM），从 5.13 版本引入，允许非特权进程创建沙箱，限制自身对文件系统的访问[[Permissions|权限]]。

## 关键内容

1. **文件系统隔离**：Landlock 通过限制进程能访问的目录树来实现最小[[Permissions|权限]]原则，无需 root [[Permissions|权限]]即可[[Configuration|配置]]。
2. **在 [[Codex CLI|Codex]] 中的角色**：[[Codex沙箱系统]] 在 Linux 平台上使用 Landlock + [[seccomp]] 组合实现双层隔离——Landlock 管文件系统边界，[[seccomp]] 管系统调用白名单。
3. **对比传统方案**：相比 [[seccomp]]（需要 root 或 cap_sys_admin），Landlock 可由普通进程自行启用，更适合 CLI 工具场景。

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — 沙箱执行层章节
- [[raw/articles/ai-tools/codex/03_codex_sandbox_system.md]] — 第 2.2 节：Landlock 作为第一层文件系统沙箱

## 相关

- [[Codex沙箱系统]] — 使用 Landlock 作为 Linux 平台文件系统隔离方案
- [[seccomp]] — 与 Landlock 配合使用的系统调用过滤机制
