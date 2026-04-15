---
type: map
topic: "AI"
page_count: 72
updated: 2026-04-16
---

# AI

## 概念

- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和消息流交互。[[DeepAgents]] (confidence: 0.85)
- [[AI设计推理层]] — AI 设计推理层是一种在 AI 助手生成 UI 代码**之前**插入专业设计决策过程的架构模式：通过知识库驱动的检索+推理，将用户的自然语言请求转化为产品类型专属的完整设计系统规范，再交由 AI 编码 (confidence: 0.88)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 LangGraph 的 `create_ag (confidence: 0.9)
- [[Agent Skills]] — Agent Skills（代理技能）是 Anthropic 提出的开放标准：**一个含 SKILL.md 文件的目录**，通过渐进式披露机制为 Agent 提供可组合、可共享的领域专业知识。本质是把" (confidence: 0.92)
- [[Agent工作流模式]] — Anthropic 从与数十个客户团队协作中提炼的 LLM 系统架构分类：**工作流**（LLM 和工具经由预定义代码路径编排）与**Agent**（LLM 动态决定自身流程和工具使用）的根本区别，以 (confidence: 0.95)
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `toolUse` 则执行工具并将结果注入下一轮， (confidence: 0.92)
- [[Agent计算机接口]] — Agent 计算机接口（Agent-Computer Interface, ACI）是类比人机接口（HCI）的概念：为 LLM Agent 设计工具接口需要与 HCI 同等的工程投入。工具的设计质量直 (confidence: 0.88)
- [[Agent评估方法论]] — Anthropic 从内部实践和客户协作中提炼的 Agent 系统评估（Eval）系统方法论：词汇体系、评分器类型、能力评估与回归评估、pass@k vs pass^k 非确定性指标、以及从零构建评估 (confidence: 0.95)
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/middleware/`）是 [[Age (confidence: 0.9)
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtocol` 定义统一的文件类 API，`San (confidence: 0.9)
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹"（trajectory），用**两层断言 (confidence: 0.9)
- [[Kinodynamic Planning]] — Kinodynamic Planning（动力学[[运动规划]]）是一类同时考虑运动学约束（如非完整约束）和动力学约束（如速度、加速度、力矩限制）的[[运动规划]]问题。与传统仅关注几何路径的[[运动 (confidence: 0.9)
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完整性、多条件综合**等评估目标。核心假设 (confidence: 0.9)
- [[Legged Robots That Balance]] — 《Legged Robots That Balance》是 [[Marc H. Raibert]] 于 1986 年由 MIT Press 出版的学术专著，被视为腿式机器人学领域的奠基之作。本书系统地 (confidence: 1.0)
- [[Master-Overrides设计系统持久化]] — Master + Overrides 是一种解决 AI 无状态（Stateless）导致"设计失忆症"的文件架构模式：将设计决策写入项目文件系统，AI 通过读文件获得"记忆"。全局规范存 MASTER (confidence: 0.9)
- [[PDDL]] — PDDL（Planning Domain Definition Language，规划领域定义语言）是自动规划领域的标准建模语言，由 Drew McDermott 等人于 1998 年为国际规划竞赛（ (confidence: 0.95)
- [[Probabilistic Robotics]] — 《Probabilistic Robotics》是由 [[Sebastian Thrun]]、[[Wolfram Burgard]] 和 [[Dieter Fox]] 于 2005 年出版的学术专著， (confidence: 1.0)
- [[ROS (Robot Operating System)]] — ROS（Robot Operating System）是一个开源的、模块化的机器人软件框架和元操作系统（meta-operating system），由 [[Morgan Quigley]] 等人于  (confidence: 1.0)
- [[RRT-Connect]] — [[快速扩展随机树 (RRT)|RRT]]-Connect 是快速扩展随机树（[[快速扩展随机树 (RRT)|RRT]]）算法的重要变体，由 [[Steven M. LaValle]] 和 James (confidence: 0.95)
- [[STRIPS 规划器]] — STRIPS（STanford Research Institute Problem Solver）是人工智能历史上最具影响力的自动规划系统之一，由 [[Richard E. Fikes]] 和 [[ (confidence: 1.0)
- [[Sprint合约制]] — Sprint 合约制是[[生成器-评估器架构]]三 Agent 系统中的一个机制：在每个 Sprint 开始前，**生成器（Generator）和评估器（Evaluator）先行谈判并达成合约**，明 (confidence: 0.88)
- [[Think工具]] — Think 工具是一个无副作用的特殊工具：模型调用它时，输入文本被追加到日志中作为"思考"，不获取新信息，不修改任何状态。它为模型在复杂工具链中提供一个**结构化的中间推理空间**，在 τ-Bench (confidence: 0.9)
- [[三分解控制框架]] — 三分解控制框架（Three-Part Decomposition）是由 [[Marc H. Raibert]] 提出的一种用于动态腿式运动控制的核心理论架构。该框架将复杂的高维非线性[[动态平衡]]问 (confidence: 1.0)
- [[上下文焦虑]] — 上下文焦虑（Context Anxiety）是 LLM 在长时任务中的一种失败模式：模型感知到自身接近上下文窗口限制时，会**过早包装工作、草率结束任务**，而非继续按计划执行。由 Anthropic (confidence: 0.9)
- [[上下文腐烂]] — 上下文腐烂（Context Rot）是指随着 LLM 上下文窗口中 token 数量增加，模型从上下文中**准确召回和推理信息的能力非均匀下降**的现象。由 [[ChromaDB|Chroma]] R (confidence: 0.95)
- [[上下文重置]] — 上下文重置（Context Reset）是长时 Agent 任务中的一种会话管理策略：**彻底清空上下文窗口，启动全新 Agent**，通过精心设计的**结构化交接工件（Handoff Artifac (confidence: 0.9)
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 UI、Web UI、IM 机器人等完全 (confidence: 0.9)
- [[动态平衡]] — 动态平衡（Dynamic Balance）是指系统在运动过程中，通过主动控制力和力矩来维持整体稳定性，而不要求系统在每一时刻都处于静力平衡状态的一种控制模式。在腿式机器人学中，动态平衡特指允许机器人在 (confidence: 0.95)
- [[包容体系结构]] — 包容体系结构（Subsumption Architecture）是由 [[Rodney Brooks]] 于 1986 年提出的一种革命性机器人控制架构。它彻底摒弃了传统人工智能中“感知 - 建模 - (confidence: 1.0)
- [[即时上下文检索]] — 即时上下文检索（Just-in-Time Context Retrieval）是一种 Agent 信息管理策略：Agent **不在运行前预加载所有可能相关的数据**，而是持有**轻量标识符**（文件 (confidence: 0.9)
- [[多Agent架构]] — 多 Agent 架构是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**子 Agent 通过各自独立上下文窗口进行并行探索，再将精简摘要返回给主 Agent**，从而实 (confidence: 0.92)
- [[工程化UX规则体系]] — 工程化 UX 规则体系是将隐性设计经验编码为**带优先级标签、唯一 ID、可机器检索和自动验证的结构化规则**的方法：使 AI 能直接执行 UX 规则检查而不只是「知道一些原则」。 (confidence: 0.9)
- [[快速扩展随机树 (RRT)]] — 快速扩展随机树（Rapidly-Exploring Random Trees, RRT）是一种用于高维空间路径规划的采样算法，由 [[Steven M. LaValle]] 于 1998 年提出。该算 (confidence: 1.0)
- [[情境化检索]] — 情境化检索（Contextual Retrieval）是 Anthropic 提出的 [[检索增强生成|RAG]] 增强方案：在将文档 Chunk 建立嵌入向量和 BM25 索引**之前**，用 LL (confidence: 0.95)
- [[手眼协调]] — 手眼协调（Hand-Eye Coordination）是机器人学中的一个核心研究领域，指机器人系统整合视觉感知（眼）与机械操作（手）能力，以实现对物体的识别、定位、抓取和操纵的技术与方法。该概念起源于 (confidence: 0.9)
- [[构型空间方法]] — **构型空间方法（Configuration Space Approach）**，简称 **C-space 方法**，是由 [[Tomas Lozano-Perez]] 在 1983 年系统形式化的一 (confidence: 1.0)
- [[检索增强生成]] — 检索增强生成（Retrieval-Augmented Generation, RAG）是一种通过检索外部知识库中的相关信息并注入提示，来弥补 LLM 静态训练知识不足的技术。适用于知识库超过上下文窗口 (confidence: 0.95)
- [[检索重排序]] — 检索重排序（Retrieval Reranking）是 [[检索增强生成|RAG]] 流水线中的精排步骤：在初始召回（粗排）获得大量候选 Chunk 后，用专门的**重排序模型**对每个 Chunk  (confidence: 0.9)
- [[注意力预算]] — 注意力预算（Attention Budget）是对 Transformer 模型处理上下文时有限注意力资源的比喻性描述：每个新 token 的加入都从这一"预算"中消耗一份，导致模型对任意 token (confidence: 0.9)
- [[渐进式披露-Progressive-Disclosure]] — 渐进式披露（Progressive Disclosure）是一种交互设计和信息管理策略，旨在通过分阶段、按需的方式向用户（或 AI 模型）展示信息，以避免认知过载和资源浪费。在 AI 系统设计中，该原 (confidence: 0.9)
- [[生成器-评估器架构]] — 受 GAN（生成对抗网络）启发的多 Agent 设计模式：**生成器（Generator）**负责产出，**评估器（Evaluator）**负责评判并给出详细批评，形成反馈闭环驱动质量提升。核心洞见： (confidence: 0.95)
- [[结构化UI风格知识库]] — 结构化 UI 风格知识库是将每种 UI 视觉风格编码为**可机器检索和直接输出的结构化记录**的设计模式：除风格描述外，每条记录携带 AI Prompt 关键词、CSS 变量模板、实现检查清单和反模式 (confidence: 0.88)
- [[结构化笔记法]] — 结构化笔记法（Structured Note-taking）是 Agent 长时任务中的持久记忆技术：Agent 将关键信息**定期写入上下文窗口之外的持久存储**（文件、记忆工具），在后续轮次中按需 (confidence: 0.88)
- [[行业设计反模式系统]] — 行业设计反模式系统是一种**以负样本为核心**的设计知识编码方式：为每种产品类型预定义「绝对不能做什么」，使 AI 生成 UI 时能自动规避行业隐性禁忌。核心洞察：**设计知识的精华不是「什么好看」， (confidence: 0.9)
- [[行为机器人学]] — 行为机器人学（Behavior-based Robotics, BBR）是机器人学的一个主要研究范式，兴起于 1980 年代末，由 [[Rodney Brooks]] 及其[[包容体系结构]]理论直接 (confidence: 0.95)
- [[运动规划]] — **运动规划（Motion Planning）**，又称路径规划（Path Planning），是机器人学和人工智能领域的核心问题之一。其基本任务是：给定一个机器人（或可移动物体）、一个包含障碍物的工 (confidence: 0.95)
- [[长时任务Agent设计]] — 针对跨多个上下文窗口的长时自主任务（数小时至数日）的 [[Agent Harness模式|Agent Harness]] 设计模式：**初始化 Agent**（建立环境和功能列表）+ **编码 Age (confidence: 0.9)

## 实体

- [[Boston Dynamics]] — Boston Dynamics 是一家世界领先的机器人工程公司，成立于 1992 年，由著名机器人学家 [[Marc H. Raibert]] 从麻省理工学院（MIT）离职后创办。公司总部位于美国马萨 (confidence: 1.0)
- [[Brian Gerkey]] — Brian Gerkey 是著名的机器人学家和开源软件倡导者，**ROS **([[ROS (Robot Operating System)|Robot Operating System]]) 的关键 (confidence: 0.95)
- [[ChromaDB]] — ChromaDB 是一个开源的向量数据库（Vector Database），专为 AI/LLM 应用设计，用于存储和检索向量嵌入（Embeddings）。它支持语义搜索——将文本转换为高维向量后，按语 (confidence: 0.85)
- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagents`），基于 [[LangGraph] (confidence: 0.95)
- [[Dieter Fox]] — Dieter Fox 是美国华盛顿大学（University of Washington）教授，著名的机器人学和人工智能专家。他是[[Probabilistic Robotics|概率机器人学]]领域 (confidence: 0.95)
- [[Heinrich A. Ernst]] — Heinrich A. Ernst 是一位在机器人学和人工智能领域具有开创性贡献的研究者，以其 1962 年在麻省理工学院（MIT）完成的博士论文《[[MH-1 机械手|MH-1]], A [[MH- (confidence: 0.95)
- [[MH-1 机械手]] — MH-1 是由 [[Heinrich A. Ernst]] 于 1962 年在麻省理工学院（MIT）开发的世界上第一个由计算机控制并具备触觉反馈的机械手系统。作为机器人学历史上的里程碑，MH-1 首次 (confidence: 0.95)
- [[Marc H. Raibert]] — Marc H. Raibert 是美国著名的计算机科学家和机器人学家，被誉为现代动态腿式机器人之父。他于 1977 年在麻省理工学院（MIT）获得博士学位，随后在卡内基梅隆大学（CMU）任教并创建了  (confidence: 1.0)
- [[Morgan Quigley]] — Morgan Quigley 是美国计算机科学家和机器人学家，**ROS **([[ROS (Robot Operating System)|Robot Operating System]]) 的主要 (confidence: 0.95)
- [[Nils J. Nilsson]] — Nils J. Nilsson（[[威廉·卡汉|1933-]]2019）是人工智能领域的先驱人物，斯坦福大学计算机科学系奠基性教授之一，曾任 SRI International 人工智能中心负责人。他 (confidence: 1.0)
- [[OpenClaw]] — OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、Slack、Signal、iMessage 等平台，各渠 (confidence: 0.85)
- [[PR2 机器人]] — **[[Probabilistic Robotics|PR]]2 **(Personal Robot 2) 是由 **[[Willow Garage]]** 开发的一款全尺寸移动操作机器人平台，被视为 (confidence: 0.95)
- [[Pi-Agent]] — Pi Agent 是由 [[Mario-Zechner]] 创建的极简 AI 编程代理工具包（TypeScript Monorepo），以 4 个工具 + < 1000 token 系统提示实现了与重 (confidence: 0.95)
- [[Richard E. Fikes]] — Richard E. Fikes 是一位杰出的计算机科学家，曾任斯坦福研究院（SRI International）人工智能中心的研究员，后任职于 Xerox PARC 及斯坦福大学。他最广为人知的成就 (confidence: 0.95)
- [[Rodney Brooks]] — Rodney A. Brooks（罗德尼·布鲁克斯）是澳大利亚裔计算机科学家、机器人学家及企业家，曾任 MIT 人工智能实验室主任。他是“[[行为机器人学]]”（[[行为机器人学|Behavior-b (confidence: 1.0)
- [[Sebastian Thrun]] — Sebastian Thrun 是斯坦福大学人工智能实验室前主任，著名计算机科学家，[[Probabilistic Robotics|概率机器人学]]领域的奠基人之一。他与 [[Wolfram Bur (confidence: 1.0)
- [[Sergey-Levine]] — Sergey Levine 是 UC Berkeley 计算机科学系教授，深度机器人学习领域最具影响力的研究者之一（Google Scholar 引用超 23 万次）。他与 Chelsea Finn  (confidence: 0.95)
- [[Shakey 机器人]] — Shakey 是世界上第一个具备通用目的的移动机器人，由斯坦福研究院（SRI International）人工智能中心于 1960 年代末至 1970 年代初研发。该项目旨在将感知、推理和行动统一在一 (confidence: 1.0)
- [[Steven M. LaValle]] — Steven M. LaValle 是国际知名的计算机科学家和机器人学家，现任芬兰奥卢大学（University of Oulu）教授。他以提出**快速扩展随机树（[[快速扩展随机树 (RRT)|RR (confidence: 1.0)
- [[UI-UX-Pro-Max]] — UI UX Pro Max（UUPM）是 GitHub 上 53k+ Stars 的开源 AI 设计技能包，专为 Claude Code、Cursor、Windsurf 等 AI 编程助手设计，作为「 (confidence: 0.9)
- [[Unimate]] — Unimate 是世界上第一台投入实际应用的工业机器人，由 George Devol 发明并由 Joseph Engelberger 推广，于 1961 年首次在通用汽车（General Motors (confidence: 0.9)
- [[Willow Garage]] — Willow Garage 是一家成立于 2006 年的美国机器人技术孵化器，由硅谷企业家 Scott Hassan 创立。该机构致力于个人机器人技术的研发，其最著名的成就是开发了 **ROS **( (confidence: 1.0)
- [[Wolfram Burgard]] — Wolfram Burgard 是德国弗莱堡大学（University of Freiburg）教授，国际知名的机器人学专家，尤其在移动机器人导航、机器学习和[[SLAM|同时定位与建图]]（[[SL (confidence: 0.95)

## 综合分析

- [[Claude-Code上下文工程全景]] — Claude Code 的[[Context-Engineering|上下文工程]]本质是：**在 [[LLM-Statelessness|LLM 无状态性]]约束下，把有限的 token 窗口从"聊 (confidence: 0.92)
- [[DeepAgents评估设计哲学]] — [[DeepAgents]] 的评估体系建立在**三条核心分离线**上，每条分离线都针对一个常见的"评估混淆陷阱"： (confidence: 0.9)
