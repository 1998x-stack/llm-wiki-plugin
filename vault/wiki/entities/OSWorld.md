---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [基准测试, 计算机使用, 操作系统, 评测, 强化学习]
aliases: ["OSWorld"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: uses
  - target: "[[WebArena]]"
    type: compares_to
supersedes: null
---

# OSWorld

## 概述
OSWorld 是[[计算]]机使用 Agent 的评测基准，用于评估 Agent 在[[操作系统]]环境中的交互和操作能力。

## 关键内容

1. **评测目标**：
   - 评估 Agent 在桌面/[[操作系统]]环境中的操作能力
   - 涵盖文件管理、应用操作、系统[[Configuration|配置]]等任务
   - 提供标准化的[[操作系统]]交互评测环境

2. **在评测体系中的位置**：
   - 与 [[WebArena]] 共同构成[[计算]]机使用 Agent 的评测基准
   - 与 [[SWE-bench]]（编码）、[[τ-Bench]]（对话）形成多类型 [[评测驱动开发|Agent 评测]][[矩阵]]

3. **技术特点**：
   - 支持 GUI 交互的自动化评测
   - 验证 Agent 在真实或沙盒环境中的操作能力
   - 面临评测 GUI 交互本质上难以自动化的挑战

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[评测驱动开发]] — uses（OSWorld 是计算机使用 Agent 评测的标准工具）
- [[WebArena]] — compares_to（同为计算机使用 Agent 评测基准）
- [[SWE-bench]] — compares_to（不同领域的 Agent 评测基准）
