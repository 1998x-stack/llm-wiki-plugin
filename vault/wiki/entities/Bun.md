---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [build-tool, javascript-runtime, package-manager]
aliases: ["Bun", "Bun Runtime"]
relates_to:
  - target: "[[JavaScript]]"
    type: compatible_with
  - target: "[[TypeScript]]"
    type: compatible_with
  - target: "[[Claude Code]]"
    type: used_by
  - target: "[[Webpack]]"
    type: compares_to
  - target: "[[Vite]]"
    type: compares_to
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Bun

## 概述
Bun 是一个快速的 JavaScript/[[TypeScript]] 运行时、打包器和包管理器，旨在提供比传统工具如 Webpack 和 Vite 更快的构建速度。

## 关键内容
1. **性能优势**：Bun 以其显著的性能提升而闻名，相比 Webpack 和 Vite 等传统构建工具具有更快的构建速度。

2. **功能集合**：Bun 不仅仅是一个 JavaScript 运行时，它还集成了多个前端开发所需的功能：
   - JavaScript/[[TypeScript]] 运行时
   - 包管理器 (替代 npm/yarn/pnpm)
   - 打包器 (替代 Webpack/Vite)
   - 测试运行器

3. **在 [[Claude Code]] 中的应用**：[[Claude Code]] 选择 Bun 作为其构建工具，正是因为 Bun 比 Webpack/Vite 显著更快，有助于提高开发效率。

4. **技术基础**：Bun 是用 Zig 编写的，这使其能够在性能方面超越传统的 JavaScript 运行时。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[JavaScript]] — compatible_with
- [[TypeScript]] — compatible_with
- [[Claude Code]] — used_by
- [[Webpack]] — compares_to
- [[Vite]] — compares_to

## 指令