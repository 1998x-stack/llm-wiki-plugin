---
type: concept
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: []
aliases: []
relates_to: []
supersedes: null
---

# AI工程

## 概念

- [[Context-Engineering]] — Context Engineering（上下文工程）是指对 LLM 的有限上下文窗口进行策展与管理的系统化方法。Anthropic 将其定义为：在固定 toke
- [[LLM-Wire-Protocol统一模式]] — [[Mario-Zechner]] 在构建 [[Pi-Agent]] 的 pi-ai 层时发现：市面上 300+ LLM 模型归根结底只实现了四种 Wire P
- [[Sprint合约制]] — Sprint 合约制是[[生成器-评估器架构]]三 Agent 系统中的一个机制：在每个 Sprint 开始前，**生成器（Generator）和评估器（Eva
- [[Think工具]] — Think 工具是一个无副作用的特殊工具：模型调用它时，输入文本被追加到日志中作为"思考"，不获取新信息，不修改任何状态。它为模型在复杂工具链中提供一个**结构
- [[上下文焦虑]] — 上下文焦虑（Context Anxiety）是 LLM 在长时任务中的一种失败模式：模型感知到自身接近上下文窗口限制时，会**过早包装工作、草率结束任务**，而
- [[上下文腐烂]] — 上下文腐烂（Context Rot）是指随着 LLM 上下文窗口中 token 数量增加，模型从上下文中**准确召回和推理信息的能力非均匀下降**的现象。由 [
- [[上下文重置]] — 上下文重置（Context Reset）是长时 Agent 任务中的一种会话管理策略：**彻底清空上下文窗口，启动全新 Agent**，通过精心设计的**结构化
- [[分层记忆架构]] — 分层记忆架构（Hierarchical Memory Architecture）是 [[Context-Engineering]] 的核心实现模式。将 LLM 
- [[即时上下文检索]] — 即时上下文检索（Just-in-Time Context Retrieval）是一种 Agent 信息管理策略：Agent **不在运行前预加载所有可能相关的数
- [[情境化检索]] — 情境化检索（Contextual Retrieval）是 Anthropic 提出的 [[检索增强生成|RAG]] 增强方案：在将文档 Chunk 建立[[Em
- [[检索增强生成]] — 检索增强生成（Retrieval-Augmented Generation, RAG）是一种通过检索外部知识库中的相关信息并注入提示，来弥补 LLM 静态训练知
- [[检索重排序]] — 检索重排序（Retrieval Reranking）是 [[检索增强生成|RAG]] 流水线中的精排步骤：在初始召回（粗排）获得大量候选 Chunk 后，用专门
- [[注意力预算]] — 注意力预算（Attention Budget）是对 [[Transformer架构|Transformer]] 模型处理上下文时有限注意力资源的比喻性描述：每个
- [[渐进式披露-Progressive-Disclosure]] — 渐进式披露（Progressive Disclosure）是一种交互设计和信息管理策略，旨在通过分阶段、按需的方式向用户（或 AI 模型）展示信息，以避免认知过
- [[结构化笔记法]] — 结构化笔记法（Structured Note-taking）是 Agent 长时任务中的持久记忆技术：Agent 将关键信息**定期写入上下文窗口之外的持久存储
- [[跨Provider上下文迁移]] — Context Handoff 是 [[Pi-Agent]] pi-ai 层最独特的能力：一个会话可以在 Anthropic → OpenAI → [[Goog

## 实体

- [[Dieter Fox]] — Dieter Fox 是美国华盛顿大学（University of Washington）教授，著名的机器人学和人工智能专家。他是[[Probabilistic
- [[Heinrich A. Ernst]] — Heinrich A. Ernst 是一位在机器人学和人工智能领域具有开创性贡献的研究者，以其 1962 年在麻省理工学院（MIT）完成的博士论文《[[MH-1
- [[Jean-Claude Latombe]] — Jean-Claude Latombe 是机器人[[运动规划]]领域的奠基人之一，曾任斯坦福大学（Stanford University）教授。他最为人熟知的成
- [[Nils J. Nilsson]] — Nils J. Nilsson（[[威廉·卡汉|1933-]]2019）是人工智能领域的先驱人物，斯坦福大学计算机科学系奠基性教授之一，曾任 SRI Inter
- [[Richard E. Fikes]] — Richard E. Fikes 是一位杰出的计算机科学家，曾任斯坦福研究院（SRI International）人工智能中心的研究员，后任职于 [[Xerox
- [[Sebastian Thrun]] — Sebastian Thrun 是斯坦福大学人工智能实验室前主任，著名计算机科学家，[[Probabilistic Robotics|概率机器人学]]领域的奠基
- [[UniMERNet]] — UniMERNet 是用于[[公式识别|数学公式识别]]的深度学习模型，可将图像中的公式检测框转换为 LaTeX 代码，是 [[MinerU]] 第四层流水线中

## 综合分析

- [[Claude-Code上下文工程全景]] — Claude Code 的[[Context-Engineering|上下文工程]]本质是：**在 [[LLM-Statelessness|LLM 无状态性]]
