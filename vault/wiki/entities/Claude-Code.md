---
type: entity
title: Claude Code
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: '2026-04-16'
source_count: 3
tags: [AI, 工具, 方法论, Agent系统]
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
- target: '[[Claude Code 分层验证]]'
  type: caused
  confidence: 0.9
- target: '[[渐进式披露 -Progressive-Disclosure]]'
  type: uses
  confidence: 0.95
- target: '[[AskUserQuestion-Tool]]'
  type: implements
  confidence: 0.9
- target: '[[Task-Tool]]'
  type: implements
  confidence: 0.9
- target: '[[TodoWrite-Tool]]'
  type: implemented_by
  confidence: 0.85
  note: "已废弃，被 Task Tool 取代"
supersedes: null
---

# Claude Code

## 概述
[[Claude Code]] 是 [[Anthropic]] 官方发布的 AI 编程助手 CLI（命令行界面）工具，基于 Claude 模型（Opus/Sonnet/Haiku）驱动。它深度集成于终端工作流，支持全代码库理解、多文件原子编辑、Git 集成和 MCP（[[MCP协议层|Model Context Protocol]]）协议。通过 Hook 系统支持第三方插件扩展（如 [[Claude-Mem]]），是当代 AI 辅助软件工程（AISE）的核心工具。

## 关键内容
### 核心特性
- **代码库理解**：通过读取文件、搜索代码、分析依赖，构建全代码库上下文
- **原子编辑**：多文件协调修改，保证变更的一致性
- **Hook 系统**：PreToolUse / PostToolUse 生命周期钩子，允许第三方脚本在工具调用前后介入
- **MCP 支持**：通过 MCP 协议连接 300+ 外部服务（GitHub、数据库、Slack 等）
- **CLAUDE.md**：项目级指令文件，为 [[Claude Code]] 提供持久的项目上下文和规范
### 子代理架构

[[Claude Code]] 支持并行 Agent 模式：主代理可将复杂任务分解为子任务，调度多个子代理并行处理，类似 [[MapReduce]]。

### 工具设计哲学

**"像智能体一样观察"（See like an agent）**：
- 工具设计需要契合模型自身能力，而非人类直觉
- 需要站在模型角度思考：需要什么样的工具？
- 实验频繁、阅读输出、尝试新方法
- 随着模型能力提升，工具也必须演进

**核心工具演进**：
- **[[AskUserQuestion-Tool|AskUserQuestion Tool]]**：三阶段演进（修改 [[ExitPlanTool]] → 更改输出格式 → 独立工具）
- **[[TodoWrite-Tool|TodoWrite]] → [[Task-Tool|Task Tool]]**：从"保持模型轨道"到"Agent 间协调"
- **RAG → Grep → [[Agent Skills]]**：从"被动接受上下文"到"主动嵌套搜索"

**渐进式披露**：
- [[Claude Code]] 添加新功能而不新增工具的常用技巧
- [[Claude Code]] Guide 智能体：子代理在自身上下文中搜索文档，只返回答案
- 保持主上下文清洁，避免[[上下文腐烂]]

**工具数量控制**：
- [[Claude Code]] 目前拥有约 20 个工具
- 新增工具门槛高（每增加一个工具就增加一个选项）
- 坚持使用少数能力特征相似的模型，降低工具设计复杂度

### Edit 后验证分层

[[Claude Code]] 的 edit 后验证采用四层架构：
- **LSP**：每次 edit 后自动报告 type errors 和 warnings，作为第一道即时反馈
- **Hooks（settings.json）**：通过 `PostToolUse` 钩子在 Edit/Write 后自动触发 lint/test，支持 `additionalContext` 回灌和 `decision: "block"` 阻断
- **CLAUDE.md**：定义项目级验证策略（最小检查原则、提交前门槛等），每个会话自动加载
- **Tool Description**：定义自定义 validate 工具的用法和示例，教会 Claude 正确调用
## 来源

- 综合自内部引用：[[Claude-Code-Hook-System]]、[[claude-cli-tools]] 等
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/12-claude code中，edit后做 validate  linting，需要在tool des.md]] — Claude Code 分层验证设计

## 相关

- [[Claude-Mem]]
- [[Claude-Code-Hook-System|Claude Code Hook System]]
- [[claude-cli-tools|Claude CLI 工具生态]]
- [[LLM-Statelessness|LLM 无状态性]]
- [[Claude Code 分层验证]] — caused（平台能力催生了分层验证架构）
- [[渐进式披露 -Progressive-Disclosure]] — uses（核心设计方法论）
- [[AskUserQuestion-Tool]] — implements（内置提问工具）
- [[Task-Tool]] — implements（任务协调工具）
- [[ExitPlanTool]] — implements（计划生成工具）
- [[TodoWrite-Tool]] — implemented_by（已废弃）
- [[Thariq-Shihipar]] — 工具设计哲学提出者
