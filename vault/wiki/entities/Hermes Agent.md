---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: ["ai-agent", "open-source", "self-improving", "nous-research", "Agent系统"]
aliases: [Hermes, Hermes Agent Framework]
relates_to:
  - Nous Research
  - 闭环学习系统
  - 跨会话记忆
  - 开放技能标准
  - 模型无关设计
  - Honcho
  - Atropos
  - 分层记忆系统
  - 冻结快照模式
  - 记忆工具
  - 情节记忆
  - 语义记忆
  - 记忆安全扫描
  - 渐进式加载
  - 条件激活机制
  - SKILL.md 格式规范
  - 程序性记忆
  - OpenClaw
  - 三层分离架构
  - 同步编排引擎
  - 迭代预算
  - 上下文压缩
  - Prompt 缓存
  - 工具注册机制
  - 三种 API 模式
  - Gateway 消息网关
  - 平台适配器模式
  - 会话持久化
  - DM 配对授权
  - Cron 调度系统
  - ACP 编辑器集成
  - 消息镜像同步
  - 生命周期 Hooks
  - 技能自我改进
  - SOUL.md 人格系统
  - 辩证推理
  - Memory Nudge
  - 轨迹压缩
  - Batch Runner
  - Plastic Labs
supersedes: null
---

# Hermes Agent

## 概述
由 [[Nous Research]] 开源的自我进化 AI 代理框架，内置学习闭环，支持 200+ 模型、14+ 消息平台接入，可在任意 VPS 或云端持续运行。

## 关键内容
- **核心定位**：内置学习闭环的自我进化 AI 代理，非传统无状态聊天机器人，而是持续运行的自主代理
- **设计哲学**：未来最有价值的 AI Agent 是积累了最多经验、能够持续自我改进的那个，而非拥有最大模型或最复杂提示词的那个
- **六大核心能力**：[[闭环学习系统]]、随处运行（6 种执行后端）、无处不在（14+ 消息平台 [[网关与路由器|Gateway]] 接入）、模型无关（200+ 模型可切换）、[[开放技能标准]]（[[agentskills.io]] 规范）、研究就绪（批量轨迹生成 + [[Atropos]] RL 环境）
- **执行模型差异**：传统 Agent 为"接收任务→执行→返回结果→状态清零"，Hermes 为"执行→学习→改进→下次执行更好→循环"
- **记忆与技能**：[[SQLite]] + FTS5 跨[[会话持久化]]记忆，成功工作流自动转化为 [[SKILL.md 格式规范|SKILL.md]] 文件存入技能库，技能在使用中持续自我改进
- **运行环境**：支持 Local、Docker、SSH、Daytona、Singularity、Modal 六种终端执行后端，从笔记本到 HPC 全覆盖
- **安装部署**：60 秒一键安装，支持 Linux、macOS、WSL2，通过 `hermes setup` 交互式向导配置
- **四层记忆体系**：[[语义记忆]]（[[语义记忆|MEMORY.md]]，2,200 字符固定）、用户模型（USER.md，1,375 字符固定）、[[情节记忆]]（[[FTS5|SQLite FTS5]] 按需召回无上限）、[[辩证推理|辩证用户建模]]（[[Honcho]] 跨会话动态更新），总固定 Token 成本仅约 1,300
- **[[冻结快照模式]]**：会话开始时加载 [[语义记忆|MEMORY.md]] + USER.md 为冻结快照注入 System Prompt，会话期间写入磁盘但不更新 Prompt，保护 KV Cache [[KV 缓存命中率|前缀缓存]]
- **记忆安全**：写入记忆前自动扫描凭证泄露、指令注入和过大条目，防止敏感信息持久化
- **[[三层分离架构]]**：入口层（CLI/[[网关与路由器|Gateway]]/ACP/[[Batch Runner]]）→ 核心层（AIAgent ~9,200 行）→ 持久化层（[[SQLite]] + FTS5）+ 执行后端层（Terminal 6/Browser 5/Web 4/MCP），入口统一但不耦合
- **[[同步编排引擎]]**：AIAgent 是单线程同步循环而非异步事件驱动，简化状态管理，多任务通过子 Agent 委派解决
- **[[迭代预算]]**：跟踪迭代次数、Token 消耗、工具调用次数，任一超阈值时优雅终止，防止无限循环
- **[[三种 API 模式]]**：chat_completions（200+ 模型兼容最广）、codex_responses（[[OpenAI]] 新格式）、anthropic_messages（Claude 原生支持 [[提示词缓存|Prompt Caching]]/[[扩展思维|Extended Thinking]]），`hermes model` 运行时动态切换
- **工具体系**：48 工具 + 40 工具集，工具在导入时通过 `@register_tool` 自动注册，支持按需启用/禁用
- **Prompt 组装**：[[SOUL.md 人格系统|SOUL.md]] → [[语义记忆|MEMORY.md]] → USER.md → [[Agent Skills|Skills]] Level 0 (~3k tokens) → Context Files → Active Tools → Date/Time → Platform Metadata
- **[[上下文压缩]]**：会话历史接近窗口上限时 `context_compressor.py` 自动触发，辅助 LLM 递增压缩最早最冗余的工具输出
- **[[Prompt 缓存]]**：`prompt_caching.py` 为 [[Anthropic]] 模式实现[[KV 缓存命中率|前缀缓存]]，标记稳定前缀（SOUL+MEMORY+USER），长期运行累积节省可观
- **代码规模**：核心文件总计超过 36,000 行（run_agent.py ~9,200、cli.py ~8,500、gateway/run.py ~7,500、hermes_cli/main.py ~5,500），测试 3,000+，是成熟工程项目
- **三条数据流**：CLI 会话（终端输入→AIAgent→[[SQLite]] 持久化）、[[网关与路由器|Gateway]] 消息（平台消息→授权验证→AIAgent→发回响应）、Cron 定时任务（调度器→独立 AIAgent→投递目标平台）
- **学习飞轮**：会话 1 学习环境和用户偏好 → 会话 5 发现重复模式创建第一个技能 → 会话 10 技能被复用并自我改进 → 会话 50 已有 15+ 技能，同类型任务速度提升 3-5x → 持续运行成为专属 AI，复利增长
- **技能创建触发条件**：任务步骤数≥4、有明确验证步骤、有易出错关键步骤、用户显式要求记录、同类型任务历史出现≥2 次、涉及特定工具非显而易见用法、任务是通用模式而非本次特有
- **[[Memory Nudge]] 机制**：Agent 在长对话自然暂停点主动自我反思，检查是否有值得保存的环境事实、用户偏好、可复用工作流、技能问题或错误认知纠正
- **安全边界**：[[记忆安全扫描]]（凭证拦截、指令注入防护、大小限制）、命令执行授权（危险模式需用户批准）、容器隔离（Docker/Singularity 命名空间隔离）、凭证过滤（工具执行结果返回 LLM 前过滤敏感信息）

## 来源
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本，MIT License，GitHub Stars 17,000+，贡献者 207+
- [NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) — 2026 年 4 月版本，Hermes Agent 深度解析第四篇：Skills 系统
- [02_hermes_architecture.md](/raw/articles/ai-tools/hermes/02_hermes_architecture.md) — Hermes Agent 深度解析系列第二篇：三层架构与 AIAgent 核心循环
- [05_hermes_gateway.md](/raw/articles/ai-tools/hermes/05_hermes_gateway.md) — Hermes Agent 深度解析第五篇：Gateway 消息网关，2026 年 4 月版本
- [06_hermes_learning_loop.md](/raw/articles/ai-tools/hermes/06_hermes_learning_loop.md) — Hermes Agent 深度解析第六篇：闭环学习引擎，技能创建/改进、Honcho 用户建模、RL 训练

## 相关
- [[Nous Research]] — extends
- [[闭环学习系统]] — implements
- [[跨会话记忆]] — implements
- [[开放技能标准]] — implements
- [[模型无关设计]] — implements
- [[Honcho]] — uses
- [[Atropos]] — uses
- [[自我进化代理]] — part_of
- [[分层记忆系统]] — implements
- [[冻结快照模式]] — implements
- [[记忆工具]] — implements
- [[情节记忆]] — implements
- [[语义记忆]] — implements
- [[记忆安全扫描]] — implements
- [[渐进式加载]] — implements
- [[条件激活机制]] — implements
- [[SKILL.md 格式规范]] — implements
- [[程序性记忆]] — implements
- [[OpenClaw]] — compares_to
- [[三层分离架构]] — implements
- [[同步编排引擎]] — implements
- [[迭代预算]] — implements
- [[上下文压缩]] — implements
- [[Prompt 缓存]] — implements
- [[工具注册机制]] — implements
- [[三种 API 模式]] — implements
- [[Gateway 消息网关]] — implements
- [[平台适配器模式]] — implements
- [[会话持久化]] — implements
- [[DM 配对授权]] — implements
- [[Cron 调度系统]] — implements
- [[ACP 编辑器集成]] — implements
- [[消息镜像同步]] — implements
- [[生命周期 Hooks]] — implements
- [[技能自我改进]] — implements
- [[SOUL.md 人格系统]] — implements
- [[辩证推理]] — uses
- [[Memory Nudge]] — implements
- [[轨迹压缩]] — implements
- [[Batch Runner]] — implements
- [[Plastic Labs]] — uses
