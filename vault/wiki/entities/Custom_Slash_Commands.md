---
type: entity
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-tools, legacy-feature, AI工程]
aliases: ["Custom Slash Commands", "Slash Commands"]
relates_to: []
supersedes: null
---

# Custom Slash Commands

## 概述
[[Custom Slash Commands]] 是 [[Claude Code]] 最初提供的可扩展机制，允许开发者通过 Markdown 文件创建自定义命令。

## 关键内容

1. **基本功能**：
   - 开发者在 `.claude/commands/` 目录下放置 Markdown 文件
   - 通过 `/command-name` 触发对应的 Prompt 模板
   - 简单的 Prompt 模板机制

2. **演进历程**：
   - 被 [[Agent Skills]] 规范完全替代
   - [[Agent Skills]] 提供更丰富的功能，包括说明文档、辅助脚本、参考资料等完整目录结构
   - 仍被并入 [[Skills]] 系统

## 来源
- [[01_claude_code_skill_system_overview.md]] — 发展背景
- [[]] —

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — supersedes
- [[SKILL.md]] — predecessor