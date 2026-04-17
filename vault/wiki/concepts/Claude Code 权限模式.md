---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程"]
aliases: ["Permission Modes", "权限模式", "Claude Code Permissions"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.7
  - target: "[[Claude Code 插件系统]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# Claude Code 权限模式

## 概述
权限模式控制 Claude Code 可以执行哪些操作，从完全交互式到完全自动化，提供 6 种权限级别：default、acceptEdits、plan、auto、dontAsk、bypassPermissions。

## 关键内容

1. **六种权限模式**：
   - **default**：默认模式，每步操作前确认
   - **acceptEdits**：自动接受文件编辑，但命令执行需确认
   - **plan**：仅规划模式，不执行任何文件修改或命令
   - **auto**：自动模式，由后台安全分类器在每一步执行前审查（Research Preview）
   - **dontAsk**：不询问模式，自动执行所有操作
   - **bypassPermissions**：绕过所有权限检查，完全自动化

2. **使用场景**：
   - 探索性任务用 `plan` 模式先了解 Claude 打算做什么
   - 常规开发用 `default` 或 `acceptEdits`
   - 自动化脚本用 `auto` 或 `dontAsk`
   - 信任 Claude 的复杂任务用 `bypassPermissions`

3. **安全考量**：权限模式是 Claude Code 安全模型的核心。`auto` 模式虽然方便，但由后台安全分类器审查，仍属于 Research Preview 阶段。`bypassPermissions` 应仅在完全信任的场景下使用。

## 来源
- [[09-advanced-features/README.md]] — Claude HowTo 高级功能指南

## 相关
- [[斜杠命令（Slash Commands）]] — uses
- [[Claude Code 插件系统]] — relates_to
