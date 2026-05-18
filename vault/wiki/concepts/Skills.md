---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [claude, automation, ai-agent, skills, AI工程]
aliases: ["Skill", "技能", "Skills System", "技能系统"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[上下文管理系统]]"
    type: relates_to
  - target: "[[CLAUDE.md]]"
    type: relates_to
supersedes: null
---

# Skills

## 概述
Skills 是 [[Claude Code]] 中的自定义命令系统，允许用户定义可在会话中通过[[Slash Commands|斜杠命令]]调用的功能，现已取代旧式的自定义命令系统。Skills 还具有[[渐进式披露（Progressive Disclosure）|按需加载]]机制，只在需要时才加载完整的技能内容，保持上下文开销最小。

## 关键内容

1. **基本概念**：
   - Skills 通过 `.claude/skills/<name>/SKILL.md` 文件定义
   - 通过 `/command-name` 形式调用
   - 已取代旧的 `.claude/commands/` 系统

2. **Frontmatter 属性**：
   - `name`: 命令名（变成 `/name` 形式）
   - `description`: 简短说明，帮助 [[Claude_Code|Claude]] 判断何时使用
   - `argument-hint`: 自动补全时显示的参数提示
   - `allowed-tools`: 命令可无[[Permissions|权限]]使用的工具
   - `disable-model-invocation`: 是否禁用 [[Claude_Code|Claude]] 自动调用
   - `context`: 设为 `fork` 时在隔离 subagent 中运行

3. **[[渐进式披露（Progressive Disclosure）|按需加载]]机制**：
   - 会话启动时只加载工具名称（极低 Token 消耗）
   - [[Claude_Code|Claude]] 识别需要哪个 Skill 后[[渐进式披露（Progressive Disclosure）|按需加载]]完整内容
   - Skill 用完可从上下文卸载，保持上下文开销最小
   - 即使[[Configuration|配置]]了大量 Skills，上下文开销仍然最小

4. **功能特性**：
   - 支持参数传递（$ARGUMENTS、$0、$1 等）
   - 支持动态上下文注入（使用 `!` 前缀执行 shell 命令）
   - 支持文件引用（使用 `@` 引用文件内容）
   - 目录结构可打包相关资源文件

## 来源
- [[Claude How To Slash Commands Reference]] — 官方文档
- [[05_to_08_combined.md]] — 05 · CLAUDE.md & 上下文管理系统

## 相关
- [[Slash Commands]] — part_of
- [[MCP Prompts]] — related_to
- [[Claude Code]] — part_of
- [[上下文管理系统]] — relates_to
- [[CLAUDE.md]] — relates_to