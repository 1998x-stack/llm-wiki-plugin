---
type: company
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 4
tags: [ai-company, llm, claude]
aliases: ["Anthropic", "Anthropic AI"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[OpenAI]]"
    type: compares_to
  - target: "[[MCP]]"
    type: implements
---

# Anthropic

## 概述
美国人工智能安全研究公司，成立于 2021 年，开发 Claude 系列大语言模型及 [[Claude Code]] AI 编程工具，提出 Constitutional AI 和 [[Agent Skills]] 规范。

## 关键内容

1. **核心产品**：
   - **Claude**：大语言模型系列（Haiku、Sonnet、Opus）
   - **[[Claude Code]]**：AI 驱动代码编辑器
   - **[[Agent Skills]]**：开放规范 [[agentskills.io]]/specification

2. **技术贡献**：
   - **Constitutional AI**：基于宪法原则的 AI 对齐方法
   - **[[Agent Skills]] 规范**：被 [[Claude Code]]、[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]] 共同采用
   - **[[Context Engineering]]**：[[Context Engineering|上下文工程]]方法论
   - **MCP（[[MCP|Model Context Protocol]]）**：2024 年末提出的标准协议，定义 AI Agent 与外部工具/数据源之间的通信方式，被称为"AI 的 USB 接口"

3. **社区项目**：
   - `anthropics/skills`：官方 Skill 仓库（65k+ Stars）
   - `anthropics/claude-code`：[[Claude Code]] 主仓库
   - `frontend-design` Skill：反 [[AI Slop]] 的前端设计能力包

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成

## 相关
- [[Claude Code]] — uses
- [[OpenAI]] — compares_to
- [[Agent Skills]] — implements
- [[Constitutional AI]] — relates_to
