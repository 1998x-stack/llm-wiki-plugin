---
type: map
topic: "Agent系统"
page_count: 64
updated: 2026-04-18
---

# Agent系统

## 概述

Agent系统 相关概念与实体的集群。核心主题：ACP 编辑器集成、ACP协议、AGENTS.md 项目约定文件、Agent Harness模式。

## 概念

- [[ACP 编辑器集成]] — Agent Communication Protocol，[[Hermes Agent|Hermes]] 与代码编辑器集成的标准协议，让 IDE 中的 Agen (confidence: 0.5)
- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和 (confidence: 0.85)
- [[AGENTS.md 项目约定文件]] — 面向 AI Agent 的项目级约定文件，在每次 Agent 会话开始时读取，定义技术栈、运行命令、代码规范、安全规则和已知问题，是 [[Agent Harne (confidence: 0.75)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La (confidence: 0.9)
- [[Agent 迭代循环]] — Agent 迭代循环是一种自主编码代理的工作模式，每个迭代周期严格实现一个 User Story：选定任务 → 实现功能 → 验证通过 → 更新进度 → Git (confidence: 0.85)
- [[Agent可组合性]] — 通过标准化协议（如 MCP）使 Agent 实例既能调用其他工具，又能将自身暴露为工具，从而在更大系统中作为可插拔节点被组合和编排的架构属性。 (confidence: 0.75)
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `tool (confidence: 0.92)
- [[Agent角色系统]] — Agent 角色系统通过配置文件定义不同角色的行为边界、关注点和输出格式，让多 Agent 协作模拟人类团队的分工协作——架构师、工程师、审查者各司其职。 (confidence: 0.75)
- [[Agent计算机接口]] — Agent 计算机接口（Agent-Computer Interface, ACI）是类比人机接口（HCI）的概念：为 L[[LM Agent]] 设计工具接口 (confidence: 0.88)
- [[Batch Runner]] — [[Hermes Agent|Hermes]] 的批量 Agent 执行工具，并行启动多个 Agent 实例收集同类型任务的完整轨迹，为 RL 训练生成大规模训 (confidence: 0.5)
- [[Clean State Protocol]] — Clean State Protocol 是[[上下文策略]]之一，要求每次 Agent 迭代结束前执行完整的状态验证检查清单（git 状态、构建、测试、prd (confidence: 0.8)
- [[Codex TUI]] — [[Codex CLI]] 的"驾驶舱"——不是简单的 REPL，而是一个**事件驱动状态机**，承担实时审批、diff 预览、会话导航、多 Agent 状态展 (confidence: 0.9)
- [[Codex会话管理器]] — [[Codex CLI]] 的上下文持久化层，解决 LLM 天然无状态与工程任务有状态之间的矛盾。通过 Session 持久化、Transcript 存储和 R (confidence: 0.95)
- [[Codex多Agent调度]] — [[Codex CLI]] 的并行任务执行系统，让 [[Codex CLI|Codex]] 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。主 Age (confidence: 0.9)
- [[Codex沙箱系统]] — [[Codex CLI]] 的执行边界层，用**[[操作系统]]内核级机制**限制 Agent 能触碰的文件系统范围和网络权限。即使 LLM 生成了恶意命令，沙 (confidence: 0.9)
- [[Codex配置系统]] — [[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。 (confidence: 0.95)
- [[Cron 调度系统]] — [[Hermes Agent|Hermes]] 内置的定时任务调度系统，支持自然语言定义任务，让 Agent 从被动响应转为主动执行。 (confidence: 0.5)
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/ (confidence: 0.9)
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtoco (confidence: 0.9)
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹" (confidence: 0.9)
- [[Dumb Zone]] — Dumb Zone 是 L[[LM Agent]] 上下文使用量超过安全阈值后进入的性能退化区域，此时模型推理质量显著下降但仍继续输出，导致 Agent 做出错 (confidence: 0.8)
- [[E2E 验证模式]] — E2E 验证模式是一组面向 Agent 开发循环的外部运行时验证方法，核心原则是"外部验证，不信任自评估"——LLM 在查看自己写的代码时极易产生确认偏误，唯一 (confidence: 0.85)
- [[ExecPolicy]] — [[Codex CLI]] 的命令审批引擎，位于 [[Codex沙箱系统]] 之前。将"哪些命令允许、哪些需要审批、哪些禁止"从硬编码逻辑中解放出来，变成**可 (confidence: 0.9)
- [[Initializer Agent]] — Initializer Agent 是 [[Ralph Loop]] 系统中仅运行一次的项目初始化代理，负责在首个 context window 内建立完整的[ (confidence: 0.8)
- [[Know Before Speaking 协议]] — [[MemPalace]] 在 `mempalace_status` 响应中注入的软约束指令，强制 AI 在回答关于人、项目或历史事件的问题前先查询记忆系统，防 (confidence: 0.5)
- [[MCP协议层]] — [[Codex CLI]] 的工具连接协议层。MCP（[[MCP|Model Context Protocol]]）是 [[Anthropic]] 提出的开放协 (confidence: 0.9)
- [[Managed Agents 架构设计]] — [[Managed-Agents|Managed Agents]] 架构是一种专为长时运行、高可靠性智能体系统设计的工程[[规范化理论|范式]]，核心思想是将" (confidence: 0.95)
- [[Memory Nudge]] — [[Hermes Agent]] 在长对话自然暂停点主动自我反思的机制，检查是否有值得保存的经验、偏好或技能，确保信息不流失。 (confidence: 0.5)
- [[Multi-Agent Orchestration]] — GSD 系统的核心架构模式，通过编排者（主会话）协调 11 个专家[[Subagents-in-Claude-Code|子智能体]]，每个[[Subagents (confidence: 0.9)
- [[Policy-First 设计]] — 一种安全架构设计哲学：**先声明策略，再执行**，而非"先执行再道歉"（act now, apologize later）。 (confidence: 0.85)
- [[Session 交接机制]] — Session 交接机制是一种跨 Agent 会话的状态传递模式，通过 prd.json（进度）、progress.txt（日记）和 AGENTS.md（经验） (confidence: 0.85)
- [[Systematic Debugging Skill]] — [[Superpowers]] 刚性技能，以"NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST"为铁律，用 4 个 (confidence: 0.9)
- [[TDD Skill]] — [[Superpowers]] 最严苛的刚性技能，以"NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST"为铁律，构 (confidence: 0.9)
- [[User Story 粒度原则]] — User Story 粒度原则规定每个 User Story 必须足够小，能在单个[[上下文窗口]]内完成，否则 LLM 会在完成前耗尽上下文导致产出质量急剧下 (confidence: 0.7)
- [[subagent-driven-development Skill]] — [[Superpowers]] 技能，通过为每个任务派遣全新子 Agent 实现计划，配合两阶段评审（规格合规性 → 代码质量），是 [[Superpowers (confidence: 0.9)
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 (confidence: 0.9)
- [[双重验证（Dual Verification）]] — 双重验证是一种防止 Agent 虚假报告完成状态的交叉验证机制，通过同时检测[[完成信号机制（Completion Signal）|完成信号]]和验证 prd. (confidence: 0.8)
- [[多Agent架构]] — 多 Agent 架构是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**子 Agent 通过各自独立[[上下文窗口]]进行并行探 (confidence: 0.92)
- [[子 Agent 卸载]] — 子 [[子 Agent 模式（Sub-Agent Pattern）|Agent 卸载]]是[[上下文策略]]之一，将消耗大量 tokens 但只需要结论的操作（ (confidence: 0.8)
- [[子 Agent 模式（Sub-Agent Pattern）]] — 子 Agent 模式是一种上下文保护策略，将昂贵的操作（测试、编译、截图）offload 给独立的子 Agent 执行，主 Agent 仅接收结论而不被执行细节 (confidence: 0.8)
- [[完成信号机制（Completion Signal）]] — 完成信号机制是 [[Agent 迭代循环]]中用于标记单次迭代结束的标准化通信协议，通过 `<promise>COMPLETE</promise>` XML 标 (confidence: 0.8)
- [[工作台 vs 长期记忆]] — 一种 AI Agent 架构心智模型：将[[上下文窗口]]视为用完即扔的临时工作台（Working Memory），将文件系统视为永久存储的长期记忆（Persi (confidence: 0.75)
- [[工具注册机制]] — [[Hermes Agent]] 的工具发现和执行分发系统，利用 Python 模块加载机制实现工具在导入时自动注册，无需手工维护工具列表。 (confidence: 0.5)
- [[技能自我改进]] — [[Hermes Agent]] 的技能在使用过程中发现问题后自动更新 [[SKILL.md 格式规范|SKILL.md]] 的机制，使技能文档随使用持续进化而 (confidence: 0.5)
- [[条件激活机制]] — [[Agent Skills|Skills]] 系统中让技能根据当前工具可用性自动显示或隐藏的机制，实现技能的条件化呈现，避免无能力执行时的界面混乱。 (confidence: 0.5)
- [[观察遮蔽]] — 观察遮蔽是[[上下文策略]]之一，当上下文接近限制时，保留最近 N 轮对话完整，将更早的消息替换为摘要占位符，从而延长单个 Session 的有效工作时间。与  (confidence: 0.75)
- [[记忆安全扫描]] — [[Hermes Agent|Hermes]] 在写入记忆前自动扫描内容的安全机制，防止凭证泄露、指令注入和过大条目写入记忆系统。 (confidence: 0.7)
- [[记忆工具]] — [[Hermes Agent]] 管理 [[语义记忆|MEMORY.md]] 的内置工具，支持 add、replace、remove 三种操作，采用子字符串匹配 (confidence: 0.7)
- [[迭代预算]] — [[Hermes Agent]] 防止无限循环的安全机制，通过跟踪迭代次数、Token 消耗和工具调用次数，在任一指标超阈值时优雅终止循环。 (confidence: 0.5)
- [[闭环学习系统]] — AI Agent 在执行任务后自动学习、改进并沉淀经验的机制，使 Agent 越用越聪明，而非每次从同一基线出发。 (confidence: 0.7)
- [[零 LLM 调用内存层]] — AI 记忆系统的架构设计原则：在内存的写入和读取过程中不调用任何 LLM，所有分类、检测、压缩操作通过确定性算法（正则表达式、关键词评分）完成。 (confidence: 0.5)

## 实体

- [[Claude-Code]] — [[Claude Code]] 是 [[Anthropic]] 官方发布的 AI 编程助手 CLI（命令行界面）工具，基于 Claude 模型（Opus/Son (confidence: 0.95)
- [[Claude-Mem]] — Claude-Mem 是一个专为 **[[Claude Code]]** 设计的开源持久化记忆插件，旨在解决大型语言模型（LLM）固有的“无状态”缺陷。通过自动 (confidence: 1.0)
- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagen (confidence: 0.95)
- [[Goose]] — Goose 是由 Block（Jack Dorsey 旗下公司）开源的通用 AI Agent CLI 工具，定位为不限于编程的通用自动化平台。支持多后端模型（含 (confidence: 0.8)
- [[Hermes Agent]] — 由 [[Nous Research]] 开源的自我进化 AI 代理框架，内置学习闭环，支持 200+ 模型、14+ 消息平台接入，可在任意 VPS 或云端持续运 (confidence: 0.7)
- [[Manus]] — Manus 是一款面向通用任务的 AI Agent 产品，由创始团队从 NLP 领域创业经验出发，选择基于前沿模型的上下文学习能力构建而非训练端到端智能体模型。 (confidence: 0.85)
- [[OpenClaw]] — OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、Slack、Si (confidence: 0.85)
- [[Pi-Agent]] — Pi Agent 是由 [[Mario-Zechner]] 创建的极简 AI 编程代理工具包（[[TypeScript]] Monorepo），以 4 个工具  (confidence: 0.95)
- [[SWE-agent]] — SWE-agent 是由 Princeton 团队（2024）开发的 AI Agent 系统，能将 LLM 转化为软件工程师，自动修复 GitHub 仓库中的真 (confidence: 0.85)

## 综合分析

- [[DeepAgents评估设计哲学]] — ## 洞见 (confidence: 0.9)
