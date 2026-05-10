---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [permissions, security, tools]
aliases: ["allowedTools", "允许工具列表", "工具白名单"]
relates_to: []
supersedes: null
---

# allowedTools

## 概述
allowed[[Tool System|Tools]] 是 [[Claude Code]] 中的工具白名单[[Configuration|配置]]，用于定义哪些工具可以自动执行而无需用户确认，提高工作效率的同时保证安全性。

## 关键内容

1. **白名单机制**：
   - 在[[Permissions|权限]]决策流程中，查询 allowed[[Tool System|Tools]] 白名单
   - 白名单中的工具可自动允许执行，无需用户确认
   - 未在白名单中的工具需用户手动确认

2. **[[Configuration|配置]]格式**：
   - 支持具体命令（如 "Bash(git status)"）
   - 支持通配符模式（如 "Bash(git diff*)"、"mcp__github__*"）
   - 按工具类型和参数进行精细控制

3. **[[Configuration|配置]]示例**：
   ```
   {
     "allowedTools": [
       "Bash(git status)",
       "Bash(git diff*)",
       "Bash(npm test)",
       "Bash(npm run lint)",
       "Edit",
       "View",
       "mcp__github__list_issues",
       "mcp__github__*"
     ]
   }
   ```

4. **安全考虑**：
   - 按工具细粒度控制，避免[[Permissions|权限]]过度
   - 可以通过通配符批量[[Configuration|配置]]相关工具
   - 需要定期审查和更新白名单内容

## 来源
- [[05_to_08_combined.md]] — 06 · 配置 & 权限系统

## 相关
- [[Permissions]] — relates_to
- [[配置权限系统]] — relates_to
- [[Tool Hook Mechanism]] — relates_to
- [[Security Filter Layer]] — relates_to