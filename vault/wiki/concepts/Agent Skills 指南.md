---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [skills, automation, reusability, standardization, AI工程]
aliases: ["Agent Skills Guide", "Skills Framework", "Claude Skills"]
relates_to: []
supersedes: null
---

# Agent Skills 指南

## 概述
[[Skills]] 是可以复用、可自动触发的能力包，包含 [[SKILL.md]]、参考文件、脚本和模板，支持[[渐进式加载]]和标准化流程。

## 关键内容

1. **主要特点**：
   - 可复用能力包，支持自动加载
   - 渐进式披露：描述 → [[SKILL.md]] → 支持文件
   - 包含脚本、模板、说明的完整解决方案

2. **存储位置**：
   - 项目目录：`.claude/skills/`
   - 用户目录：`~/.claude/skills/`
   - 自动发现机制无需手动注册

3. **文件结构**：
   - 基本结构：`my-skill/SKILL.md`
   - 支持可选字段：argument-hint、allowed-tools、model等
   - 遵循YAML frontmatter格式

## 来源
- [[Skills]] — 核心概念参考
- [[MCP Prompts]] — 相关提示机制
- [[Slash Commands]] — 命令系统对照

## 相关
- [[MCP Prompts]] — 扩展提示能力
- [[Subagents]] — 隔离任务执行
- [[Hooks]] — 事件触发机制
- [[Slash Commands]] — 手动命令系统
- [[Memory]] — 上下文管理系统
- [[CLAUDE.MD]] — 配置文件生成