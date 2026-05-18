---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-tools, coding-assistant, skills-system, AI工程]
aliases: ["Claude Code", "Claude", "Anthropic Claude"]
relates_to:
  - target: "[[反蒸馏系统]]"
    type: implements
  - target: "[[客户端证明]]"
    type: implements
  - target: "[[Undercover Mode]]"
    type: implements
  - target: "[[权限模型]]"
    type: implements
supersedes: null
---

# Claude Code

## 概述
[[Claude Code]] 是 [[Anthropic]] 推出的 AI 编码助手，支持多种扩展机制包括 [[Skills]]、[[Agents]]、[[Hooks]] 等。

## 关键内容

1. **扩展机制**：
   - 最初提供 [[Custom Slash Commands]] 机制
   - 后来采用 [[Agent Skills]] 规范，全面替代 [[Slash Commands]]
   - 支持 [[MCP|MCP Servers]]、[[Claude Connectors]]、[[Plugins]] 等多种扩展方式

2. **[[Skills]] 系统**：
   - 基于 [[SKILL.md]] 文件定义
   - 支持三层[[渐进式加载]]机制
   - 通过 description 字段进行语义匹配激活

3. **生态系统**：
   - 与社区共同制定 [[Agent Skills]] 规范
   - 支持 Plugin Marketplace 进行分发
   - 可与其他工具（[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]]）互通

## 来源
- [[01_claude_code_skill_system_overview.md]] — 全景介绍
- [[]] —

## 相关
- [[Agent Skills]] — extends
- [[Custom Slash Commands]] — supersedes
- [[MCP Servers]] — relates_to