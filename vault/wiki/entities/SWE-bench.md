---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [benchmark, coding-agent, evaluation, AI工程]
aliases: ["SWE-bench", "Software Engineering Benchmark"]
relates_to:
  - "[[Anthropic]] — participates_in"
  - "[[ACI (Agent-Computer Interface)]] — evaluates"
supersedes: null
---

# SWE-bench

## 概述
编码 [[评测驱动开发|Agent 评测]]基准，用于评估 AI 模型在真实软件工程任务中的表现，[[Anthropic]] Sonnet 模型在此评测中取得突破性表现。

## 关键内容
1. **评测定位**：SWE-bench 是评估 AI 编码 Agent 能力的基准测试，聚焦于真实 [[GitHub]] issue 的解决能力。
2. **[[Anthropic]] 的突破**：[[Anthropic]] 的 Sonnet 模型在 SWE-bench 评测中取得突破性表现，验证了 [[ACI 设计原则]]的有效性。
3. **ACI 实证案例**：在 SWE-bench Agent 中发现，模型在 agent 离开根目录后使用相对路径时会出错。解决方案是要求工具**始终使用绝对路径**，这一改变使模型运行"无懈可击"。
4. **工程意义**：SWE-bench 的实证结果证明了工具定义和 ACI 设计对 Agent 性能的关键影响。
5. **[[基础设施噪声]]交叉验证**：在 SWE-Bench 上的交叉实验（227 个问题，每题 10 次采样，RAM 1x → 5x）显示成功率随 RAM 单调增加，但提升幅度仅 **1.54 个百分点**（5x vs 1x）。效应小于 [[Terminal-Bench 2.0]] 的原因：SWE-Bench 任务资源需求普遍较低，资源约束较少成为瓶颈。但重要结论相同：资源[[Configuration|配置]]对 SWE-Bench 也不是中性的。

## 来源
- [[01_building_effective_agents.md]] — 第五章，Anthropic Engineering Blog "Building effective agents"
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/06_infrastructure_noise.md]] — 基础设施噪声交叉验证实验

## 相关
- [[Anthropic]] — participates_in (评测参与者)
- [[ACI (Agent-Computer Interface)]] — evaluates (ACI 原则的验证平台)
- [[Terminal-Bench 2.0]] — compares_to (交叉验证显示 SWE-Bench 基础设施噪声效应更小)
- [[基础设施噪声]] — affected_by (资源配置影响评测结果)
