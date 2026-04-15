---
type: entity
title: Claude Code
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: '2026-04-15'
source_count: 1
tags:
- AI
- 工具
- 方法论
aliases:
- Claude Code CLI
- claude-code
- Anthropic Claude Code
relates_to:
- target: '[[Claude-Mem]]'
  type: related_to
  confidence: 1.0
- target: '[[Claude-Code-Hook-System|Claude Code Hook System]]'
  type: related_to
  confidence: 0.95
- target: '[[claude-cli-tools|Claude CLI 工具生态]]'
  type: part_of
  confidence: 0.9
supersedes: null
---

# Claude Code

## 概述
Claude Code 是 Anthropic 官方发布的 AI 编程助手 CLI（命令行界面）工具，基于 Claude 模型（Opus/Sonnet/Haiku）驱动。它深度集成于终端工作流，支持全代码库理解、多文件原子编辑、Git 集成和 MCP（Model Context Protocol）协议。通过 Hook 系统支持第三方插件扩展（如 Claude-Mem），是当代 AI 辅助软件工程（AISE）的核心工具。

## 关键内容
### 核心特性
- **代码库理解**：通过读取文件、搜索代码、分析依赖，构建全代码库上下文
- **原子编辑**：多文件协调修改，保证变更的一致性
- **Hook 系统**：PreToolUse / PostToolUse 生命周期钩子，允许第三方脚本在工具调用前后介入
- **MCP 支持**：通过 MCP 协议连接 300+ 外部服务（GitHub、数据库、Slack 等）
- **CLAUDE.md**：项目级指令文件，为 Claude Code 提供持久的项目上下文和规范

### 子代理架构
Claude Code 支持并行 Agent 模式：主代理可将复杂任务分解为子任务，调度多个子代理并行处理，类似 MapReduce。

## 来源
- 综合自 wiki 内部引用（Claude-Code-Hook-System、claude-cli-tools 等页面）

## 相关
- [[Claude-Mem]]
- [[Claude-Code-Hook-System|Claude Code Hook System]]
- [[claude-cli-tools|Claude CLI 工具生态]]
- [[LLM-Statelessness|LLM 无状态性]]
