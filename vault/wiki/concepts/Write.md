---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [write-operation, code-modification, file-creation]
aliases: ["Write", "Write操作", "写操作"]
relates_to: 
  - target: "[[Claude Code]]"
    type: relates_to
  - target: "[[Claude Code四大能力基元]]"
    type: part_of
supersedes: null
---

# Write

## 概述
Write是[[Claude Code四大能力基元]]之一，代表修改和创建文件的能力，通过Edit、Write/Replace、Create等工具实现代码和文件的写入操作。

## 关键内容
1. **功能范围**：包括编辑文件(Edit)、写入/替换内容(Write/Replace)、创建新文件(Create)等多种写入操作。

2. **代码修改**：支持对现有代码进行补丁(Patch)操作，可以精确修改特定位置的内容。

3. **全文替换**：支持对整个文件或大段内容进行替换，适用于[[重构]]等场景。

4. **新文件创建**：能够根据需要创建全新的文件，用于添加新的功能模块。

5. **在[[Claude Code]]中的角色**：作为四大基础能力之一，Write使AI能够实际修改代码库，实现功能添加、修复bug等操作。

## 来源
- [[01_system_overview.md]] — 四大能力基元部分

## 相关
- [[Claude Code]] — relates_to
- [[Claude Code四大能力基元]] — part_of
- [[Code Modification]] — relates_to