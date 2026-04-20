---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["agent-pattern", "workflow", "feedback-loop", "iteration"]
aliases: ["评估器-优化器模式", "Feedback Loop", "迭代优化模式"]
relates_to:
  - "[[AI Agent 架构模式]] — part_of"
  - "[[Agent vs Workflow]] — relates_to"
supersedes: null
---

# Evaluator-Optimizer 模式

## 概述
一个 LLM 生成响应，另一个 LLM 提供评估和反馈，形成循环迭代机制，直到输出通过评估标准。

## 关键内容
1. **工作流程**：Input → [Generator] → [Evaluator] → Pass? → Output（若未通过则反馈给 Generator 重新生成）。形成闭环反馈循环。
2. **适用场景的两个判断标准**：
   - LLM 响应在人工反馈后可明显改进
   - LLM 能提供有效的反馈
3. **典型案例**：文学翻译（翻译器 + 评论器）；复杂搜索任务（多轮搜索+分析）；代码生成与审查循环。
4. **工程要点**：Evaluator 需要有明确的评估标准，避免无限循环。应设置最大迭代次数和收敛条件。
5. **与软件工程的对应**：Evaluator-Optimizer 对应 Feedback Control Loop（反馈控制循环），通过持续反馈调节系统输出。

## 来源
- [[01_building_effective_agents.md]] — 第三章 3.6 节，Anthropic Engineering Blog "Building effective agents"

## 相关
- [[AI Agent 架构模式]] — part_of (五种核心模式之一)
- [[ACI (Agent-Computer Interface)]] — relates_to (评估标准设计属于 ACI 范畴)
- [[Agent vs Workflow]] — relates_to (属于工作流范式)
