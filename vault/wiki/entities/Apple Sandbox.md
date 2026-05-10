---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-19
source_count: 1
tags: ["安全", "macOS", "沙箱"]
aliases: ["Apple Sandbox", "Seatbelt", "sandbox-exec"]
relates_to:
  - target: "[[沙箱系统]]"
    type: part_of
  - target: "[[Codex CLI]]"
    type: uses
supersedes: null
---

# Apple Sandbox

## 概述
Apple 原生 macOS 沙箱机制（代号 Seatbelt），基于 Scheme 描述语言的访问控制策略，通过 `sandbox-exec` 工具对进程施加文件系统、网络和进程级别的访问限制。

## 关键内容

1. **策略语言**：使用 Scheme 语法描述访问控制规则，支持 `(deny default)` [[Settings|设置]]默认拒绝策略，`(allow file-read*)` 允许[[Read|读操作]]，`(allow file-write* (subpath "..."))` 限定写路径，`(deny network-outbound)` 禁止网络访问。

2. **动态策略生成**：[[Codex CLI]] 在运行时根据当前 workspace 路径动态生成 Seatbelt profile，无需手动[[Configuration|配置]]策略文件。

3. **调试支持**：`--log-denials` 模式可打印所有被拦截的系统调用，便于调试沙箱[[Configuration|配置]]错误。

4. **零额外依赖**：作为 Apple 原生机制，无需安装额外软件或内核模块，macOS 系统自带支持。

5. **核心原语**：基于 `sandbox-exec` 和 entitlements 实现，实现位置在 `codex-rs/core/src/platform/macos/`。

## 来源
- [[raw/articles/ai-tools/codex/03_codex_sandbox_system.md]] — 第 2.1 节

## 相关
- [[沙箱系统]] — part_of
- [[Codex CLI]] — uses
- [[Landlock]] — compares_to
- [[seccomp]] — compares_to
