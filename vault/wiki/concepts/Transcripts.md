---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [history-records, session-logs, memory-system, 推荐系统]
aliases: [Transcripts, 会话记录, 历史记录]
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
  - target: "[[MEMORY.md]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Transcripts

## 概述
Transcripts 是 [[Claude Code]] [[三层记忆架构]]的第三层，用于存储会话历史原始记录，采用只 Grep 不全读的访问策略。

## 关键内容

1. **存储特征**：
   - 存储会话历史的原始记录
   - 位于 memory/transcripts/ 目录下
   - 保留完整的交互历史以便追溯

2. **访问策略**：
   - 从不被完整读回上下文，避免占用过多[[上下文窗口]]
   - 使用 grep 命令查找特定标识符或关键词
   - 定位到相关行并读取前后的有限上下文
   - 将提取的片段而非完整记录放入上下文

3. **设计优势**：
   - 保留完整历史记录便于追溯
   - 避免历史记录占满[[上下文窗口]]
   - 提供精确匹配而非模糊检索
   - 保持历史记录的完整性

4. **解决的核心矛盾**：
   - 需要保留完整历史（便于追溯）
   - 但又不能让历史占满上下文

## 来源
- [[raw/articles/ai-tools/claude-code/03_memory_architecture.md]] — Claude Code 源码泄露深度解析（三）

## 相关
- [[三层记忆架构]] — part_of
- [[Topic Files]] — relates_to
- [[Self-Healing Memory]] — relates_to
- [[MEMORY.md]] — relates_to
