---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Slash Commands", "斜杠命令", "Claude Code Commands"]
relates_to:
  - target: "[[Agent Skills]]"
    type: extends
    confidence: 0.9
  - target: "[[MCP协议层]]"
    type: extends
    confidence: 0.7
  - target: "[[Claude Code 分层验证]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# 斜杠命令（Slash Commands）

## 概述
Claude Code 中用户手动触发的快捷操作，分为四类：内置命令（55+ 个）、[[Agent Skills|Skills]]（自定义命令）、插件命令（来自已安装插件）和 MCP prompts（来自 MCP server）。

## 关键内容

1. **四类命令**：
   - **内置命令**：Claude Code 自带，如 `/help`、`/clear`、`/model`、`/compact`、`/context`、`/cost`
   - **[[Agent Skills|Skills]]**：用户自定义命令，基于 `SKILL.md` 文件，如 `/optimize`、`/pr`
   - **插件命令**：来自已安装插件，如 `/frontend-design:frontend-design`
   - **MCP prompts**：来自 MCP server，如 `/mcp__github__list_prs`

2. **重要内置命令**：
   - `/compact [instructions]`：压缩对话，可附带聚焦指令
   - `/context`：用彩色网格可视化上下文占用
   - `/cost`：查看 token 使用统计
   - `/effort [low|medium|high|max|auto]`：设置推理强度，`max` 需要 Opus 4.6
   - `/fast [on|off]`：切换快速模式
   - `/branch [name]`：将当前[[会话分支（Branching）|对话分支]]到新会话（v2.1.77 中 `/fork` 更名为 `/branch`）
   - `/sandbox`：切换沙箱模式
   - `/teleport`：将会话转移到另一台机器
   - `/rewind`：回退到 checkpoint

3. **自定义命令合并**：自定义 slash command 已合并进 [[Agent Skills|Skills]]。`.claude/commands/` 仍然可用，但更推荐使用 `.claude/skills/`。两者都会创建 `/command-name` 形式的快捷命令。

## 来源
- [[01-slash-commands/README.md]] — Claude HowTo 斜杠命令参考指南

## 相关
- [[Agent Skills]] — extends
- [[MCP协议层]] — extends
- [[Claude Code 分层验证]] — relates_to
