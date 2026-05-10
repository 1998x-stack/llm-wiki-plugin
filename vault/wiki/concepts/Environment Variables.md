---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [environment, configuration, settings]
aliases: ["Environment Variables", "环境变量", "环境变量系统"]
relates_to: []
supersedes: null
---

# Environment Variables

## 概述
[[Claude Code]] 中的关键环境变量[[Configuration|配置]]，用于控制系统的各种行为和[[Settings|设置]]，包括 API 认证、模型选择和输出限制等。

## 关键内容

1. **认证与模型[[Settings|设置]]**：
   - ANTHROPIC_API_KEY：API 认证密钥
   - CLAUDE_MODEL：指定使用的模型（如 [[Claude-Sonnet-4-6|claude-sonnet-4-6]]）

2. **输出控制**：
   - MAX_MCP_OUTPUT_TOKENS：MCP 输出 Token 上限，默认 25000

3. **功能开关**：
   - ENABLE_TOOL_SEARCH：工具搜索模式[[Configuration|配置]]

4. **CI/CD 特殊[[Configuration|配置]]**：
   - 在 CI/CD 环境中防止 [[Claude_Code|Claude]] 无限期等待用户输入
   - 使用 `claude -p "your task" --output-format json` 命令格式

## 来源
- [[05_to_08_combined.md]] — 06 · 配置 & 权限系统

## 相关
- [[Configuration]] — relates_to
- [[Settings]] — relates_to
- [[Claude Code]] — relates_to
- [[MCP]] — relates_to