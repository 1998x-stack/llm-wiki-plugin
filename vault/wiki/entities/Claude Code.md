---
type: project
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-20
source_count: 7
tags: ["ai-tools", "coding-assistant", "anthropic", "Agent系统"]
aliases: ["Claude Code", "ClaudeCode"]
relates_to:
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Agent Skills]]"
    type: implements
  - target: "[[OpenAI Codex]]"
    type: compares_to
  - target: "[[Cursor]]"
    type: compares_to
  - target: "[[Ralph Loop]]"
    type: used_by
---

# Claude Code

## 概述
[[Anthropic]] 推出的 AI 驱动代码编辑器，基于 Claude 模型，支持 [[Agent Skills]]、[[MCP|MCP Servers]] 和 Plugins 扩展机制，提供多智能体协作和[[Context Engineering|上下文工程]]能力。

## 关键内容

1. **核心定位**：AI 原生代码编辑器，通过自然语言对话完成软件开发全流程

2. **扩展机制全家桶**：
   - **CLAUDE.md**：项目持久记忆文件
   - **[[Agent Skills]] ([[SKILL.md 格式规范|SKILL.md]])**：目录级可复用能力包
   - **[[MCP|MCP Servers]]**：进程级工具服务
   - **Claude Connectors**：远程 MCP 服务（Slack、Figma 等）
   - **Plugins**：[[Agent Skills|Skills]] + Agents + Hooks + MCP Server 的发布单元
   - **Agents**：专用[[Subagents-in-Claude-Code|子智能体]]
   - **Hooks**：生命周期钩子（PreTool、PostTool 等）

3. **三层[[渐进式加载]]机制**：
   - 第 1 层：启动时加载所有 Skill 的 name + description（~100 tokens/skill）
   - 第 2 层：任务匹配后[[渐进式披露（Progressive Disclosure）|按需加载]]完整 [[SKILL.md 格式规范|SKILL.md]]（<5,000 tokens）
   - 第 3 层：执行过程中明确需要时加载 references/

4. **跨工具兼容性**：[[Agent Skills]] 规范被 Claude Code、[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]] 共同采用

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[01-overview-context-rot]] — Context Rot 与上下文工程
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 协作开发案例
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — Claude Code 工程实践（Auto Mode、沙箱、Skills 体系）
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/19_ai_resistant_evals.md]] — 设计抗 AI 的技术评估（提及 Claude Code 可在几秒内解决经典算法题）
- [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) — Claude Code 沙箱机制详解，2025 年 10 月 20 日

## 相关
- [[Anthropic]] — part_of
- [[Agent Skills]] — implements
- [[SKILL.md]] — uses
- [[MCP]] — uses
- [[OpenAI Codex]] — compares_to
- [[Cursor]] — compares_to
- [[Gemini CLI]] — compares_to
- [[Ralph Loop]] — used_by（作为底层编码代理驱动自主迭代循环）
- [[MemPalace]] — used_by（Milla Jovovich 与 Ben Sigman 用 Claude Code 协作开发）
- [[Claude Code 沙箱机制]] — implements
