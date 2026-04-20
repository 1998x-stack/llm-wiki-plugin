---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-engineering, agent-architecture, scalability, cost-optimization, managed-agents]
aliases: [Scaled Managed Agents, 受管理 Agent 架构, 分层 Agent 架构, 脑手分离扩展模式]
relates_to:
  - target: "[[脑手分离架构]]"
    type: extends
  - target: "[[Managed-Agents]]"
    type: implements
  - target: "[[多 Agent 系统]]"
    type: compares_to
  - target: "[[Agent 架构与设计原则]]"
    type: part_of
  - target: "[[子 Agent 模式（Sub-Agent Pattern）]]"
    type: relates_to
supersedes: null
---

# 可扩展的受管理 Agent

## 概述
可扩展的受管理 Agent 是一种将 Agent 的推理能力（大脑）与工具执行能力（双手）解耦并分层独立扩展的架构模式，通过不同规模模型匹配任务复杂度实现成本优化。

## 关键内容

1. **三层分层设计**：
   - **战略层（Strategy Layer）**：大型推理模型（如 Opus 4），负责任务理解、规划、决策，调用频率低
   - **战术层（Tactical Layer）**：中型模型（如 Sonnet 4），负责子任务规划、工具序列决策，调用频率中
   - **执行层（Execution Layer）**：小型/专业化模型（如 Haiku 4.5）或确定性代码，负责具体工具调用、数据处理，调用频率高

2. **层间接口设计**：
   - 战略层 → 战术层：高层目标描述（如"收集 S&P 500 IT 行业所有董事会成员信息"）
   - 战术层 → 执行层：具体操作指令（如"搜索 Apple Inc 董事会成员，返回 JSON 格式"）
   - 执行层 → 战术层：结构化结果（包含成功/失败状态、原始数据、元数据）

3. **独立扩展能力**：
   - 推理负载增加时扩展战略层实例
   - 工具调用量增加时扩展执行层实例
   - 特定类型任务增加时为特定领域创建专业化执行 Agent

4. **成本优化效果**：实际成本可降低 60-80%，同时保持关键推理步骤的质量。每次工具调用使用大型推理模型是巨大的成本浪费，该架构允许搜索查询构建由战略层决策（需要高质量），实际网络请求和解析由执行层处理（轻量任务），结果综合由战略层分析（需要高质量）。

5. **关键工程挑战**：
   - **状态同步**：哪些上下文需要传递到哪一层？如何避免信息重复传递（浪费 token）？当执行层失败时，战术层如何得知并适应？
   - **错误传播**：执行层错误可能因延迟报告而在战术层累积；战术层的误解可能导致执行层的系统性错误；跨层的错误追踪需要统一的追踪 ID
   - **延迟 vs 质量权衡**：层次越多通信开销增加，但并行执行机会也增加；任务复杂度越高，多层架构的收益越大

6. **与传统多 Agent 系统的对比**：
   - 受管理 Agent 有明确的层次结构，传统多 Agent 可以是扁平的
   - 受管理 Agent 不同层使用不同大小模型，传统多 Agent 通常使用相同模型
   - 受管理 Agent 各层独立扩展，传统多 Agent 整体扩展
   - 受管理 Agent 成本优化显著，传统多 Agent 成本优化有限

7. **实践建议**：
   - 先分析任务的计算分布：找出哪些步骤需要高级推理，哪些是机械执行
   - 从两层开始：先实现"规划层"和"执行层"，复杂度可控
   - 设计可观察的接口：每层的输入/输出都应该有日志，便于调试
   - 逐步降低执行层的模型大小：从安全的大模型开始，验证质量后再降级

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/17_scaled_managed_agents.md]] — 全文

## 相关
- [[脑手分离架构]] — extends（核心架构思想的扩展）
- [[Managed-Agents]] — implements（受管理 Agent 的具体实现模式）
- [[多 Agent 系统]] — compares_to（与传统多 Agent 系统的对比）
- [[Agent 架构与设计原则]] — part_of（Agent 架构谱系的重要组成部分）
- [[子 Agent 模式（Sub-Agent Pattern）]] — relates_to（同为脑手分离思想的轻量实现）
