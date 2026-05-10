---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, command-system, deprecated]
aliases: ["Custom Slash Commands", "Slash Commands"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Agent Skills]]"
    type: superseded_by
supersedes: null
---

# Custom Slash Commands

## 概述
[[Claude Code]]最初提供的可扩展机制，在`.claude/commands/`目录下放置Markdown文件，用`/command-name`触发对应Prompt模板。

## 关键内容

1. **实现方式**：
   - 在`.claude/commands/`目录下放置Markdown文件
   - 使用`/command-name`[[Slash Commands|斜杠命令]]触发对应的Prompt模板

2. **发展演进**：
   - 最初的可扩展机制
   - 2025年中期被[[Agent Skills]]规范全面替代
   - [[Agent Skills]]是其超集，提供了更完整的功能

3. **局限性**：
   - 仅限于单文件Prompt模板
   - 缺乏完整的目录结构支持
   - 不支持辅助脚本、参考资料等功能

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — superseded_by