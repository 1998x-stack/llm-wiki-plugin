---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [基准测试, 对话Agent, 评测, AI工程]
aliases: ["τ2-Bench", "Tau2-Bench", "Tau Squared Bench"]
relates_to:
  - target: "[[τ-Bench]]"
    type: extends
  - target: "[[评测驱动开发]]"
    type: uses
supersedes: null
---

# τ2-Bench

## 概述
τ2-Bench 是 [[τ-Bench]] 的后续版本，用于对话 Agent 的进阶评测，论文编号 arxiv: 2506.07982。

## 关键内容

1. **与 [[τ-Bench]] 的关系**：
   - τ2-Bench 是 [[τ-Bench]] 的迭代升级版本
   - 延续了对话式 Agent 多轮交互评测的核心框架

2. **改进方向**：
   - 可能包含更复杂的对话场景
   - 更细粒度的评分维度
   - 更贴近真实用户交互的评测标准

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[τ-Bench]] — extends（τ2-Bench 扩展自 τ-Bench）
- [[评测驱动开发]] — uses（对话 Agent 评测基准体系的一部分）
