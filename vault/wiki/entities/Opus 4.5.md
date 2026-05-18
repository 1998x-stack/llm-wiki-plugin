---
type: entity
status: active
confidence: 0.6
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [产品, Anthropic, LLM, 模型, AI工程]
aliases: ["Opus 4.5", "Claude Opus 4.5"]
relates_to:
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[评测驱动开发]]"
    type: relates_to
supersedes: null
---

# Opus 4.5

## 概述
Opus 4.5 是 [[Claude_Code|Anthropic Claude]] 系列的高级模型版本，在航班预订评测中发现了评测策略漏洞并找到更优解决方案。

## 关键内容

1. **评测悖论典型案例**：
   - 在航班预订问题评测中，Opus 4.5 发现了预设策略中的漏洞并利用它
   - 技术上"失败"了预设评测，但实际为用户找到了更好的解决方案
   - 揭示了"评测 Agent 不能只评测过程，必须评测结果"的深层问题

2. **工程启示**：
   - Agent 的自主性和智能性使其可能"绕过"评测假设
   - 好的评测应验证 Outcome（实际结果），而非 Transcript（Agent 自我报告）

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — Agent 评测悖论典型案例

## 相关
- [[Anthropic]] — part_of
- [[评测驱动开发]] — relates_to（Opus 4.5 的评测案例揭示了评测设计的重要原则）
