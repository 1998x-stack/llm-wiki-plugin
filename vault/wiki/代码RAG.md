---
type: concept
status: active
confidence: 0.5
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, 方法论]
aliases: [Code RAG, 代码场景RAG]
relates_to:
  - 检索增强生成
  - AST抽象语法树
  - Claude Code
supersedes: null
---

# 代码RAG

## 概述
将RAG技术应用于代码场景的检索增强方案。实操表明纯代码做RAG效果远不如字符串匹配，有效的代码RAG必须配套解释文档，AST抽象语法树是未来核心方向。

## 关键内容
1. **纯代码RAG的失败原因**：代码语义不完整，变量名和函数名只能传递有限信息；代码间存在import依赖和跨文件调用，容易出现语义断裂；纯向量化检索效果甚至不如grep等基础字符串匹配工具。
2. **有效方案：1:1解释文档**：仓库中每个Python文件对应一个Markdown文档，讲清核心作用、用到的函数、依赖关系、输入输出。基于文档做RAG，检索效果有质的提升。
3. **AST树是未来方向**：AST抽象语法树能将代码文件拆解成清晰的结构树——项目有哪些文件、文件里有哪些类、类里有哪些方法、方法间调用关系、函数起止行数。基于AST树可为Agent做精准代码定位和依赖拓展，本质是为代码仓库搭建专属"知识图谱"。
4. **Claude Code的实践**：内部优先用命令行检索代码，AST方案已在落地中，未来会成为代码RAG的标准配置。

## 来源
- [[raw/articles/essays/thinking-series/011-算法面试]] — 一线工程师实操结论

## 相关
- [[检索增强生成]] — part_of
- [[AST抽象语法树]] — uses
- [[Claude Code]] — relates_to
- [[知识图谱]] — compares_to
