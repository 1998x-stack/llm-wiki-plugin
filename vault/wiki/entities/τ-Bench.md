---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [基准测试, 对话Agent, 评测, Anthropic, AI工程]
aliases: ["τ-Bench", "Tau-Bench"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: uses
  - target: "[[SWE-bench]]"
    type: compares_to
supersedes: null
---

# τ-Bench

## 概述
τ-Bench 是对话 Agent 的评测基准，用于评估 Agent 在多轮对话任务中的表现，由 [[Anthropic]] 相关团队提出。

## 关键内容

1. **评测目标**：
   - 专注于对话式 Agent 的质量评估
   - 模拟真实用户与 Agent 的多轮交互场景
   - 衡量任务完成率、对话效率和用户满意度

2. **与 [[τ2-Bench]] 的关系**：
   - [[τ2-Bench]] 是其后续版本（arxiv: 2506.07982）
   - 两者共同构成对话 [[评测驱动开发|Agent 评测]]的标准基准

3. **在评测体系中的位置**：
   - 与 [[SWE-bench]]（编码）、[[WebArena]]/[[OSWorld]]（[[计算]]机使用）共同构成多类型 [[评测驱动开发|Agent 评测]][[矩阵]]
   - 被 [[Anthropic]] 工程博客引用为对话 [[评测驱动开发|Agent 评测]]的参考标准

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[评测驱动开发]] — uses（τ-Bench 是对话 Agent 评测的标准工具）
- [[SWE-bench]] — compares_to（不同领域的 Agent 评测基准）
- [[τ2-Bench]] — extends（τ2-Bench 是 τ-Bench 的后续版本）
