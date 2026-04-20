---
type: company
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 11
tags: [ai-company, llm, claude]
aliases: ["Anthropic", "Anthropic AI"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[OpenAI]]"
    type: compares_to
  - target: "[[MCP]]"
    type: implements
  - target: "[[AI Agent 架构模式]]"
    type: created
  - target: "[[评测驱动开发]]"
    type: implements
  - target: "[[Auto Mode 安全分类器]]"
    type: created
  - target: "[[Prompt Injection]]"
    type: researches
  - target: "[[抗 AI 评测设计]]"
    type: researches
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
   - **[[上下文检索]]**：2024 年 9 月提出的 RAG 改进方法，通过为文本块添加语境前缀降低检索失败率达 67%

3. **社区项目**：
   - `anthropics/skills`：官方 Skill 仓库（65k+ Stars）
   - `anthropics/claude-code`：[[Claude Code]] 主仓库
   - `frontend-design` Skill：反 [[AI Slop]] 的前端设计能力包

4. **评测方法论研究**：
   - [[Gian Segato]] 等发表关于 Agentic 编码评测中[[基础设施噪声]]的量化研究
   - 发现在 [[Terminal-Bench 2.0]] 上不同资源配置之间的成功率差距达 6 个百分点
   - 提出 Benchmark 资源配置的校准原则：分别规定 requests 和 limits，推荐 3× 带宽

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — Anthropic Engineering Blog 深度分析系列（23 篇文章索引）
- [[01_building_effective_agents.md]] — Anthropic Engineering Blog "Building effective agents"
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — Agent 评测系统工程指南
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/15_claude_code_auto_mode.md]] — Claude Code Auto Mode 安全分类器
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/19_ai_resistant_evals.md]] — 设计抗 AI 的技术评估
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/20_code_execution_mcp]] — 通过 MCP 的代码执行：构建更高效的 Agent

## 相关
- [[Claude Code]] — uses
- [[OpenAI]] — compares_to
- [[Agent Skills]] — implements
- [[Constitutional AI]] — relates_to
- [[上下文检索]] — implements
- [[Gian Segato]] — employs（Anthropic Engineering 团队成员）
- [[基础设施噪声]] — researches（量化研究并发表工程建议）
- [[Auto Mode 安全分类器]] — created（Auto Mode 核心安全组件）
- [[Prompt Injection]] — researches（防御机制研究）
- [[抗 AI 评测设计]] — researches（Anthropic Engineering 团队研究并发表）
