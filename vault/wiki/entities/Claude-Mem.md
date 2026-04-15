---
type: entity
title: "Claude-Mem"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [AI, 工具，方法论，研究]
aliases: ["Claude Memory Plugin", "Claude Code Memory", "Claude Memory"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
    confidence: 1.0
  - target: "[[LLM Statelessness]]"
    type: contradicts
    confidence: 0.95
  - target: "[[Bun Runtime]]"
    type: uses
    confidence: 0.9
  - target: "[[SQLite]]"
    type: uses
    confidence: 1.0
  - target: "[[ChromaDB]]"
    type: uses
    confidence: 0.85
  - target: "[[Alex Newman]]"
    type: caused
    confidence: 1.0
  - target: "[[Lifecycle Hooks]]"
    type: uses
    confidence: 1.0
  - target: "[[Worker Service]]"
    type: depends_on
    confidence: 1.0
  - target: "[[Smart Install]]"
    type: uses
    confidence: 1.0
  - target: "[[Context Hook]]"
    type: uses
    confidence: 1.0
  - target: "[[New Hook]]"
    type: uses
    confidence: 1.0
  - target: "[[Save Hook]]"
    type: uses
    confidence: 1.0
  - target: "[[Summary Hook]]"
    type: uses
    confidence: 1.0
  - target: "[[Cleanup Hook]]"
    type: uses
    confidence: 1.0
supersedes: null
---

# Claude-Mem

## 概述
Claude-Mem 是一个专为 **Claude Code** 设计的开源持久化记忆插件，旨在解决大型语言模型（LLM）固有的“无状态”缺陷。通过自动捕获会话中的工具调用、利用 AI 进行智能压缩并存储于本地数据库，它使 AI 编程助手能够跨越多次会话保留项目上下文、逻辑边界及配置细节。该系统采用“两进程 + 一数据库”架构，结合 Hook 系统与后台 Worker 服务，实现了零用户干预的自动化记忆管理，显著降低了重复解释的摩擦成本。

## 关键内容
### 核心功能与设计哲学
Claude-Mem 的核心命题是赋予 AI 编程助手真实的项目记忆。在传统模式下，LLM 每次新建会话都会丢失之前的上下文，导致开发者需要反复解释项目背景、调试历史及配置细节。Claude-Mem 通过以下四个步骤解决这一问题：
1. **自动捕获**：利用 Claude Code 的钩子系统（Hook System）实时监听所有工具调用（如文件读写、命令执行）。
2. **AI 压缩**：调用 Claude Agent SDK 将原始的工具日志提炼为结构化的「观察记录」（Observations），去除冗余信息。
3. **持久存储**：将压缩后的记忆存入本地的 SQLite 数据库，并可选地使用 ChromaDB 进行向量嵌入。
4. **智能注入**：在新会话启动时，自动检索相关历史上下文并注入到初始提示词中，实现记忆的无缝延续。

### 系统架构
系统采用“两进程 + 一数据库”模型：
- **主进程（Claude Code）**：运行 6 个 JavaScript 钩子脚本（context, new, save, summary, cleanup, user-message），负责拦截生命周期事件。
- **后台服务（Worker Service）**：基于 Express.js 和 Bun 运行的常驻进程，监听本地端口（默认 37777）。它负责异步处理 AI 压缩、管理会话状态、提供 SSE 实时推送以及托管 React 编写的 Viewer UI。
- **数据层**：使用 SQLite 配合 FTS5 进行全文检索，结合 ChromaDB 进行语义向量检索，形成混合检索能力。

### Hook 架构细节
Claude-Mem 采用“神经末梢”式的架构设计，利用 Claude Code 提供的 **Lifecycle Hooks** 机制，在特定时间节点介入工作流：
- **Hook 层**：运行在 Claude Code 进程中的 6 个脚本（`smart-install.js`, `context-hook.js`, `new-hook.js`, `save-hook.js`, `summary-hook.js`, `cleanup-hook.js`），负责数据采集、预处理和指令下发。
- **Worker 层**：独立的后台服务，负责接收 Hook 发送的数据，调用 LLM 进行智能压缩，并将结果存入数据库。
- **通信模式**：所有 Hook 通过 **stdin/stdout** 与宿主环境通信。输入为序列化的 JSON 上下文数据，输出为控制指令或注入内容（如 `additionalContext`）。

### 核心设计原则
- **唯一性**：以 `session_id` 作为全局不变量和主键，确保多轮对话数据关联正确。
- **幂等性**：关键数据库操作（如创建会话）使用 `INSERT OR IGNORE`，防止重复触发导致数据冗余。
- **边缘脱敏**：隐私标签（如 `<private>`）在数据离开 Hook 进程前即被剥离，确保敏感信息不进入存储层。
- **非阻塞**：除必要的健康检查外，大部分与 Worker 的通信采用“即发即忘”模式（带超时限制），避免阻塞用户的主工作流。

### 技术选型优势
- **Bun 运行时**：替代了早期的 PM2+Node.js 方案，利用 `bun:sqlite` 获得更高的性能和更低的冷启动时间，且无需额外依赖。
- **零基础设施依赖**：摒弃 Redis 或 PostgreSQL，仅依赖单机即可运行的 SQLite，极大降低了部署门槛。
- **即发即忘（Fire-and-Forgert）通信**：Hook 脚本向 Worker 发送 HTTP 请求后立即返回，避免阻塞用户的编码流程，解决了 AI 处理耗时与 Hook 超时限制之间的矛盾。

### 隐私与安全
系统引入了 `<private>` 标签机制。用户在提示词中包裹在此标签内的内容（如 API Key）会在进入 Worker 前的边缘层被自动剥离，确保敏感信息永不落盘。同时，系统使用 `<claude-mem-context>` 标签标记注入的历史上下文，防止其被二次压缩存储，避免了“记忆污染”的递归问题。

### 项目现状
由 Alex Newman (@thedotmack) 开发，遵循 AGPL-3.0 协议。当前版本为 v10.6.2，GitHub Stars 超过 41.5k，已成为增强 Claude Code 生产力的重要工具。

## 来源
- [[raw/articles/claude-mem/blog_01_overview.md]]

## 相关
- [[Claude Code]]
- [[LLM Statelessness]]
- [[Bun Runtime]]
- [[SQLite]]
- [[ChromaDB]]
- [[Alex Newman]]