---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["基准测试", "计算机使用", "网页自动化", "评测"]
aliases: ["WebArena"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: uses
  - target: "[[OSWorld]]"
    type: compares_to
supersedes: null
---

# WebArena

## 概述
WebArena 是计算机使用 Agent 的评测基准，用于评估 Agent 在网页环境中的自动化操作能力，论文编号 arxiv: 2307.13854。

## 关键内容

1. **评测目标**：
   - 评估 Agent 在真实网页环境中的交互能力
   - 涵盖网页导航、表单填写、信息检索等任务
   - 提供标准化的网页自动化评测环境

2. **在评测体系中的位置**：
   - 与 OSWorld 共同构成计算机使用 Agent 的评测基准
   - 与 SWE-bench（编码）、τ-Bench（对话）形成多类型 Agent 评测矩阵

3. **技术特点**：
   - 基于真实网页环境的仿真
   - 支持 DOM 交互和截图交互两种模式
   - 验证 Agent 在不同情境下选择正确交互方式的能力

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[评测驱动开发]] — uses（WebArena 是计算机使用 Agent 评测的标准工具）
- [[OSWorld]] — compares_to（同为计算机使用 Agent 评测基准）
- [[SWE-bench]] — compares_to（不同领域的 Agent 评测基准）
