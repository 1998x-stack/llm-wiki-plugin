---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["pylsp", "python-lsp-server", "Python Language Server"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "[[pyright]]"
    type: compares_to
    confidence: 0.8
supersedes: null
entity_type: tool
---

# pylsp（Python LSP Server）

## 概述
社区维护的 Python 语言服务器，2021 年从 Palantir 停止维护的 python-language-server (pyls) fork 而来，采用插件化架构，支持丰富的 Python 开发功能。

## 关键内容

1. **历史**：2017 年 Palantir 发布 pyls，2021-01 停止维护，2021-03 社区 fork 为 python-lsp-server (pylsp)，持续活跃维护至 2024 年 v1.11.x。

2. **插件生态**：支持 rope（重构）、flake8、autopep8、yapf、pylint、mccabe、pyflakes、ruff 等插件，通过 `pip install "python-lsp-server[all]"` 安装全功能。

3. **功能覆盖**：代码补全、跳转定义、悬停信息、签名帮助、代码动作、重命名、格式化、诊断等完整 LSP 能力。

4. **与 [[pyright]] 对比**：pylsp 侧重多功能和插件化，[[pyright]] 侧重严格的静态类型检查。

## 来源
- [[01_python_lsp]] — Python LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[pyright]] — compares_to
