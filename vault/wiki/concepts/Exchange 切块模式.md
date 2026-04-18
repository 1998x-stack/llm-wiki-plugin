---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [chunking, conversation, semantic-integrity, mempalace]
aliases: ["Exchange Chunking", "问答对切块", "Exchange 模式"]
relates_to:
  - target: "[[挖掘管道]]"
    type: part_of
  - target: "[[MemPalace]]"
    type: part_of
  - target: "[[原文逐字存储]]"
    type: extends
supersedes: null
---

# Exchange 切块模式

## 概述
[[MemPalace]] Convos 模式专用的对话切块策略，以"用户提问 + AI 回答"问答对为最小单元，确保语义完整性。

## 关键内容
- **核心原则**：每个 chunk 必须包含完整的一问一答，绝不打断问题和答案之间的语义关联
- **实现方式**：按 `>` 标记分割文本（`>` 标记代表用户输入），每个 exchange 是一个独立 chunk
- **与 Projects 模式的区别**：Projects 模式按字符数切块（800 字符 + 100 重叠），Exchange 模式按语义单元切块
- **兜底机制**：如果 `>` 标记少于 3 个（不像对话格式），退回段落切块模式
- **语义完整性保障**：一个 chunk 里永远包含完整的问答对，检索时不会只返回问题或只返回答案
- **代码实现**：`chunks = split_by_exchanges(text)` — 按 `>` 分割，每个 exchange 作为独立 chunk

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_05_mining_pipelines.md]] — MemPalace 深度解析第五篇：三种挖掘管道

## 相关
- [[挖掘管道]] — part_of
- [[MemPalace]] — part_of
- [[原文逐字存储]] — extends
