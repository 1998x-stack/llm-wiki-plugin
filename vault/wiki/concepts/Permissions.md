---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [security, authorization, access-control, AI工程]
aliases: ["Permissions", "权限", "权限系统"]
relates_to: []
supersedes: null
---

# Permissions

## 概述
[[Claude Code]] 中的权限系统，通过多层次的权限控制机制实现对工具调用的安全管理，确保在"零人工审批"和"完全用户控制"之间取得平衡。

## 关键内容

1. **权限决策流程**：
   - [[Tool Hook Mechanism|PreToolUse Hook]]（确定性拦截层）：命中黑名单立即拦截（exit 2）
   - 查询 [[allowedTools]] 白名单：白名单命中自动允许，无需用户确认
   - PermissionRequest Hook：Hook 自动授权跳过用户弹窗
   - 用户手动确认：允许一次/本会话/永久允许

2. **多层级[[Configuration|配置]]**：
   - 企业策略层：企业管理员托管[[Configuration|配置]]，覆盖所有用户、所有项目
   - 用户全局层：当前用户的所有项目范围
   - 项目共享层：当前项目的所有成员（提交到 Git）
   - 项目本地层：仅当前用户在此项目（加入 .gitignore）

3. **[[allowedTools]] [[Configuration|配置]]**：
   - 白名单机制，定义哪些工具可自动执行
   - 支持通配符匹配（如 Bash(git diff*)）
   - 包括具体命令或命令模式

4. **安全最佳实践**：
   - 避免 Token 硬编码在[[Configuration|配置]]文件中
   - 按工具细粒度控制权限
   - [[Environment Variables|环境变量]]方式传递敏感信息

## 来源
- [[05_to_08_combined.md]] — 06 · 配置 & 权限系统

## 相关
- [[配置权限系统]] — relates_to
- [[allowedTools]] — relates_to
- [[Security Filter Layer]] — relates_to
- [[Tool Hook Mechanism]] — relates_to