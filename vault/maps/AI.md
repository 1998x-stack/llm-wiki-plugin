---
type: map
topic: "AI"
page_count: 62
updated: 2026-04-15
---

# AI

## 概念

- [[Codex TUI]] — [[Codex CLI]] 的"驾驶舱"——不是简单的 REPL，而是一个**事件驱动状态机**，承担实时审批、diff 预览、会话导航、多 Agent 状态展示等功能。 (confidence: 0.9)
- [[Codex会话管理器]] — [[Codex CLI]] 的上下文持久化层，解决 LLM 天然无状态与工程任务有状态之间的矛盾。通过 Session 持久化、Transcript 存储和 Resume 机制，将 Agent 变成"有记忆的协作者"。 (confidence: 0.9)
- [[Codex多Agent调度]] — [[Codex CLI]] 的并行任务执行系统，让 Codex 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。 (confidence: 0.9)
- [[Codex沙箱系统]] — [[Codex CLI]] 的执行边界层，用**操作系统内核级机制**限制 Agent 能触碰的文件系统范围和网络权限。即使 LLM 生成了恶意命令，沙箱在内核层强制拦截。 (confidence: 0.9)
- [[Codex配置系统]] — [[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。 (confidence: 0.9)
- [[ExecPolicy]] — [[Codex CLI]] 的命令审批引擎：将"哪些命令允许、哪些需要审批、哪些禁止"变成可版本化、可测试、可共享的**策略声明文件**。 (confidence: 0.9)
- [[MCP协议层]] — [[Codex CLI]] 的工具连接协议层。MCP（Model Context Protocol）是 Anthropic 提出的开放协议，让工具与 Agent 解耦。 (confidence: 0.9)
- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和 (confidence: 0.85)
- [[AI设计推理层]] — AI 设计推理层是一种在 AI 助手生成 UI 代码**之前**插入专业设计决策过程的架构模式：通过知识库驱动的检索+推理，将用户的自然语言请求转化为产品类型专 (confidence: 0.88)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La (confidence: 0.9)
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `tool (confidence: 0.92)
- [[Claude-Code-Hook-System]] — Claude Code Hook System 是 Claude Code 编程助手提供的一种扩展机制，允许开发者通过编写脚本拦截和响应 AI 会话的生命周期事 (confidence: 0.9)
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/ (confidence: 0.9)
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtoco (confidence: 0.9)
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹" (confidence: 0.9)
- [[Kinodynamic Planning]] — Kinodynamic Planning（动力学[[运动规划]]）是一类同时考虑运动学约束（如非完整约束）和动力学约束（如速度、加速度、力矩限制）的[[运动规划 (confidence: 0.9)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完 (confidence: 0.9)
- [[Legged Robots That Balance]] — 《Legged Robots That Balance》是 [[Marc H. Raibert]] 于 1986 年由 MIT Press 出版的学术专著，被视 (confidence: 1.0)
- [[Master-Overrides设计系统持久化]] — Master + Overrides 是一种解决 AI 无状态（Stateless）导致"设计失忆症"的文件架构模式：将设计决策写入项目文件系统，AI 通过读文 (confidence: 0.9)
- [[PDDL]] — PDDL（Planning Domain Definition Language，规划领域定义语言）是自动规划领域的标准建模语言，由 Drew McDermot (confidence: 0.95)
- [[Probabilistic Robotics]] — 《Probabilistic Robotics》是由 [[Sebastian Thrun]]、[[Wolfram Burgard]] 和 [[Dieter Fo (confidence: 1.0)
- [[ROS (Robot Operating System)]] — ROS（Robot Operating System）是一个开源的、模块化的机器人软件框架和元操作系统（meta-operating system），由 [[M (confidence: 1.0)
- [[RRT-Connect]] — [[快速扩展随机树 (RRT)|RRT]]-Connect 是快速扩展随机树（[[快速扩展随机树 (RRT)|RRT]]）算法的重要变体，由 [[Steven  (confidence: 0.95)
- [[STRIPS 规划器]] — STRIPS（STanford Research Institute Problem Solver）是人工智能历史上最具影响力的自动规划系统之一，由 [[Ric (confidence: 1.0)
- [[三分解控制框架]] — 三分解控制框架（Three-Part Decomposition）是由 [[Marc H. Raibert]] 提出的一种用于动态腿式运动控制的核心理论架构。该 (confidence: 1.0)
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 (confidence: 0.9)
- [[动态平衡]] — 动态平衡（Dynamic Balance）是指系统在运动过程中，通过主动控制力和力矩来维持整体稳定性，而不要求系统在每一时刻都处于静力平衡状态的一种控制模式。在 (confidence: 0.95)
- [[包容体系结构]] — 包容体系结构（Subsumption Architecture）是由 [[Rodney Brooks]] 于 1986 年提出的一种革命性机器人控制架构。它彻底 (confidence: 1.0)
- [[工程化UX规则体系]] — 工程化 UX 规则体系是将隐性设计经验编码为**带优先级标签、唯一 ID、可机器检索和自动验证的结构化规则**的方法：使 AI 能直接执行 UX 规则检查而不只 (confidence: 0.9)
- [[快速扩展随机树 (RRT)]] — 快速扩展随机树（Rapidly-Exploring Random Trees, RRT）是一种用于高维空间路径规划的采样算法，由 [[Steven M. LaV (confidence: 1.0)
- [[手眼协调]] — 手眼协调（Hand-Eye Coordination）是机器人学中的一个核心研究领域，指机器人系统整合视觉感知（眼）与机械操作（手）能力，以实现对物体的识别、定 (confidence: 0.9)
- [[构型空间方法]] — **构型空间方法（Configuration Space Approach）**，简称 **C-space 方法**，是由 [[Tomas Lozano-Per (confidence: 1.0)
- [[概率路线图 (PRM)]] — 概率路线图（Probabilistic Roadmap, [[Probabilistic Robotics|PR]]M）是一种用于高维构型空间中机器人[[运动规 (confidence: 1.0)
- [[结构化UI风格知识库]] — 结构化 UI 风格知识库是将每种 UI 视觉风格编码为**可机器检索和直接输出的结构化记录**的设计模式：除风格描述外，每条记录携带 AI Prompt 关键词 (confidence: 0.88)
- [[行业设计反模式系统]] — 行业设计反模式系统是一种**以负样本为核心**的设计知识编码方式：为每种产品类型预定义「绝对不能做什么」，使 AI 生成 UI 时能自动规避行业隐性禁忌。核心洞 (confidence: 0.9)
- [[行为机器人学]] — 行为机器人学（Behavior-based Robotics, BBR）是机器人学的一个主要研究范式，兴起于 1980 年代末，由 [[Rodney Brook (confidence: 0.95)
- [[运动规划]] — **运动规划（Motion Planning）**，又称路径规划（Path Planning），是机器人学和人工智能领域的核心问题之一。其基本任务是：给定一个机 (confidence: 0.95)

## 实体

- [[Boston Dynamics]] — Boston Dynamics 是一家世界领先的机器人工程公司，成立于 1992 年，由著名机器人学家 [[Marc H. Raibert]] 从麻省理工学院（ (confidence: 1.0)
- [[Brian Gerkey]] — Brian Gerkey 是著名的机器人学家和开源软件倡导者，**ROS **([[ROS (Robot Operating System)|Robot Ope (confidence: 0.95)
- [[Codex CLI]] — OpenAI 以 Rust 重写并开源的**本地编码 Agent**。一套把 LLM 决策与 OS 级执行边界融合的系统工程——LLM 推理引擎 + OS 级沙箱执行器 + 人机协同审批协议 + MCP 协议总线。 (confidence: 0.9)
- [[ChromaDB]] — ChromaDB 是一个开源的向量数据库（Vector Database），专为 AI/LLM 应用设计，用于存储和检索向量嵌入（Embeddings）。它支持 (confidence: 0.85)
- [[Claude-Code]] — Claude Code 是 Anthropic 官方发布的 AI 编程助手 CLI（命令行界面）工具，基于 Claude 模型（Opus/Sonnet/Haik (confidence: 0.95)
- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagen (confidence: 0.95)
- [[Dieter Fox]] — Dieter Fox 是美国华盛顿大学（University of Washington）教授，著名的机器人学和人工智能专家。他是[[Probabilistic (confidence: 0.95)
- [[Heinrich A. Ernst]] — Heinrich A. Ernst 是一位在机器人学和人工智能领域具有开创性贡献的研究者，以其 1962 年在麻省理工学院（MIT）完成的博士论文《[[MH-1 (confidence: 0.95)
- [[MH-1 机械手]] — MH-1 是由 [[Heinrich A. Ernst]] 于 1962 年在麻省理工学院（MIT）开发的世界上第一个由计算机控制并具备触觉反馈的机械手系统。作 (confidence: 0.95)
- [[Marc H. Raibert]] — Marc H. Raibert 是美国著名的计算机科学家和机器人学家，被誉为现代动态腿式机器人之父。他于 1977 年在麻省理工学院（MIT）获得博士学位，随后 (confidence: 1.0)
- [[Morgan Quigley]] — Morgan Quigley 是美国计算机科学家和机器人学家，**ROS **([[ROS (Robot Operating System)|Robot Ope (confidence: 0.95)
- [[OpenClaw]] — OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、Slack、Si (confidence: 0.85)
- [[PR2 机器人]] — **[[Probabilistic Robotics|PR]]2 **(Personal Robot 2) 是由 **[[Willow Garage]]** 开 (confidence: 0.95)
- [[Rodney Brooks]] — Rodney A. Brooks（罗德尼·布鲁克斯）是澳大利亚裔计算机科学家、机器人学家及企业家，曾任 MIT 人工智能实验室主任。他是“[[行为机器人学]]” (confidence: 1.0)
- [[Sebastian Thrun]] — Sebastian Thrun 是斯坦福大学人工智能实验室前主任，著名计算机科学家，[[Probabilistic Robotics|概率机器人学]]领域的奠基 (confidence: 1.0)
- [[Sergey-Levine]] — Sergey Levine 是 UC Berkeley 计算机科学系教授，深度机器人学习领域最具影响力的研究者之一（Google Scholar 引用超 23  (confidence: 0.95)
- [[Shakey 机器人]] — Shakey 是世界上第一个具备通用目的的移动机器人，由斯坦福研究院（SRI International）人工智能中心于 1960 年代末至 1970 年代初研 (confidence: 1.0)
- [[Steven M. LaValle]] — Steven M. LaValle 是国际知名的计算机科学家和机器人学家，现任芬兰奥卢大学（University of Oulu）教授。他以提出**快速扩展随机 (confidence: 1.0)
- [[Tomas Lozano-Perez]] — Tomas Lozano-Perez 是麻省理工学院（MIT）的终身教授，机器人学与人工智能领域的杰出科学家。他于 1983 年发表的论文《Spatial Pl (confidence: 1.0)
- [[UI-UX-Pro-Max]] — UI UX Pro Max（UUPM）是 GitHub 上 53k+ Stars 的开源 AI 设计技能包，专为 Claude Code、Cursor、Wind (confidence: 0.9)
- [[Unimate]] — Unimate 是世界上第一台投入实际应用的工业机器人，由 George Devol 发明并由 Joseph Engelberger 推广，于 1961 年首次 (confidence: 0.9)
- [[Willow Garage]] — Willow Garage 是一家成立于 2006 年的美国机器人技术孵化器，由硅谷企业家 Scott Hassan 创立。该机构致力于个人机器人技术的研发，其 (confidence: 1.0)
- [[Wolfram Burgard]] — Wolfram Burgard 是德国弗莱堡大学（University of Freiburg）教授，国际知名的机器人学专家，尤其在移动机器人导航、机器学习和[ (confidence: 0.95)

## 综合分析

- [[DeepAgents评估设计哲学]] — [[DeepAgents]] 的评估体系建立在**三条核心分离线**上，每条分离线都针对一个常见的"评估混淆陷阱"： (confidence: 0.9)
