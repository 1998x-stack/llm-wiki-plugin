---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架", C++编程]
aliases: ["clangd", "Clang Language Server", "C/C++ 语言服务器"]
relates_to:
  - target: "[[LSP（语言服务器协议）]]"
    type: implements
    confidence: 0.95
  - target: "ccls"
    type: compares_to
    confidence: 0.8
supersedes: null
entity_type: tool
---

# clangd

## 概述
LLVM/Clang 官方的 C/C++/ObjC/CUDA 语言[[服务]]器，基于 Clang 的 LibTooling 构建，是 C/C++ 生态中最全功能的 LSP 实现。

## 关键内容

1. **历史**：2018 年 7.0 首个正式版，2020 年 10.0 [[Semantic Tokens（语义标记）|语义高亮]]，2023 年 16.0 C++23 支持，2024 年 19.0 当前稳定版。

2. **架构**：LSP Layer（JSON-RPC 处理）→ ClangdServer（协调层）→ TUScheduler（翻译单元调度，异步优先级）→ FileIndex（后台全 workspace 索引，含 MemIndex 和 DiskIndex）→ GlobalCompilationDatabase（compile_commands.json）。

3. **核心设计**：TUScheduler 按文件异步调度 AST [[Worker Agent|Worker]] 和 Preamble [[Worker Agent|Worker]]；FileIndex 维护内存和磁盘双层索引；通过 compile_commands.json 获取编译[[Configuration|配置]]。

4. **与 ccls 对比**：clangd 功能最全、官方维护；ccls 是高性能替代方案，在 C++17 支持上表现优秀。

## 来源
- [[05_cpp_lsp]] — C/C++ LSP 工具完整调研

## 相关
- [[LSP（语言服务器协议）]] — implements
- ccls — compares_to
