---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [claude, cli, commands, skills]
aliases: ["Slash Command", "斜杠命令"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
supersedes: null
---

# Slash Commands

## 概述
Slash command 是在 [[Claude_Code|Claude]] 的交互式会话中用来控制行为的快捷方式，主要分为内置命令、[[Skills]]、插件命令和 MCP prompts。

## 关键内容

1. **命令分类**：
   - **内置命令**：[[Claude Code]] 自带，例如 `/help`、`/clear`、`/model`
   - **[[Skills]]**：基于 `SKILL.md` 文件自定义的命令，例如 `/optimize`、`/pr`
   - **插件命令**：来自已安装插件的命令，例如 `/frontend-design:frontend-design`
   - **MCP prompts**：来自 MCP server 的命令，例如 `/mcp__github__list_prs`

2. **[[Skills]] 系统**：
   - 自定义 slash command 已合并进 [[Skills]] 系统
   - 推荐使用 `.claude/skills/<name>/SKILL.md` 结构
   - 目录结构可以打包脚本、模板、参考文件
   - 支持自动触发和子 agent 执行

3. **命令实现**：
   - 使用 frontmatter 定义命令属性（name、description、argument-hint 等）
   - 支持参数传递（$ARGUMENTS、$0、$1 等）
   - 可通过 `!` 前缀注入动态上下文
   - 支持 `@` 引用文件内容

## 来源
- [[Claude How To Slash Commands Reference]] — 官方文档

## 相关
- [[Skills]] — uses
- [[MCP Prompts]] — uses
- [[Claude Code]] — part_of