---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["AI工程", "安全性", "权限管理"]
aliases: ["Permission Modes", "权限模式", "Claude Code Permissions"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.7
  - target: "[[Claude Code 插件系统]]"
    type: relates_to
    confidence: 0.6
  - target: "[[Auto Mode 安全分类器]]"
    type: implements
    confidence: 0.9
  - target: "[[Prompt Injection]]"
    type: defends_against
    confidence: 0.85
supersedes: null
---

# Claude Code 权限模式

## 概述
[[Permissions|权限]]模式控制 [[Claude Code]] 可以执行哪些操作，从完全交互式到完全自动化，提供 6 种[[Permissions|权限]]级别：default、acceptEdits、plan、auto、dontAsk、bypass[[Permissions]]。

## 关键内容

1. **六种[[Permissions|权限]]模式**：
   - **default**：默认模式，每步操作前确认
   - **acceptEdits**：自动接受文件编辑，但命令执行需确认
   - **plan**：仅规划模式，不执行任何文件修改或命令
   - **auto**：自动模式，由 [[Auto Mode 安全分类器]] 在每一步执行前审查
   - **dontAsk**：不询问模式，自动执行所有操作
   - **bypass[[Permissions]]**：绕过所有[[Permissions|权限]]检查，完全自动化

2. **使用场景**：
   - 探索性任务用 `plan` 模式先了解 [[Claude_Code|Claude]] 打算做什么
   - 常规开发用 `default` 或 `acceptEdits`
   - 自动化脚本用 `auto` 或 `dontAsk`
   - 信任 [[Claude_Code|Claude]] 的复杂任务用 `bypassPermissions`

3. **安全考量**：[[Permissions|权限]]模式是 [[Claude Code]] 安全模型的核心。`auto` 模式虽然方便，但由后台[[Auto Mode 安全分类器|安全分类器]]审查，仍属于 Research Preview 阶段。`bypassPermissions` 应仅在完全信任的场景下使用。

## 来源
- [[09-advanced-features/README.md]] — Claude HowTo 高级功能指南
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/15_claude_code_auto_mode.md]] — Claude Code Auto Mode 深度解析

## 相关
- [[斜杠命令（Slash Commands）]] — uses
- [[Claude Code 插件系统]] — relates_to
- [[Auto Mode 安全分类器]] — implements
- [[Prompt Injection]] — defends_against
