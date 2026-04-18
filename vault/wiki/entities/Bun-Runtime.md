---
type: entity
entity_type: tool
title: “Bun Runtime”
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [工具, JS运行时, 包管理器, 工具与框架]
aliases: [“Bun.js”, “Bun JS Runtime”, “Bun”]
relates_to:
  - target: “[[Claude-Mem]]”
    type: uses
    confidence: 0.9
  - target: “[[Node.js]]”
    type: compares_to
    confidence: 0.9
  - target: “[[SQLite]]”
    type: uses
    confidence: 0.8
  - target: “uv”
    type: compares_to
    confidence: 0.95
supersedes: null
---

# Bun Runtime

## 概述
Bun 是 JavaScript/[[TypeScript]] 生态的全能工具链（运行时 + 包管理器 + 打包器 + 测试框架），用 Zig 实现，由 Oven（Bun Inc.）开发，2022 年首发。定位为”Cargo for JS”，以极速替代 node+npm+jest+ts-node 整套工具链。

## 关键内容

1. **性能基准**：冷缓存包安装比 npm 快约 16x（3s vs 48s），Docker 多阶段构建无缓存约快 8-10x（6s vs 52s）。缓存命中时约快 12x。
2. **功能覆盖**：内置包管理器（兼容 npm registry）、[[TypeScript]] 原生执行（无需 tsc）、打包器（替代 esbuild/rollup）、测试框架（Jest 兼容）、[[SQLite]]（`bun:sqlite`）、Workspaces、热重载（`bun --hot`）。
3. **架构设计**：全局缓存 + 硬链接（类 pnpm）；二进制 lockfile `bun.lockb`；底层用 Zig + JavaScriptCore；Node.js API 兼容率约 95%+。
4. **适用场景**：新建 JS/TS 项目、对 CI 安装速度极度敏感、API 服务/工具库/全栈 Web 应用、AI Agent 工具链（[[Claude Code]] 等工具首选）。
5. **局限**：不管理 Node 版本（需配合 fnm/nvm）；Node.js 兼容性 95% 而非 100%；企业环境对工具链稳定性要求极高时建议观望。

## 来源
- [[raw/articles/ai-tools/claude-mem/blog_01_overview.md]] — Claude-Mem 项目选型
- [[raw/articles/programming/cli-tools/bun-vs-uv.md]] — Bun vs uv 跨语言深度对比

## 相关
- uv — compares_to（Python 生态对标工具）
- [[Node.js]] — compares_to
- [[SQLite]] — uses