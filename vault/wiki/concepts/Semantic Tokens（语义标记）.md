---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["Semantic Highlighting", "语义高亮", "语义标记"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: part_of
    confidence: 0.95
  - target: "[[TextMate 语法]]"
    type: supersedes
    confidence: 0.8
supersedes: null
---

# Semantic Tokens（语义标记）

## 概述
LSP 3.16 引入的语义标记机制，通过语言[[服务]]器分析代码语义而非仅依赖 TextMate 语法正则，为编辑器提供精确的语法高亮和语义分类信息。

## 关键内容

1. **Delta 编码格式**：[[服务]]端返回 5 个整数一组的数组 `[deltaLine, deltaStartChar, length, tokenType, tokenModifiers]`。deltaLine 和 deltaStartChar 相对于上一个 token 的位置，实现紧凑的增量编码。

2. **Token 类型**：包括 namespace、type、class、function、method、property、parameter、variable、keyword 等标准类型，由 legend 定义。

3. **Token 修饰符**：使用位掩码表示多个修饰符，如 declaration、definition、readonly、static、deprecated、abstract、async 等。

4. **优势**：相比 TextMate 语法（基于正则表达式的文本匹配），Semantic Tokens 能[[区分]]同名不同义的标识符（如局部变量 vs 全局变量、函数声明 vs 函数调用），提供更精确的着色。

5. **客户端支持**：Neovim、[[VS Code]]、Emacs 等主流编辑器均支持 Semantic Tokens 渲染。

## 来源
- [[00_lsp_overview]] — LSP 语言服务器协议总览与架构调研

## 相关
- [[LSP（语言服务器协议）]] — part_of
- [[TextMate 语法]] — supersedes
