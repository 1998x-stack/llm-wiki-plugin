---
type: map
topic: "AI工程"
page_count: 42
updated: 2026-04-16
---

# AI工程

## 概述

AI工程 相关概念与实体的集群。核心主题：AI 产品积分系统设计、AI 原生架构、Advisor Tool（顾问工具）、Agent Skills。

## 概念

- [[AI 产品积分系统设计]] — AI 产品（Manus、v0.dev、Lovable、Bolt、Cursor、Replit、Builder.io 等）采用的积分/Credits 定价体系深度分 (confidence: 0.8)
- [[AI 原生架构]] — 一种优先为 AI Agent 而非人类用户设计的软件架构理念，主张 GUI 不适合 AI（图形界面是给人用的，AI 更适合直接调接口），产品应面向「Agent  (confidence: 0.75)
- [[Advisor Tool（顾问工具）]] — Anthropic Claude API 的 Advisor 模式是一种服务端多模型协作机制，允许在单次 HTTP 请求内部由廉价模型（Sonnet/Haiku (confidence: 0.8)
- [[Agent Skills]] — Agent Skills（代理技能）是 Anthropic 提出的开放标准：**一个含 SKILL.md 文件的目录**，通过渐进式披露机制为 Agent 提供 (confidence: 0.92)
- [[Agent工作流模式]] — Anthropic 从与数十个客户团队协作中提炼的 LLM 系统架构分类：**工作流**（LLM 和工具经由预定义代码路径编排）与**Agent**（LLM 动 (confidence: 0.95)
- [[Agent评估方法论]] — Anthropic 从内部实践和客户协作中提炼的 Agent 系统评估（Eval）系统方法论：词汇体系、评分器类型、能力评估与回归评估、pass@k vs pa (confidence: 0.95)
- [[Checkpoints 与 Rewind]] — Checkpoints 保存 Claude Code 对话状态快照（消息、文件修改、工具使用历史、会话上下文），让用户可以回退到之前的时间点，安全地试验和探索多 (confidence: 0.8)
- [[Claude Code 插件系统]] — 插件是 Claude Code 最高级别的扩展方式，将 slash commands、subagents、MCP servers 和 hooks 打包成可安装的 (confidence: 0.85)
- [[Claude Code 权限模式]] — 权限模式控制 Claude Code 可以执行哪些操作，从完全交互式到完全自动化，提供 6 种权限级别：default、acceptEdits、plan、aut (confidence: 0.8)
- [[Claude Code 记忆系统]] — Memory 系统让 Claude Code 在不同会话之间保留上下文。用户可将团队规范、项目规则、个人偏好和目录级约束写进 `CLAUDE.md`，Claud (confidence: 0.85)
- [[Code-Review-for-Claude-Code]] — Code Review 是 Claude Code 推出的多智能体代码审查系统，为每个 PR 派遣一组智能体进行深度审查，捕捉人类审核者容易遗漏的漏洞。目前面向 (confidence: 0.95)
- [[Context-Engineering]] — Context Engineering（上下文工程）是指对 LLM 的有限[[上下文窗口]]进行策展与管理的系统化方法。Anthropic 将其定义为：在固定  (confidence: 0.92)
- [[FTS5]] — FTS5（Full-Text Search version 5）是 [[SQLite]] 的内置全文搜索扩展模块，提供高效的文本索引和检索能力。在 [[Clau (confidence: 0.85)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完 (confidence: 0.9)
- [[Sprint合约制]] — Sprint 合约制是[[生成器-评估器架构]]三 Agent 系统中的一个机制：在每个 Sprint 开始前，**生成器（Generator）和评估器（Eva (confidence: 0.88)
- [[Subagents-in-Claude-Code]] — Subagents（子智能体）是 Claude Code 中的独立代理实例，拥有自己的上下文窗口。主代理可以派遣子智能体处理独立任务，子智能体完成后仅返回相关结 (confidence: 0.92)
- [[Think工具]] — Think 工具是一个无副作用的特殊工具：模型调用它时，输入文本被追加到日志中作为"思考"，不获取新信息，不修改任何状态。它为模型在复杂工具链中提供一个**结构 (confidence: 0.9)
- [[Wide-Research]] — Wide Research（广泛研究）是 [[Manus]] 推出的架构范式，通过并行启动多个专用子代理来解决上下文窗口限制导致的"编造阈值"问题。每个子代理都 (confidence: 0.88)
- [[上下文压缩（Context Compaction）]] — Claude Code 的上下文压缩功能（`/compact` 命令）将长对话压缩成精简摘要，释放上下文窗口空间，同时保留关键信息和任务连续性。 (confidence: 0.8)
- [[上下文漂移]] — AI 辅助开发中的行业通病，指修改 A 功能导致 B 功能损坏的现象（"改 A 坏 B"），源于长上下文中的信息衰减和注意力分散，是 AI 编程工具面临的核心挑 (confidence: 0.7)
- [[上下文焦虑]] — 上下文焦虑（Context Anxiety）是 LLM 在长时任务中的一种失败模式：模型感知到自身接近[[上下文窗口]]限制时，会**过早包装工作、草率结束任务 (confidence: 0.9)
- [[上下文腐烂]] — 上下文腐烂（Context Rot）是指随着 LLM [[上下文窗口]]中 token 数量增加，模型从上下文中**准确召回和推理信息的能力非均匀下降**的现象 (confidence: 0.95)
- [[上下文重置]] — 上下文重置（Context Reset）是长时 Agent 任务中的一种会话管理策略：**彻底清空[[上下文窗口]]，启动全新 Agent**，通过精心设计的* (confidence: 0.9)
- [[会话分支（Branching）]] — Claude Code 的会话分支功能允许从当前对话创建新会话分支（`/branch`，v2.1.77 中 `/fork` 更名为 `/branch`），保留完 (confidence: 0.75)
- [[分层记忆架构]] — 分层记忆架构（Hierarchical Memory Architecture）是 [[Context-Engineering]] 的核心实现模式。将 LLM  (confidence: 0.9)
- [[即时上下文检索]] — 即时上下文检索（Just-in-Time Context Retrieval）是一种 Agent 信息管理策略：Agent **不在运行前预加载所有可能相关的数 (confidence: 0.9)
- [[情境化检索]] — 情境化检索（Contextual Retrieval）是 Anthropic 提出的 [[检索增强生成|RAG]] 增强方案：在将文档 Chunk 建立[[Em (confidence: 0.95)
- [[斜杠命令（Slash Commands）]] — Claude Code 中用户手动触发的快捷操作，分为四类：内置命令（55+ 个）、Skills（自定义命令）、插件命令（来自已安装插件）和 MCP promp (confidence: 0.85)
- [[检索增强生成]] — 检索增强生成（Retrieval-Augmented Generation, RAG）是一种通过检索外部知识库中的相关信息并注入提示，来弥补 LLM 静态训练知 (confidence: 0.95)
- [[检索重排序]] — 检索重排序（Retrieval Reranking）是 [[检索增强生成|RAG]] 流水线中的精排步骤：在初始召回（粗排）获得大量候选 Chunk 后，用专门 (confidence: 0.9)
- [[注意力预算]] — 注意力预算（Attention Budget）是对 [[Transformer架构|Transformer]] 模型处理上下文时有限注意力资源的比喻性描述：每个 (confidence: 0.9)
- [[渐进式披露（Progressive Disclosure）]] — Claude Code Skills 的上下文管理策略——不一次性把所有内容塞进上下文，而是按需分三层加载：先看描述判断相关性，再加载 SKILL.md 核心说 (confidence: 0.8)
- [[生成器-评估器架构]] — 受 GAN（生成对抗网络）启发的多 Agent 设计模式：**生成器（Generator）**负责产出，**评估器（Evaluator）**负责评判并给出详细批 (confidence: 0.95)
- [[结构化笔记法]] — 结构化笔记法（Structured Note-taking）是 Agent 长时任务中的持久记忆技术：Agent 将关键信息**定期写入[[上下文窗口]]之外的 (confidence: 0.88)
- [[长时任务Agent设计]] — 针对跨多个[[上下文窗口]]的长时自主任务（数小时至数日）的 [[Agent Harness模式|Agent Harness]] 设计模式：**初始化 Agen (confidence: 0.9)

## 实体

- [[Aider]] — Aider 是由 Paul Gauthier 开源的 Git 原生 AI 结对编程 CLI 工具，支持 Claude、GPT-4o、Gemini 及本地模型。以 (confidence: 0.9)
- [[Cara-Phillips]] — Cara Phillips 是 Anthropic 的技术作家，专注于多智能体系统架构和协调模式的研究和撰写。2026 年发表《Multi-agent coor (confidence: 0.85)
- [[Chris-Olah]] — Chris Olah 是 Anthropic 的联合创始人之一。提出生成式 AI 系统是"培育"（grown）而非单纯"构建"（built）而成的观点，强调研究 (confidence: 0.85)
- [[TapTap Maker]] — TapTap 旗下的 AI 原生游戏开发工具（TTM），专为 AI 设计的游戏引擎，支持组件化开发、技能库系统，已支持 30 万行中型游戏，具备开发-发布全闭环 (confidence: 0.75)
- [[嗒啦啦]] — TapTap 旗下的 AI 创作助手/工具，注重拟人化设计以提升创作愉悦感和陪伴感，不是冷冰冰的工具，与 TapTap Maker 同属 TapTap AI 游 (confidence: 0.65)
- [[黎叔]] — TapTap Maker（TTM）产品负责人，嗒啦啦项目核心人物，主张 AI 原生游戏开发工具设计理念，认为 GUI 不适合 AI、应优先为 Agent 设计架 (confidence: 0.7)

## 综合分析

- [[Claude-Code上下文工程全景]] — ## 综合洞见 (confidence: 0.92)
