---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [read-operation, file-access, code-understanding]
aliases: ["Read", "Read操作", "读操作"]
relates_to: 
  - target: "[[Claude Code]]"
    type: relates_to
  - target: "[[Claude Code四大能力基元]]"
    type: part_of
supersedes: null
---

# Read

## 概述
Read是[[Claude Code四大能力基元]]之一，代表读取和理解代码库的能力，通过View、LS、Glob、[[GrepTool]]等工具实现对代码和文件系统的访问。

## 关键内容
1. **功能范围**：包括查看文件内容(View)、列出目录(LS)、查找文件(Glob)、搜索内容([[GrepTool]])等基本文件系统操作。

2. **代码理解**：通过读取文件内容和搜索特定模式，使AI能够理解现有代码库的结构和内容。

3. **上下文获取**：为AI提供必要的上下文信息，以便做出正确的编程决策。

4. **在[[Claude Code]]中的角色**：作为四大基础能力之一，Read为AI提供了感知代码环境的能力，是其他操作（[[Write]]、[[Execute]]、[[Connect]]）的前提。

## 来源
- [[01_system_overview.md]] — 四大能力基元部分

## 相关
- [[Claude Code]] — relates_to
- [[Claude Code四大能力基元]] — part_of
- [[File Access]] — relates_to