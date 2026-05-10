---
type: entity
entity_type: tool
status: active
confidence: 0.6
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude-code, slash-command, git]
aliases: ["commit slash command", "Claude Code commit command"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
    confidence: 0.6
  - target: "[[Git Commit]]"
    type: implements
    confidence: 0.7
  - target: "[[Conventional Commits]]"
    type: uses
    confidence: 0.7
supersedes: null
---

# commit

## 概述
[[Claude Code]]中的commit[[Slash Commands|斜杠命令]]，用于创建带上下文的Git提交。

## 关键内容

1. **功能特性**：
   - 自动获取当前git状态
   - 显示当前git diff
   - 展示当前分支信息
   - 列出最近的提交记录

2. **使用方式**：
   - 可接受提交消息作为参数
   - 如未提供参数，则根据变更自动生成符合[[Conventional Commits|约定式提交]]格式的消息
   - 支持多种提交类型：feat、fix、docs、refactor、test、chore等

3. **允许的工具**：
   - `git add`
   - `git status`
   - `git commit`
   - `git diff`

## 来源
- [[]] — 

## 相关
- [[Claude Code]] — part_of
- [[Git Commit]] — implements
- [[Conventional Commits]] — uses