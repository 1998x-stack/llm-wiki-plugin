---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [memory-index, pointer-index, context-management, AI工程]
aliases: [MEMORY.md, Memory Index File, 记忆索引文件]
relates_to: 
  - target: "[[三层记忆架构]]"
    type: part_of
    confidence: 0.8
  - target: "[[Topic Files]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Self-Healing Memory]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Strict Write Discipline]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# MEMORY.md

## 概述
MEMORY.md 是 [[Claude Code]] [[三层记忆架构]]的第一层，作为整个记忆系统的轻量级指针索引，始终加载在上下文中。

## 关键内容

1. **核心作用**：
   - 作为整个记忆系统的**核心枢纽**，存储指向数据的指针而非实际数据
   - 每行约 150 个字符，保持极小的体积
   - 始终加载到上下文中（永久占用[[上下文窗口]]）

2. **结构特征**：
   - 内容是结构化的指针列表，指向更详细的 topic files
   - 包含主题的最后更新时间戳
   - 记录最近的决策和它们的来源位置

3. **设计优势**：
   - **全局可见**：Agent 在任何时候都知道有哪些主题可以检索
   - **[[渐进式披露（Progressive Disclosure）|按需加载]]**：只有真正需要的 topic 才会被读取
   - **极小开销**：整个索引文件只有几 KB

4. **典型内容**：
   - 项目记忆索引列表，指向 memory/topics/ 目录下的具体[[Topic Files|主题文件]]
   - 最近决策记录，包含时间戳和相关日志位置

## 来源
- [[raw/articles/ai-tools/claude-code/03_memory_architecture.md]] — Claude Code 源码泄露深度解析（三）

## 相关
- [[三层记忆架构]] — part_of
- [[Topic Files]] — relates_to
- [[Self-Healing Memory]] — relates_to
- [[Strict Write Discipline]] — relates_to
