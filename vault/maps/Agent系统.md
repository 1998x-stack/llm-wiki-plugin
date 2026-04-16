---
type: map
topic: "Agent系统"
page_count: 24
updated: 2026-04-16
---

# Agent系统

## 概述

Agent系统 相关概念与实体的集群。核心主题：ACP协议、Agent Harness模式、Agent Skills、Agent工作流模式。

## 概念

- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和 (confidence: 0.85)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La (confidence: 0.9)
- [[Agent Skills]] — Agent Skills（代理技能）是 Anthropic 提出的开放标准：**一个含 SKILL.md 文件的目录**，通过渐进式披露机制为 Agent 提供 (confidence: 0.92)
- [[Agent工作流模式]] — Anthropic 从与数十个客户团队协作中提炼的 LLM 系统架构分类：**工作流**（LLM 和工具经由预定义代码路径编排）与**Agent**（LLM 动 (confidence: 0.95)
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `tool (confidence: 0.92)
- [[Agent计算机接口]] — Agent 计算机接口（Agent-Computer Interface, ACI）是类比人机接口（HCI）的概念：为 LLM Agent 设计工具接口需要与  (confidence: 0.88)
- [[Agent评估方法论]] — Anthropic 从内部实践和客户协作中提炼的 Agent 系统评估（Eval）系统方法论：词汇体系、评分器类型、能力评估与回归评估、pass@k vs pa (confidence: 0.95)
- [[Codex TUI]] — [[Codex CLI]] 的"驾驶舱"——不是简单的 REPL，而是一个**事件驱动状态机**，承担实时审批、diff 预览、会话导航、多 Agent 状态展 (confidence: 0.9)
- [[Codex会话管理器]] — [[Codex CLI]] 的上下文持久化层，解决 LLM 天然无状态与工程任务有状态之间的矛盾。通过 Session 持久化、Transcript 存储和 R (confidence: 0.9)
- [[Codex多Agent调度]] — [[Codex CLI]] 的并行任务执行系统，让 [[Codex CLI|Codex]] 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。主 Age (confidence: 0.9)
- [[Codex沙箱系统]] — [[Codex CLI]] 的执行边界层，用**操作系统内核级机制**限制 Agent 能触碰的文件系统范围和网络权限。即使 LLM 生成了恶意命令，沙箱在内核 (confidence: 0.9)
- [[Codex配置系统]] — [[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。 (confidence: 0.9)
- [[Managed-Agents]] — Claude Managed Agents 是 Anthropic 在 Claude Platform 中提供的托管服务，代表用户运行长周期 Agent。它通过 (confidence: 0.95)
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 (confidence: 0.9)
- [[会话日志]] — 会话日志是存在于 Claude [[上下文窗口]]之外的持久化上下文对象，以追加式事件流记录所有发生的事件。与压缩或裁剪等不可逆的上下文决策不同，会话日志保证上 (confidence: 0.9)
- [[元控制框架]] — 元控制框架是一种不预设特定控制框架实现的系统设计模式，通过定义通用接口来容纳多种不同的 harness，使系统能随模型智能的提升而适配不同的控制框架需求。 (confidence: 0.95)
- [[多Agent架构]] — 多 Agent 架构是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**子 Agent 通过各自独立[[上下文窗口]]进行并行探 (confidence: 0.92)
- [[宠物与牲畜模式]] — 宠物与牲畜模式是云计算中的基础设施管理范式：宠物是有名字、需人工照料、不可丢失的个体；牲畜是无名、可互换、失败时直接替换的群体。在 Agent 架构设计中，该模 (confidence: 0.9)
- [[生成器-评估器架构]] — 受 GAN（生成对抗网络）启发的多 Agent 设计模式：**生成器（Generator）**负责产出，**评估器（Evaluator）**负责评判并给出详细批 (confidence: 0.95)
- [[结构化笔记法]] — 结构化笔记法（Structured Note-taking）是 Agent 长时任务中的持久记忆技术：Agent 将关键信息**定期写入[[上下文窗口]]之外的 (confidence: 0.88)
- [[脑手分离架构]] — 脑手分离架构是将 Agent 的"大脑"（Claude 及其控制框架）与"手"（沙箱和执行工具）及"会话"（事件日志）解耦的设计模式，使各组件可独立失败、替换和 (confidence: 0.95)
- [[长时任务Agent设计]] — 针对跨多个[[上下文窗口]]的长时自主任务（数小时至数日）的 [[Agent Harness模式|Agent Harness]] 设计模式：**初始化 Agen (confidence: 0.9)

## 实体

- [[Codex CLI]] — OpenAI 以 Rust 重写并开源的**本地编码 Agent**。不是聊天机器人，而是一套把 LLM 决策与 OS 级执行边界融合的系统工程——运行在本地终 (confidence: 0.9)
- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagen (confidence: 0.95)
