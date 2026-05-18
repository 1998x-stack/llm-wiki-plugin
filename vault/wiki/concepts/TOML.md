---
type: concept
status: active
confidence: 0.8
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [数据格式, 配置管理, 工具, 机器学习]
aliases: [TOML, Tom's Obvious Minimal Language]
relates_to:
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.95
  - target: "[[Codex配置系统]]"
    type: uses
    confidence: 0.85
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# TOML

一种极简的[[Configuration|配置]]文件数据格式，设计目标是"人类可读、机器易解析"，在 [[Codex CLI]] 中作为 [[ExecPolicy]] 规则文件和主[[Configuration|配置]]的标准格式。

## 关键内容

1. **在 [[ExecPolicy]] 中的应用**：规则文件以 `.rules` 扩展名存储，使用 TOML 数组表（`[[rule]]`）定义多条规则。每条规则包含 `name`、`prefix`、`decision`、`justification` 以及可选的 `match`/`not_match` [[单元测试]]用例。

2. **嵌套数组表示"或"逻辑**：`prefix = ["git", ["log", "status", "diff"]]` 中，内层数组表示子命令的可选集合，外层表示命令序列。这种嵌套结构是 TOML 原生支持的。

3. **相比 YAML/JSON 的优势**：
   - 比 JSON 更易读（无花括号、无引号冗余）
   - 比 YAML 更严格（无缩进歧义、无类型推断陷阱）
   - 原生支持注释，适合策略文件的 `justification` 字段

4. **在 [[Codex CLI|Codex]] [[Configuration|配置]]体系中的统一使用**：从 `config.toml` 到 `.rules` 文件，全链路 TOML，降低认知负担。

## 来源

- [[raw/articles/ai-tools/codex/04_codex_execpolicy.md]] — 第 2 节：规则语法详解（TOML 示例）

## 相关

- [[ExecPolicy]] — uses，ExecPolicy 规则文件的标准格式
- [[Codex配置系统]] — uses，主配置文件格式
- [[Codex CLI]] — uses，全链路配置格式
