---
type: entity
entity_type: tool
title: "jq"
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [工具, CLI, JSON, 数据处理, 开发工具, 工具与框架]
aliases:
  - jq JSON processor
relates_to:
  - target: "[[现代 CLI 工具全景]]"
    type: part_of
    confidence: 1.0
  - target: "[[ripgrep]]"
    type: compares_to
    confidence: 0.7
supersedes: null
---

# jq

## 概述

jq 是命令行 JSON 处理器，被称为"JSON 瑞士军刀"。支持过滤、投影、聚合和结构转换，是 CLI 数据管道的核心组件，通过 `brew install jq` 或包管理器安装。

## 关键内容

1. **核心操作**：`.` 格式化输出；`.users[] | select(.age > 30)` 过滤；`.[] | {name, email}` 投影；`map(.price) | add` 聚合计算，语法简洁但功能完整。
2. **管道集成**：与 `curl`、`rg --json`、`yq` 等工具无缝组合——`rg "error" --json | jq '.data.text'` 提取 [[ripgrep]] JSON 输出中的文本内容，实现结构化数据流处理。
3. **AI Agent 价值**：API 响应解析、配置文件提取、日志分析的标配工具；与 `rg --json` 组合使 Agent 能程序化处理代码搜索结果，避免文本解析错误。

## 来源

- [[raw/articles/programming/cli-tools/modern-cli-tools.md]] — 现代 CLI 工具全景指南

## 相关

- [[现代 CLI 工具全景]] — part_of
- [[ripgrep]] — compares_to（常与 rg --json 组合使用）
