---
type: map
topic: "Agent系统"
page_count: 25
updated: 2026-04-16
---

# Agent系统

## 概述

Agent系统 相关概念与实体的集群。核心主题：ACP协议、Agent Harness模式、Agent-Teams-Pattern、Agent循环。

## 概念

- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和 (confidence: 0.85)
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La (confidence: 0.9)
- [[Agent-Teams-Pattern]] — 智能体团队（Agent Teams）是当工作被分解为可长期独立执行的并行子任务时采用的多智能体模式。与协调器 - 子代理模式不同，团队成员在多次任务分配中持续运 (confidence: 0.85)
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `tool (confidence: 0.92)
- [[Agent计算机接口]] — Agent 计算机接口（Agent-Computer Interface, ACI）是类比人机接口（HCI）的概念：为 LLM Agent 设计工具接口需要与  (confidence: 0.88)
- [[Codex TUI]] — [[Codex CLI]] 的"驾驶舱"——不是简单的 REPL，而是一个**事件驱动状态机**，承担实时审批、diff 预览、会话导航、多 Agent 状态展 (confidence: 0.9)
- [[Codex会话管理器]] — [[Codex CLI]] 的上下文持久化层，解决 LLM 天然无状态与工程任务有状态之间的矛盾。通过 Session 持久化、Transcript 存储和 R (confidence: 0.9)
- [[Codex多Agent调度]] — [[Codex CLI]] 的并行任务执行系统，让 [[Codex CLI|Codex]] 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。主 Age (confidence: 0.9)
- [[Codex沙箱系统]] — [[Codex CLI]] 的执行边界层，用**操作系统内核级机制**限制 Agent 能触碰的文件系统范围和网络权限。即使 LLM 生成了恶意命令，沙箱在内核 (confidence: 0.9)
- [[Codex配置系统]] — [[Codex CLI]] 的"神经系统"，控制每一个可调行为。不是简单的配置文件，而是一个**多层继承、可版本化、环境感知**的配置管理体系。 (confidence: 0.9)
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/ (confidence: 0.9)
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtoco (confidence: 0.9)
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹" (confidence: 0.9)
- [[ExecPolicy]] — [[Codex CLI]] 的命令审批引擎，位于 [[Codex沙箱系统]] 之前。将"哪些命令允许、哪些需要审批、哪些禁止"从硬编码逻辑中解放出来，变成**可 (confidence: 0.9)
- [[Generator-Verifier-Pattern]] — 生成器 - 验证器（Generator-Verifier）是最简单的多智能体模式，也是应用最广泛的模式。生成器接收任务并生成初始输出，验证器检查输出是否符合标准 (confidence: 0.85)
- [[MCP协议层]] — [[Codex CLI]] 的工具连接协议层。MCP（Model Context Protocol）是 Anthropic 提出的开放协议，让工具与 Agent (confidence: 0.9)
- [[Message-Bus-Pattern]] — 消息总线（Message Bus）是随着智能体数量增加、交互模式变得复杂时采用的多智能体模式。引入共享通信层，智能体在该层中发布和订阅事件。新智能体具备新功能时 (confidence: 0.85)
- [[Multi-Agent-Coordination-Patterns]] — 多智能体协调模式是构建多智能体系统时的五种核心架构模式。每种模式适用于不同的场景，具有各自的优劣。选择合适模式应基于问题的结构性特征，而非追求复杂性。建议从最简 (confidence: 0.9)
- [[Orchestrator-Subagent-Pattern]] — 协调器 - 子智能体（Orchestrator-Subagent）是由层级结构定义的多智能体模式。一个智能体担任团队负责人，负责规划工作、分配任务并整合结果。子 (confidence: 0.85)
- [[Shared-State-Pattern]] — 共享状态（Shared State）是通过让智能体通过一个所有智能体都可直接读写的持久存储进行协调，从而消除中间环节的多智能体模式。智能体自主运行，可读写共享数 (confidence: 0.85)
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端 (confidence: 0.9)
- [[多Agent架构]] — 多 Agent 架构是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**子 Agent 通过各自独立[[上下文窗口]]进行并行探 (confidence: 0.92)

## 实体

- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagen (confidence: 0.95)
- [[Goose]] — Goose 是由 Block（Jack Dorsey 旗下公司）开源的通用 AI Agent CLI 工具，定位为不限于编程的通用自动化平台。支持多后端模型（含 (confidence: 0.8)

## 综合分析

- [[DeepAgents评估设计哲学]] — ## 洞见 (confidence: 0.9)
