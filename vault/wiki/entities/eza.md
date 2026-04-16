---
type: entity
entity_type: tool
title: "eza"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, Rust, 文件管理, 开发工具, 工具与框架]
aliases:
  - exa
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
supersedes: null
---

# eza

## 概述

eza 是 `ls` 命令的现代替代品（exa 的维护分支），用 Rust 编写。支持 Git 状态标注、文件图标、树形视图，可完全替代 `tree` 命令，通过 `cargo install eza` 安装。

## 关键内容

1. **Git 感知**：`eza -la --git` 在每个文件旁显示 Git 状态符号（N=新文件/M=已修改/D=已删除/A=已暂存/I=被忽略），一眼掌握工作区状态。
2. **树形视图**：`eza --tree --level=3 --git-ignore` 替代 `tree` 命令，支持深度控制和 `.gitignore` 感知，避免展示无关的 `node_modules`。
3. **AI Agent 价值**：`eza --tree` 生成的层次结构帮助 Agent 快速理解项目目录布局，Git 状态列让 Agent 无需运行 `git status` 即可判断文件变更。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
