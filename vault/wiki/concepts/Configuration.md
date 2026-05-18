---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [settings, configuration, management, AI工程]
aliases: ["Configuration", "配置", "配置系统"]
relates_to: []
supersedes: null
---

# Configuration

## 概述
[[Claude Code]] 的配置系统，通过多层级配置文件实现灵活而安全的系统[[Settings|设置]]，确保不同层面的需求得到满足。

## 关键内容

1. **四层配置结构**：
   - 企业策略层（企业管理员托管配置）：影响所有用户、所有项目，如禁止访问生产 DB、强制代码审计日志
   - 用户全局层（~/.claude/settings.json）：当前用户的所有项目范围，如个人偏好、常用[[allowedTools|工具白名单]]
   - 项目共享层（./.claude/settings.json）：当前项目的所有成员（提交到 Git），如团队级[[Permissions|权限]]、项目级 [[Hooks]]、共享 MCP
   - 项目本地层（./.claude/settings.local.json）：仅当前用户在此项目（加入 .gitignore），如个人实验配置、临时覆盖

2. **MCP 配置位置**：
   - 用户级 MCP：~/.claude.json（注意：不在 ~/.claude/ 目录内）
   - 项目级 MCP：./.mcp.json（提交到 Git，团队共享）
   - 规则：项目级 MCP 补充（不覆盖）用户级 MCP

3. **关键[[Environment Variables|环境变量]]**：
   - ANTHROPIC_API_KEY：API 认证
   - CLAUDE_MODEL：[[模型选择]]
   - MAX_MCP_OUTPUT_TOKENS：MCP 输出 Token 上限
   - ENABLE_TOOL_SEARCH：工具搜索模式

4. **反模式清单**：
   - Token 硬编码在配置文件中导致机密泄露
   - CI/CD 中不加 `-p` 标志导致作业无限期挂起
   - 永久允许所有 MCP 工具导致[[Permissions|权限]]过度
   - settings.local.json 提交到 Git 导致个人配置污染团队

## 来源
- [[05_to_08_combined.md]] — 06 · 配置 & 权限系统

## 相关
- [[配置权限系统]] — relates_to
- [[MCP]] — relates_to
- [[Settings]] — relates_to
- [[Environment Variables]] — relates_to