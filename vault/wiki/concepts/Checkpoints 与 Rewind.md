---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Checkpoints", "Rewind", "对话快照", "Branch Point"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.8
  - target: "[[上下文压缩]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Checkpoints 与 Rewind

## 概述
Checkpoints 保存 [[Claude Code]] 对话状态快照（消息、文件修改、工具使用历史、会话上下文），让用户可以回退到之前的时间点，安全地试验和探索多种方案。

## 关键内容

1. **核心概念**：
   - **Checkpoint**：保存消息、文件和上下文的对话快照
   - **Rewind**：回到之前的 checkpoint，并丢弃之后的更改
   - **Branch Point**：从同一个 checkpoint 出发，探索多个方案

2. **访问方式**：
   - 键盘快捷键：按两次 `Esc`（`Esc` + `Esc`）打开 checkpoint 界面
   - Slash Command：`/rewind`（别名：`/checkpoint`）

3. **Rewind 选项**：
   - **恢复代码和对话**：文件和消息都恢复到那个 checkpoint
   - **恢复对话**：只回退消息，保留当前代码不变
   - **恢复代码**：只回退文件修改，保留完整对话历史
   - **从这里开始总结**：把从这里往后的[[上下文压缩（Context Compaction）|对话压缩]]成 AI 生成的摘要，而非直接丢弃
   - **算了**：取消并返回当前状态

4. **自动 Checkpoints**：[[Claude Code]] 会自动在关键操作前后创建 checkpoints，如文件写入、命令执行等，确保用户可以随时回退。

## 来源
- [[08-checkpoints/README.md]] — Claude HowTo Checkpoints 与 Rewind 指南

## 相关
- [[斜杠命令（Slash Commands）]] — uses
- [[上下文压缩]] — relates_to
