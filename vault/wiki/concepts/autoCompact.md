---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI工具, 上下文管理, 会话管理, 性能优化]
aliases: ["autoCompact", "AutoCompact Mechanism", "Context Compression"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Context Management]]"
    type: implements
  - target: "[[Prompt Cache]]"
    type: complements
supersedes: null
---

# autoCompact

## 概述
[[Claude Code]]中的[[上下文压缩]]机制，当对话历史过长接近模型[[上下文窗口]]上限时，自动触发将对话历史压缩为结构化摘要的功能。

## 关键内容
1. **触发机制**：当检测到当前token使用量接近阈值时，系统会触发auto[[上下文压缩（Context Compaction）|Compact]]机制。

2. **工作流程**：
   - 检测当前token使用量接近阈值
   - 启动一个独立的[[Claude_Code|Claude]]会话
   - 请求模型将当前对话历史压缩为结构化摘要
   - 用摘要替换[[Transcripts|历史记录]]，继续会话

3. **容错机制**：为解决压缩失败导致的无限循环问题，系统[[Settings|设置]]了MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES=3的限制，防止API滥用。根据注释记录，在BQ 2026-03-10事件中，1,279个会话出现了50+次连续失败（最多3,272次），每天全球浪费约25万次API调用，该修复方案每天节省了大量API调用。

4. **工程价值**：auto[[上下文压缩（Context Compaction）|Compact]]机制体现了数据驱动工程的价值，通过真实线上数据指导技术决策，优化资源使用。

## 来源
- [[Claude Code 源码泄露深度解析（二）：核心 Agent 引擎与 40+ 工具系统]] — 全文

## 相关
- [[Claude Code]] — part_of
- [[Context Management]] — implements
- [[Prompt Cache]] — complements