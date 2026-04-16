---
type: entity
entity_type: tool
title: "just"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, Rust, 任务自动化, 开发工具, 工具与框架]
aliases:
  - justfile
  - just task runner
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
supersedes: null
---

# just

## 概述

just 是 `make` 的现代替代任务运行器，用 Rust 编写。不依赖文件时间戳，支持参数传递，`Justfile` 语法比 `Makefile` 更简洁直观，通过 `cargo install just` 安装。

## 关键内容

1. **核心优势**：解决 `make` 依赖文件修改时间戳的缺陷——`just` 的 recipe 始终执行，不会因"文件已是最新"跳过；支持参数传递（`just build v1.2.3`），语法无 Makefile 的 tab 限制。
2. **Justfile 语法**：`recipe_name *args: uv run pytest {{args}} -v` 支持可变参数；`build tag="latest": docker build -t myapp:{{tag}} .` 支持默认值；`just --list` 自文档化所有任务。
3. **AI Agent 价值**：统一的任务入口（测试/构建/部署/迁移）让 Agent 无需猜测命令格式，`just --list` 提供可发现的操作空间，降低 Agent 编排错误率。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
