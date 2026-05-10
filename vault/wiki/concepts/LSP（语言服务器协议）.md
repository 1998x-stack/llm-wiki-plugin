---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["Language Server Protocol", "语言服务器协议", "LSP 3.17"]
relates_to:
  - target: "[[Semantic Tokens]]"
    type: extends
    confidence: 0.9
  - target: "LSIF"
    type: extends
    confidence: 0.85
  - target: "[[JSON-RPC]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# LSP（语言服务器协议）

## 概述
Language Server Protocol 是 Microsoft 制定的开放协议，通过 JSON-RPC 2.0 在编辑器与独立语言[[服务]]进程之间通信，实现代码补全、跳转定义、诊断等 IDE 功能的一次实现、多编辑器复用。

## 关键内容

1. **历史演进**：2016 年 Microsoft 正式发布 LSP 1.0，与 Red Hat/Codenvy 联合推出。历经 3.0（[[CodeAct]]ion）、3.16（Semantic Tokens、Call Hierarchy）、3.17（Type Hierarchy、Inlay Hints、Notebooks）等版本，当前稳定版为 3.17.0（2023-05）。

2. **核心架构**：编辑器（LSP Client）通过 stdio/TCP socket/pipe/WebSocket 与独立进程的语言[[服务]]器（Language Server）通信。消息分为 Request（需回复）、Response（结果/错误）、Notification（单向无需回复）三种类型。

3. **初始化握手**：Client 发送 `initialize`（携带 capabilities）→ Server 回复 `initializeResult` → Client 发送 `initialized` notification → 进入正常工作阶段 → `shutdown` → `exit`。

4. **能力[[矩阵]]**：涵盖文本同步（didOpen/didChange/didSave/didClose）、语言特性（completion/hover/definition/references/codeAction/rename/semanticTokens/inlayHint 等 20+ 种）、工作空间特性（workspace symbol/executeCommand/applyEdit 等）。

5. **Semantic Tokens（3.16+）**：提供超越 TextMate 语法的精确着色。采用 Delta 编码格式 `[deltaLine, deltaStartChar, length, tokenType, tokenModifiers]`，5 个整数一组，支持增量更新。

6. **LSIF（[[LSIF（语言服务器索引格式）|Language Server Index Format]]）**：LSP 的"离线版本"，用于代码搜索和代码导航（[[GitHub]]、Sourcegraph 使用）。将语言[[服务]]器的分析结果序列化为图结构（vertex:document → contains → vertex:range → resultSet）。

7. **主流语言[[服务]]器**：[[gopls]]（Go）、[[hls（Haskell Language Server）]]（Haskell）、[[lua-language-server]]（Lua）、[[vtsls]]（[[TypeScript]]）、[[rust-analyzer]]（Rust）、[[pylsp]]（[[Python]]）、[[clangd]]（C/C++）、intelephense（PHP）、solargraph（Ruby）等。

8. **[[ACP 编辑器集成|编辑器集成]]**：Neovim（nvim-lspconfig）、[[VS Code]]（LanguageClient）、Emacs（eglot/lsp-mode）、Helix（languages.toml）均支持 LSP 客户端。

9. **调试工具**：`lsp-devtools`（record/tui）、Neovim `vim.lsp.set_log_level("debug")`、netcat 手动发送 JSON-RPC 请求。

10. **性能优化**：增量同步（Incremental vs Full）、防抖（100~500ms）、部分结果（$/progress 流式返回）、后台工作区索引、取消请求（$/cancelRequest）、AST 缓存按文件 hash 失效。

## 来源
- [[00_lsp_overview]] — LSP 语言服务器协议总览与架构调研

## 相关
- [[Semantic Tokens]] — extends
- LSIF — extends
- [[JSON-RPC]] — depends_on
