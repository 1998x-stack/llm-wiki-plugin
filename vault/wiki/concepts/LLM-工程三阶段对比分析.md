---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [LLM工程, 工程方法论, AI工程, LLM能力]
aliases: ["LLM Engineering Three Phases", "LLM工程三阶段对比"]
relates_to:
  - target: "[[LLM-工程三阶段]]"
    type: extends
    confidence: 0.9
  - target: "[[Prompt-Engineering]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Harness-Engineering]]"
    type: compares_to
    confidence: 0.9
supersedes: null
---

# LLM 工程三阶段对比分析

## 概述
对比分析 [[Prompt Engineering]]、[[Context Engineering]] 和 [[Harness-Engineering|Harness Engineering]] 三个阶段的核心差异、演化驱动力和未来发展趋势的详细研究。

## 关键内容

1. **三阶段基础维度对比**：
   - **[[Prompt Engineering]]**: 核心问题是"怎么说，让 AI 听懂？"，操作对象是自然语言指令文本，人类角色是指令设计师，AI 角色是执行单次任务的工具，关注输入端的Token级别。主要挑战包括幻觉、不稳定、不可迁移等问题。
   
   - **[[Context Engineering]]**: 核心问题是"给 AI 什么信息，它才能做好？"，操作对象是[[上下文窗口]]中的信息内容与结构，人类角色是信息架构师，AI 角色是在信息流中工作的助手，关注信息流的系统级别。主要挑战包括检索质量、上下文稀释、[[Memory-Management|记忆管理]]等。

   - **[[Harness-Engineering|Harness Engineering]]**: 核心问题是"设计什么环境，AI 才能持续做好？"，操作对象是代码库环境、约束系统、反馈循环，人类角色是环境架构师，AI 角色是自主编码的主体，关注工程环境的组织级别。主要挑战包括熵增、约束设计、人机协作边界等。

2. **技术机制与演化分析**：
   - **核心机制**: [[Prompt Engineering]] 依赖条件概率引导 `P(y｜prompt)`，[[Context Engineering]] 采用信息检索 + 上下文组装，[[Harness-Engineering|Harness Engineering]] 使用机械约束 + 反馈循环。
   
   - **约束类型**: 从 Prompt 的软约束（语言描述）发展到 Context 的半软约束（结构化注入），再到 Harness 的硬约束（CI [[门控机制（Gating Mechanism）|门控]]，不可绕过）。
   
   - **演化驱动力**: 从 Prompt 到 Context 的跃迁由[[上下文窗口]]突破（4K → 128K）、LLM推理能力提升和企业级RAG需求爆发触发；从 Context 到 Harness 的跃迁由 Agent能力跃迁、规模化[[代码生成]]后的质量崩溃以及[[OpenAI]] Harness案例的示范效应驱动。

3. **未来发展趋势**：
   - **短期趋势**（2025-2026）包括Harness基础设施产品化、多Agent协作标准化和自进化约束系统的发展。
   
   - **中期预测**（2026-2028）预测第四阶段将是**[[组织工程]]（[[组织工程|Organizational Engineering]]）**，重点设计人机协作的整个组织系统，人类将专注于目标设定、价值判断、伦理边界和战略方向。
   
   - **长期预测**（2028-2030+）预示了"[[软件即意图]]"和[[自我演进软件系统]]的出现，工程师角色将从编码转向意图表达和系统目标设定。

## 来源
- [[ai-engineering--04_comparison_and_future]] — LLM 工程三阶段：对比分析与未来预测

## 相关
- [[LLM-工程三阶段]] — relates_to
- [[Prompt-Engineering]] — compares_to
- [[Context-Engineering]] — compares_to
- [[Harness-Engineering]] — compares_to
- [[Organizational-Engineering]] — relates_to