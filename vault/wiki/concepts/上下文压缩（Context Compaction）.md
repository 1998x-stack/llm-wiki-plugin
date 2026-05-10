---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Context Compaction", "对话压缩", "Compact"]
relates_to:
  - target: "[[上下文窗口]]"
    type: depends_on
    confidence: 0.9
  - target: "[[Checkpoints 与 Rewind]]"
    type: relates_to
    confidence: 0.7
  - target: "[[渐进式披露（Progressive Disclosure）]]"
    type: compares_to
    confidence: 0.75
supersedes: null
---

# 上下文压缩（Context Compaction）

## 概述
[[Claude Code]] 的[[上下文压缩]]功能（`/compact` 命令）将长对话压缩成精简摘要，释放[[上下文窗口]]空间，同时保留关键信息和任务连续性。

## 关键内容

1. **工作原理**：`/compact [instructions]` 命令将当前对话历史压缩成 AI 生成的摘要，可附带聚焦指令告诉 [[Claude_Code|Claude]] 压缩时应保留哪些关键信息。压缩后，旧消息被替换为摘要，释放 token 空间。

2. **与 [[Checkpoints 与 Rewind|Rewind]] 的关系**：[[Checkpoints 与 Rewind|Rewind]] 的"从这里开始总结"选项也会执行类似压缩，但 `/compact` 是主动触发的独立操作，更灵活。

3. **使用场景**：
   - 长对话接近[[上下文窗口]]限制时
   - 完成一个子任务后，压缩历史开始新任务
   - 需要减少 token 消耗时

4. **与渐进式披露的对比**：渐进式披露是"预防性"策略（不让不需要的信息进入上下文），[[上下文压缩]]是"补救性"策略（当上下文过长时压缩旧内容）。

## 来源
- [[01-slash-commands/README.md]] — Claude HowTo 斜杠命令参考
- [[08-checkpoints/README.md]] — Claude HowTo Checkpoints 指南

## 相关
- [[上下文窗口]] — depends_on
- [[Checkpoints 与 Rewind]] — relates_to
- [[渐进式披露（Progressive Disclosure）]] — compares_to
