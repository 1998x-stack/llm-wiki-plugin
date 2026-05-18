---
type: map
topic: "AI设计"
page_count: 34
updated: 2026-05-18
---

# AI设计

## 概述

AI设计 相关概念与实体的集群。核心主题：AI设计推理层、Approval Gate UI、Boolean Props 地狱、Harness 设计。

## 概念

- [[AI设计推理层]] — AI 设计推理层是一种在 AI 助手生成 UI 代码**之前**插入专业设计决策过程的架构模式：通过知识库驱动的检索+推理，将用户的自然语言请求转化为产品类型专 (confidence: 0.88)
- [[Approval Gate UI]] — Approval Gate UI 是 Agent 系统中关键的人机协同节点，将 [[ExecPolicy]] 的策略决策可视化为可操作的界面，展示待执行命令、影 (confidence: 0.75)
- [[Boolean Props 地狱]] — [[React]] 组件设计中的反模式，指组件接受过多布尔类型属性导致接口复杂、难以维护的问题。 (confidence: 0.8)
- [[Harness 设计]] — Harness 是为长时运行 AI Agent 设计的控制框架，负责状态管理、验证循环、人机协作协议和上下文持久化，本质上是"为 AI Agent 定制的 CI (confidence: 0.8)
- [[Master-Overrides设计系统持久化]] — Master + Overrides 是一种解决 AI 无状态（Stateless）导致"设计失忆症"的文件架构模式：将设计决策写入项目文件系统，AI 通过读文 (confidence: 0.9)
- [[PCA颜色增强]] — PCA颜色增强是一种数据增强技术，通过对图像 RGB 通道的主成分添加随机扰动来模拟自然光照变化，由 [[AlexNet]] 论文首次提出，可将 Top-1 错 (confidence: 0.8)
- [[Poka-Yoke 工具设计]] — Poka-Yoke 工具设计是一种 Agent 工具接口设计方法论，源自制造业防错理念，通过修改接口设计使错误在结构上无法发生，而非依赖模型"记住"正确用法。 (confidence: 0.8)
- [[React]] — ReAct (Reasoning and Acting) 是一种结合推理和行动的技术，通过交错执行 Reasoning 和 Acting 来完成任务。 (confidence: 0.7)
- [[UI系统选择规范]] — [[UrhoX引擎|UrhoX]] 有两套 UI 系统，原生 UI（Urho3D UIElement）已废弃，必须使用新 UI 系统（urhox-libs/UI (confidence: 0.9)
- [[UX设计双模式架构]] — UX设计双模式架构是一种为同一UX设计领域提供两种完全不同AI行为模式的方法，分别适用于不同的项目需求。 (confidence: 0.8)
- [[仓库]] — 在分层架构中负责数据访问的组件，为业务逻辑层提供统一的数据访问接口，封装对数据源的具体操作细节。 (confidence: 0.7)
- [[依赖注入]] — 一种设计模式，通过外部来源向对象提供其依赖项，降低组件间的耦合度，提升代码的可测试性和[[可维护性]]。 (confidence: 0.7)
- [[品牌语气一致性]] — 确保所有沟通内容都符合品牌语气和风格指南的原则，适用于营销文案、客户沟通等对外内容的撰写。 (confidence: 0.8)
- [[品牌语气示例]] — 展示品牌语气在实际应用中的具体样例，涵盖不同情境下的语言风格表现。 (confidence: 0.8)
- [[工程化UX规则体系]] — 工程化 UX 规则体系是将隐性设计经验编码为**带优先级标签、唯一 ID、可机器检索和自动验证的结构化规则**的方法：使 AI 能直接执行 UX 规则检查而不只 (confidence: 0.9)
- [[开放架构]] — 开放架构（Open Architecture）是一种系统设计哲学，强调系统的开放性、互操作性和可扩展性，允许第三方独立开发组件并与系统其他部分协同工作，这一理念 (confidence: 0.8)
- [[技术栈感知设计规则]] — 技术栈感知设计规则是一种将**同一设计决策**按不同技术栈细化为具体实现模式的知识编码方式：相同的「圆角卡片 hover 效果」在 [[React]]、Swif (confidence: 0.87)
- [[无障碍设计]] — 无障碍设计是一种确保产品、[[服务]]和环境能够被尽可能多的人使用的设计方法，特别是那些有残障的人士。 (confidence: 0.8)
- [[服务]] — 在分层架构中封装业务逻辑的组件，负责实现具体的业务功能，是应用程序的核心逻辑处理层。 (confidence: 0.7)
- [[纵深防御]] — 一种安全架构设计原则，通过多层独立[[防御机制]]确保单层突破不等于完全逃逸，每层提供不同类型的保护以应对不同攻击向量。 (confidence: 0.85)
- [[结构化UI风格知识库]] — 结构化 UI 风格知识库是将每种 UI 视觉风格编码为**可机器检索和直接输出的结构化记录**的设计模式：除风格描述外，每条记录携带 AI Prompt 关键词 (confidence: 0.88)
- [[行业色彩情绪映射]] — 行业色彩情绪映射是一种将产品类型与色彩方案通过**情绪关键词**对应起来的设计知识编码方式：颜色选择的依据不是「好看」，而是**行业惯例形成的用户信任联觉 +  (confidence: 0.88)
- [[行业设计反模式系统]] — 行业设计反模式系统是一种**以负样本为核心**的设计知识编码方式：为每种产品类型预定义「绝对不能做什么」，使 AI 生成 UI 时能自动规避行业隐性禁忌。核心洞 (confidence: 0.9)
- [[防错设计]] — 防错设计（Poka-yoke）是一种通过接口设计使常见错误在结构上不可能发生的设计方法论，在 Agent 工具设计中表现为使用具体类型、枚举值和绝对路径等手段减 (confidence: 0.8)

## 实体

- [[Guorui Zhou]] — 阿里巴巴集团阿里妈妈精准定向检索及基础算法团队的研究员，深度兴趣网络（DIN）论文的主要作者之一。 (confidence: 0.8)
- [[Ink]] — [[React]] Ink 是用于构建命令行界面(CLI)应用程序的 [[React]] 渲染器，允许使用 [[React]] 组件来创建声明式终端 UI。 (confidence: 0.8)
- [[Ink Framework]] — 基于 [[React]] 的终端 UI 渲染框架，被 [[Claude Code]] 用于构建终端界面。 (confidence: 0.8)
- [[Ratatui]] — Ratatui 是 Rust 的 TUI 渲染引擎，为 [[Codex CLI]] 等现代终端应用提供全屏 alternate screen 渲染、语法高亮 d (confidence: 0.7)
- [[UI-UX-Pro-Max]] — UI UX Pro Max（UUPM）是 [[GitHub]] 上 53k+ Stars 的开源 AI 设计[[Skills|技能]]包，专为 [[Claude (confidence: 0.9)
- [[Yanghui Yan]] — 阿里巴巴集团阿里妈妈精准定向检索及基础算法团队的研究员，深度兴趣网络（DIN）论文的作者之一。 (confidence: 0.8)
- [[Yoga]] — Yoga 是 Meta 开源的布局引擎，实现了 Flexbox 布局[[算法]]，支持约束布局，能够适配任意终端宽度。 (confidence: 0.8)
- [[bencium UX Designer]] — bencium UX Designer是一套专为[[Claude Code]]设计的UX设计[[Skills|技能]]集合，包含两个不同行为模式的AI助手，用于 (confidence: 0.8)
