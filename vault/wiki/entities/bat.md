---
type: entity
entity_type: tool
title: "bat"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, Rust, 文件查看, 开发工具, 工具与框架]
aliases:
  - batcat
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
  - target: "[[ripgrep]]"
    type: compares_to
    confidence: 0.8
supersedes: null
---

# bat

## 概述

bat 是 `cat` 命令的现代替代品，用 Rust 编写。集成语法高亮、Git diff 标注、行号显示和自动分页，Ubuntu 下二进制名为 `batcat`，可设 alias。

## 关键内容

1. **核心功能**：语法高亮（支持 100+ 语言）+ Git 变更行标注（显示哪些行被新增/修改）+ 自动分页（类 `less`）；`--paging=never` 适合管道使用。
2. **集成场景**：`rg "error" --json | bat --language json`（彩色 JSON 输出）；`git show HEAD:file.py | bat -l py`（历史版本带高亮）；可配置为 `MANPAGER` 使 man 页带语法高亮。
3. **AI Agent 价值**：行号显示让 Agent 引用代码位置更精确；Git diff 标注帮助 Agent 直观理解文件变更状态，减少错误引用。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
- [[ripgrep]] — compares_to（内容查看 vs 内容搜索）
