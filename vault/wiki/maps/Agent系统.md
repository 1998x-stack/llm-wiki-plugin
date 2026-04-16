---
type: map
topic: "Agent系统"
page_count: 23
updated: 2026-04-16
---

# Agent系统

## 概念

- [[ACP协议]] — **Agent Client Protocol（ACP）** 是一种标准化的"客户端—智能体"通信协议，定义客户端如何与 AI Agent 进行会话、工具调用和
- [[AIXI模型]] — AIXI 是 Marcus Hutter (2000) 提出的通用人工智能理论模型，将 Solomonoff 归纳推理与 Bellman 最优控制结合，在任何可
- [[Agent Harness模式]] — **Agent Harness**（"马具"）是一种 AI Agent 工程架构模式：**不**从零实现 Agent 运行时，而是在现有 LLM 框架（如 La
- [[Agent Skills]] — Agent Skills（代理技能）是 Anthropic 提出的开放标准：**一个含 SKILL.md 文件的目录**，通过渐进式披露机制为 Agent 提供
- [[Agent工作流模式]] — Anthropic 从与数十个客户团队协作中提炼的 LLM 系统架构分类：**工作流**（LLM 和工具经由预定义代码路径编排）与**Agent**（LLM 动
- [[Agent循环]] — Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳：反复调用 LLM，根据停止原因分支——若 `stop` 则输出结果，若 `tool
- [[Agent计算机接口]] — Agent 计算机接口（Agent-Computer Interface, ACI）是类比人机接口（HCI）的概念：为 LLM Agent 设计工具接口需要与 
- [[Agent评估方法论]] — Anthropic 从内部实践和客户协作中提炼的 Agent 系统评估（Eval）系统方法论：词汇体系、评分器类型、能力评估与回归评估、pass@k vs pa
- [[DeepAgents中间件体系]] — [[DeepAgents]] [[ROS (Robot Operating System)|中间件]]（`libs/deepagents/deepagents/
- [[DeepAgents后端协议]] — [[DeepAgents]] 的存储与执行抽象层（`libs/deepagents/deepagents/backends/`）。`BackendProtoco
- [[DeepAgents评估体系]] — [[DeepAgents]] 的评估框架（`libs/evals/`），基于 pytest + LangSmith，将 Agent 一次运行表示为结构化"轨迹"
- [[Kinodynamic Planning]] — Kinodynamic Planning（动力学[[运动规划]]）是一类同时考虑运动学约束（如非完整约束）和动力学约束（如速度、加速度、力矩限制）的[[运动规划
- [[LLM-as-Judge]] — 使用 LLM 作为自动评判器（Judge），对 AI 系统的输出按预定义**准则**打分，代替人工评估。适用于难以用规则/子串匹配表达的**语义正确性、风格、完
- [[STRIPS 规划器]] — STR[[逆倾向评分|IPS]]（STanford Research Institute Problem Solver）是人工智能历史上最具影响力的自动规划系统
- [[三分解控制框架]] — 三分解控制框架（Three-Part Decomposition）是由 [[Marc H. Raibert]] 提出的一种用于动态腿式运动控制的核心理论架构。该
- [[事件驱动Agent架构]] — 事件驱动 Agent 架构是指：Agent 循环内所有状态变化都通过**事件发射（emit）**通知订阅者，而不依赖返回值。同一 Agent 核心可同时驱动终端
- [[多Agent架构]] — 多 Agent 架构是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**子 Agent 通过各自独立上下文窗口进行并行探索，再将
- [[生成器-评估器架构]] — 受 GAN（生成对抗网络）启发的多 Agent 设计模式：**生成器（Generator）**负责产出，**评估器（Evaluator）**负责评判并给出详细批
- [[长时任务Agent设计]] — 针对跨多个上下文窗口的长时自主任务（数小时至数日）的 [[Agent Harness模式|Agent Harness]] 设计模式：**初始化 Agent**（

## 实体

- [[DeepAgents]] — LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagen
- [[OpenClaw]] — OpenClaw 是一个多渠道 AI 助手，以 [[Pi-Agent]] 为核心引擎，支持 WhatsApp、Telegram、Discord、Slack、Si
- [[Pi-Agent]] — Pi Agent 是由 [[Mario-Zechner]] 创建的极简 AI 编程代理工具包（TypeScript Monorepo），以 4 个工具 + < 

## 综合分析

- [[DeepAgents评估设计哲学]] — [[DeepAgents]] 的评估体系建立在**三条核心分离线**上，每条分离线都针对一个常见的"评估混淆陷阱"：
