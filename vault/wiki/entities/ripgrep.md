---
type: entity
entity_type: tool
title: "ripgrep"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, Rust, 搜索, 开发工具, 工具与框架]
aliases:
  - rg
  - ripgrep
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
  - target: "fd"
    type: compares_to
    confidence: 0.9
  - target: "jq"
    type: compares_to
    confidence: 0.8
  - target: "[[GrepTool]]"
    type: implements
    confidence: 0.8
  - target: "[[Tool Ecosystem]]"
    type: part_of
    confidence: 0.7
supersedes: null
---

# ripgrep

## 概述

ripgrep（简称 `rg`）是一个用 Rust 编写的高性能递归搜索工具，是 `grep` 的现代替代品。默认感知 `.gitignore`，支持 Unicode，搜索速度比传统 grep 快 10-100 倍。

## 关键内容

1. **性能优势**：多线程并行搜索 + SIMD 优化，处理含 `node_modules` 的大型 monorepo 时，同等任务从 45s 降至 0.4s（约 100 倍提升）。
2. **Git 感知**：默认读取 `.gitignore` 和 `.rgignore`，自动跳过忽略目录，无需额外参数；`-l` 只输出文件名，`--json` 支持管道结构化处理。
3. **AI Agent 价值**：Agent 代码库搜索首选工具——Git 感知避免无关[[Context Window Pollution|上下文污染]]，`--json` 输出可直接 pipe 给 `jq` 进行程序化处理，行号精确引用减少幻觉。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
- fd — compares_to（文件定位搭档）
- jq — compares_to（JSON 输出管道）
