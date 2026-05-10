---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [ai-engineering, multi-agent, architecture, parallel]
aliases: [Multi-Agent System, 多 Agent 系统, 多智能体系统]
relates_to:
  - target: "[[Agent 架构与设计原则]]"
    type: extends
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[并行 Agent 开发]]"
    type: relates_to
  - target: "[[任务分解]]"
    type: relates_to
  - target: "[[可扩展的受管理 Agent]]"
    type: compares_to
supersedes: null
---

# 多 Agent 系统

## 概述
多 Agent 系统是由多个协作 Agent 组成的 AI 架构模式，通过并行处理和任务分解实现复杂问题的解决，是 Anthropic 工程研究的重要方向。

## 关键内容

1. **从原型到生产的工程实践**：2025 年 6 月提出的多 Agent 研究系统工程指南，实现 90.2% 性能提升，总结 8 条 Prompt 工程原则。

2. **并行 Agent 编程挑战**：2026 年 2 月的 C 编译器构建案例揭示并行 Agent 编程中的接口规范挑战，证明多 Agent 协作需要严格的接口定义。

3. **性能优化关键因素**：
   - Token 使用量是性能的主要预测指标
   - 任务分解质量决定并行效率
   - Agent 间通信开销影响整体性能

4. **与简单模式的平衡**：Anthropic 强调"do the simplest thing that works"，多 Agent 系统仅在单 Agent 无法满足需求时使用，避免过度工程化。

5. **应用场景**：
   - 复杂代码库的并行分析与修改
   - 多步骤研究任务的并行执行
   - 大规模内容生成和处理

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — 多 Agent 系统章节
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/13_building_c_compiler.md]] — C 编译器并行实验

## 相关
- [[Agent 架构与设计原则]] — extends
- [[Anthropic]] — part_of
- [[Claude Code]] — uses
- [[并行 Agent 开发]] — relates_to
- [[任务分解]] — relates_to
- [[评测驱动开发]] — relates_to
- [[上下文工程]] — relates_to
- [[可扩展的受管理 Agent]] — compares_to (分层架构 vs 扁平协作)
