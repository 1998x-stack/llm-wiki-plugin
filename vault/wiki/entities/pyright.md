---
type: entity
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["pyright", "Pyright", "Microsoft Python Language Server"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "[[pylsp]]"
    type: compares_to
    confidence: 0.8
supersedes: null
entity_type: tool
---

# pyright

## 概述
Microsoft 出品的 Python 静态类型检查器和 LSP 服务器，提供严格的类型检查能力，是 Pylance（VS Code 专属）的开源基础。

## 关键内容

1. **定位**：专注于静态类型检查，支持 Python 3.7+ 的类型注解，包括 PEP 484、PEP 526、PEP 544 等。

2. **与 Pylance 的关系**：Pylance 是 VS Code 专属的 Python 语言服务器，基于 pyright 构建（闭源），添加了额外的 IntelliCode 等功能。

3. **basedpyright**：pyright 的增强分支，提供更多诊断功能和配置选项。

4. **与 [[pylsp]] 对比**：pyright 侧重类型检查，[[pylsp]] 侧重插件化和多功能（补全、重构、格式化等）。

## 来源
- [[01_python_lsp]] — Python LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- [[pylsp]] — compares_to
