---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 5
tags: ["ai-tools", "coding-assistant", "anthropic", "Agent系统", "terminal-agent", "tech-stack"]
aliases: ["Claude Code", "ClaudeCode", "Claude Code 系统"]
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
  - target: "[[Skills]]"
    type: implements
  - target: "[[MCP Prompts]]"
    type: implements
  - target: "[[Slash Commands]]"
    type: implements
  - target: "[[TypeScript]]"
    type: uses
  - target: "[[Bun]]"
    type: uses
  - target: "[[Anthropic Messages API]]"
    type: uses
  - target: "[[MCP（Model Context Protocol）]]"
    type: uses
  - target: "[[外部工具集成]]"
    type: enables
  - target: "[[React]]"
    type: uses
  - target: "[[Ink]]"
    type: uses
  - target: "[[Yoga]]"
    type: uses
  - target: "[[Terminal Renderer Engine]]"
    type: implements
  - target: "[[Tool System]]"
    type: contains
  - target: "[[BUDDY]]"
    type: contains
  - target: "[[ULTRAPLAN]]"
    type: contains
  - target: "[[VOICE_MODE]]"
    type: contains
  - target: "[[autoCompact]]"
    type: implements
  - target: "[[Prompt Cache]]"
    type: implements
  - target: "[[三层记忆架构]]"
    type: implements
  - target: "[[Self-Healing Memory]]"
    type: implements
  - target: "[[MEMORY.md]]"
    type: uses
  - target: "[[Topic Files]]"
    type: uses
  - target: "[[Transcripts]]"
    type: uses
  - target: "[[Strict Write Discipline]]"
    type: implements
  - target: "[[矛盾检测与解决]]"
    type: implements
---

# Claude Code

## 概述
运行在终端的自主编码智能体，采用极简 Harness 架构——LLM 大脑 + 真实世界身体（Shell / 文件系统 / 外部[[服务]]）。[[Anthropic]] 推出的 AI 驱动代码编辑器，基于 [[Claude_Code|Claude]] 模型，支持 [[Agent Skills]]、[[MCP|MCP Servers]] 和 [[Plugins]] 扩展机制，提供多智能体协作和[[Context Engineering|上下文工程]]能力。

## 关键内容

1. **产品哲学**："The product is the model"。不像其他编码产品把 LLM 层层包裹，[[Claude_Code|Claude]] Code 让模型直接与系统交互，提供原始模型体验。强调最少业务逻辑原则：Client 端只负责 UI 渲染 + 工具路由，智能完全来自模型。

2. **三代 LLM 应用演化**：
   - 第一代：聊天机器人（无状态问答，控制权归人）
   - 第二代：工作流（[[LangChain]] / n8n，代码驱动的 DAG 链，控制权归代码）
   - 第三代：自主 Agent（[[Claude_Code|Claude]] Code，模型驱动的循环，控制权归模型）

3. **技术栈**：
   - 语言：[[TypeScript]]（类型安全 + 模型自编率极高）
   - UI 框架：[[React]] + Ink（声明式终端 UI，模型可控）
   - 布局引擎：Yoga（Meta 开源，约束布局，适配任意终端宽度）
   - 构建工具：Bun（比 Webpack/Vite 显著更快）
   - API：[[Anthropic Messages API]]（直接暴露模型能力）
   - 协议：MCP（[[Model Context Protocol]]，标准化外部[[服务]]接入）
   - 持久化：`~/.claude/sessions/<id>/transcript.jsonl`（会话历史，支持 /resume）

4. **系统架构**：
   - 用户接口层：CLI、[[VS Code]] 插件、Web UI
   - 核心 Agent 层：[[nO 主循环]]（[[TAOR Loop]] - Think → Act → Observe → Repeat）
   - [[Context Management|上下文管理]]器：[[Compressor wU2]]（触发阈值：92%）
   - 规划系统：[[TodoWrite-Tool|TodoWrite]]、Reminder 注入（目标锚定、防目标漂移）
   - 确定性控制层：[[Hooks 系统]]（21 个生命周期事件，4 种处理器类型）
   - [[Tool Ecosystem|工具生态系统]]：Read、[[Write]]、[[Execute]]、[[Connect]] [[Claude Code四大能力基元|四大能力基元]]
   - [[Configuration|配置]][[Permissions|权限]]层：settings.json 4 级层级，Permission 白名单/黑名单
   - 扩展层：MCP 外部[[服务]]、[[Skills]]、[[Plugins]]
   - 委派层：[[子 Agent & 多 Agent 系统|子 Agent]]、[[Git Worktree]] 隔离、并行 Agent Teams
   - 持久化上下文层：[[CLAUDE.md]] 三级层级（全局/项目/子目录），跨会话架构记忆、编码规范、架构决策记录（ADR）
   
5. **工具系统与安全机制**：
   - 内置40+工具：文件系统工具、[[代码执行]]工具、网络API工具、多智能体工具、Git版本控制工具、记忆状态工具
   - [[BashTool]]安全机制：23项安全检查，包括命令黑名单、Zsh特有威胁防护、Unicode安全检查、管道与重定向分析
   - [[Permissions|权限]]三级体系：Level 3自动执行、Level 2单次确认、Level 1永久拒绝或特殊授权
   - 85+[[Slash Commands|斜杠命令]]系统：Git工作流命令、记忆与项目管理命令、多智能体命令、调试诊断命令

5. **[[Claude Code四大能力基元|四大能力基元]]**：
   - **Read（读）**：View、LS、Glob、[[GrepTool]] - 理解代码库、搜索文件
   - **[[Write]]（写）**：Edit、[[Write]]/Replace、Create - patch、全文替换、新建文件
   - **[[Execute]]（执行）**：Bash（持久 Shell 会话）- git、npm、docker、pytest
   - **[[Connect]]（连接）**：MCP 协议 - [[GitHub]]、DB、Sentry、[[Slack]]

6. **运营指标**：
   - 代码自生率：90% 由 [[Claude_Code|Claude]] Code 自己编写
   - 发布频率：每位工程师每天约 5 次
   - 年化收入：GA 后 3 个月突破 $500M ARR，增长 10×
   - 用户粘性：7×24 小时不间断运行，触发 [[Anthropic]] 实施周用量限制
   - 迭代速度：每个新功能经历 10+ 个真实原型迭代
   - 模型上下文：Sonnet：200k tokens，Opus 默认输出上限 64k tokens

7. **扩展机制全家桶**：
   - **[[CLAUDE.md]]**：项目持久记忆文件
   - **[[Agent Skills]] ([[SKILL.md 格式规范|SKILL.md]])**：目录级可复用能力包
   - **[[MCP|MCP Servers]]**：进程级工具[[服务]]
   - **[[Claude Connectors]]**：远程 MCP [[服务]]（[[Slack]]、Figma 等）
   - **[[Plugins]]**：[[Agent Skills|Skills]] + [[Agents]] + [[Hooks]] + [[MCP Prompts|MCP Server]] 的发布单元
   - **[[Agents]]**：专用[[Subagents-in-Claude-Code|子智能体]]
   - **[[Hooks]]**：生命周期钩子（PreTool、PostTool 等）
   - **[[Slash Commands]]**：[[Slash Commands|斜杠命令]]系统，包括内置命令、[[Skills]]、插件命令和 [[MCP Prompts]]

8. **三层[[渐进式加载]]机制**：
   - 第 1 层：启动时加载所有 [[Skills|Skill]] 的 name + description（~100 tokens/skill）
   - 第 2 层：任务匹配后[[渐进式披露（Progressive Disclosure）|按需加载]]完整 [[SKILL.md 格式规范|SKILL.md]]（<5,000 tokens）
   - 第 3 层：执行过程中明确需要时加载 references/

9. **跨工具兼容性**：[[Agent Skills]] 规范被 [[Claude_Code|Claude]] Code、[[OpenAI Codex]]、[[Cursor]]、[[Gemini CLI]] 共同采用

## 来源
- [[01_claude_code_skill_system_overview]] — 系统架构全景
- [[01-overview-context-rot]] — Context Rot 与上下文工程
- [[02_anthropic_frontend_design_skill]] — frontend-design Skill 解析
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 协作开发案例
- [[01_system_overview.md]] — Claude Code 系统总览 & Tech Stack

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
- [[TypeScript]] — uses
- [[Bun]] — uses
- [[Anthropic Messages API]] — uses
- [[MCP（Model Context Protocol）]] — uses
- [[外部工具集成]] — enables
- [[React]] — uses
- [[Ink]] — uses
- [[Yoga]] — uses
- [[TAOR Loop]] — core_pattern
- [[Hooks 系统]] — core_component
- [[MCP Servers]] — uses
- [[Skills]] — implements
- [[Slash Commands]] — implements

## 指令
