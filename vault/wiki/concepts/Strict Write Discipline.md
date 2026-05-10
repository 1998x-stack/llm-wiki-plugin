---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [write-discipline, memory-integrity, consistency]
aliases: [Strict Write Discipline, 严格写入纪律, 两阶段提交模式]
relates_to: 
  - target: "[[三层记忆架构]]"
    type: part_of
    confidence: 0.8
  - target: "[[MEMORY.md]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Self-Healing Memory]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Topic Files]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Strict Write Discipline

## 概述
Strict [[Write]] Discipline（严格写入纪律）是 [[Claude Code]] [[三层记忆架构]]中最重要的设计约束之一，确保记忆系统的一致性和防止记忆污染。

## 关键内容

1. **核心规则**：
   - Agent 只有在文件写入成功之后，才能更新 [[MEMORY.md]] 索引
   - 实施两阶段提交模式：先写入 topic file，后更新 [[MEMORY.md]] 索引
   - 如果写入失败，则不更新索引，也不记录失败

2. **流程控制**：
   ```
   尝试写入 topic file
       │
       ├── 成功 ──→ 更新 MEMORY.md 索引 ✓
       │
       └── 失败 ──→ 不更新索引，不记录失败 ✗
   ```

3. **重要意义**：
   - 防止 [[MEMORY.md]] 记录指向不存在文件的指针
   - 避免因读取不存在文件导致的失败
   - 防止模型用自身"记忆"填充空白，产生幻觉
   - 防止错误信息污染整个记忆系统

4. **设计原理**：
   - 借鉴数据库事务的两阶段提交思想
   - 体现了"宁可不记，不能记错"的原则
   - 对于 LLM 系统，错误的记忆比没有记忆更危险

## 来源
- [[raw/articles/ai-tools/claude-code/03_memory_architecture.md]] — Claude Code 源码泄露深度解析（三）

## 相关
- [[三层记忆架构]] — part_of
- [[MEMORY.md]] — relates_to
- [[Self-Healing Memory]] — relates_to
- [[Topic Files]] — relates_to
