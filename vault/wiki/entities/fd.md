---
type: entity
entity_type: tool
title: "fd"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, Rust, 搜索, 开发工具, 工具与框架]
aliases:
  - fd-find
  - fdfind
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
  - target: "[[ripgrep]]"
    type: compares_to
    confidence: 0.9
supersedes: null
---

# fd

## 概述

fd 是 `find` 命令的现代替代品，用 Rust 编写。提供更简洁的语法、自动 `.gitignore` 感知和并行执行，支持模糊文件名匹配，Ubuntu 下二进制名为 `fdfind`。

## 关键内容

1. **简洁语法**：`fd -e py` 等价于 `find . -name "*.py" -type f`；无需 `-name` 标志，默认模糊匹配；自动跳过 `.gitignore` 中的目录，无需手动排除 `node_modules`。
2. **实用组合**：`fd -e py | xargs rg "TODO"` 与 [[ripgrep]] 组合；`-x` 参数对每个匹配文件执行命令；`--changed-within 1d` 查找近期修改文件；`-H` 包含隐藏文件。
3. **AI Agent 价值**：Agent `codebase_search` 操作首选——语法出错率更低，并行执行速度快，Git 感知确保不污染上下文。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
- [[ripgrep]] — compares_to（文件搜索 vs 内容搜索的黄金搭档）
