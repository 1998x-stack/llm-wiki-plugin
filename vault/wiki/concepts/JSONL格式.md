---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [数据格式, 工程实践, 日志, AI工程]
aliases: [JSON Lines, JSONL, NDJSON]
relates_to:
  - target: "[[Codex会话管理器]]"
    type: uses
    confidence: 0.95
  - target: "[[Codex CLI]]"
    type: uses
    confidence: 0.8
  - target: "[[上下文窗口]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# JSONL 格式

## 概述
JSONL（JSON Lines / NDJSON）是一种逐行存储 JSON 对象的文本格式，每行一个完整的 JSON 记录，支持流式追加和崩溃安全写入。

## 关键内容

1. **格式定义**：每行一个独立的 JSON 对象，行与行之间用换行符分隔。不同于 JSON 数组，不需要首尾括号包裹，可无限追加。

2. **崩溃安全特性**：写入中断时只会丢失当前行，之前所有记录保持完整。这一特性使其成为日志、Transcript、事件流等场景的首选格式。

3. **流式处理优势**：不需要重写整个文件即可追加新记录；可用 `jq` 等工具直接管道分析，如 `cat transcript.jsonl | jq '.role'`。

4. **在 [[Codex会话管理器|Codex Session Manager]] 中的应用**：`transcript.jsonl` 存储完整对话记录，每行包含 `role`、`content`、`ts` 等字段，记录 user/assistant/tool 三类消息。

5. **与 JSON 数组的对比**：JSON 数组需一次性读写整个文件，崩溃时可能损坏全部数据；JSONL 逐行独立，适合长时间运行的 Agent [[会话日志]]。

## 来源
- [[raw/articles/ai-tools/codex/05_codex_session_manager.md]] — Codex CLI 深度解析 Vol.5：Session Manager

## 相关
- [[Codex会话管理器]] — uses
- [[Codex CLI]] — uses
- [[上下文窗口]] — relates_to
