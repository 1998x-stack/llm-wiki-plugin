---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [configuration, settings, management, AI工程]
aliases: ["Settings", "设置", "配置设置"]
relates_to: []
supersedes: null
---

# Settings

## 概述
[[Claude Code]] 的设置系统，通过多层级[[Configuration|配置]]文件实现灵活的系统[[Configuration|配置]]管理，包括用户级、项目级和本地级设置。

## 关键内容

1. **四层[[Configuration|配置]]结构**：
   - 企业策略层：企业管理员托管[[Configuration|配置]]，影响所有用户、所有项目
   - 用户全局层（~/.claude/settings.json）：当前用户的所有项目范围
   - 项目共享层（./.claude/settings.json）：当前项目的所有成员（提交到 Git）
   - 项目本地层（./.claude/settings.local.json）：仅当前用户在此项目（加入 .gitignore）

2. **优先级规则**：
   - 从高到低：项目本地层 > 项目共享层 > 用户全局层 > 企业策略层
   - 项目级设置可以补充但不覆盖用户级设置

3. **[[Configuration|配置]]类型**：
   - 个人偏好和常用[[allowedTools|工具白名单]]（用户全局层）
   - 团队级[[Permissions|权限]]、项目级 [[Hooks]]、共享 MCP（项目共享层）
   - 个人实验[[Configuration|配置]]、临时覆盖（项目本地层）

4. **版本控制考虑**：
   - 项目共享层设置提交到 Git，供团队共享
   - 项目本地层设置加入 .gitignore，避免污染团队[[Configuration|配置]]

## 来源
- [[05_to_08_combined.md]] — 06 · 配置 & 权限系统

## 相关
- [[Configuration]] — relates_to
- [[Environment Variables]] — relates_to
- [[MCP]] — relates_to
- [[Claude Code]] — relates_to