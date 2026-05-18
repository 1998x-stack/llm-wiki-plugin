---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [developer, open-source, ai-tools, AI工程]
aliases: [TÂCHES, TACHES]
relates_to:
  - target: "[[GSD]]"
    type: creator
supersedes: null
---

# TÂCHES

## 概述
TÂCHES 是 GSD ([[GSD|get-shit-done]]) 框架的开发者，一位完全依赖 [[Claude Code]] 的独立开发者，专注于开发对抗 [[Context Rot]] 问题的工程框架。

## 关键内容

1. **主要成就**：
   - 开发了 GSD ([[GSD|get-shit-done]]) 框架，[[GitHub]] Stars 40k+
   - 专门针对 [[Claude Code]] 使用中的 [[Context Rot]] 问题设计工程解决方案
   - 该框架被 [[Amazon]]/[[Google]]/Shopify 工程师广泛使用

2. **核心理念**：
   - 提出核心哲学："The complexity is in the system, not in your workflow."
   - 强调复杂度应该在系统里，不应该在工作流里
   - 设计了五大技术支柱来解决 LLM [[Context Management|上下文管理]]问题

3. **技术贡献**：
   - [[Context Engineering|上下文工程]]：每个命令只加载真正需要的文件
   - [[XML 结构化 Prompt]]：使用结构化格式提高准确性
   - [[多智能体编排]]：主会话协调，[[Subagents-in-Claude-Code|子智能体]]执行
   - 原子 [[Git Commit|Git 提交]]：每个任务独立提交
   - [[波次并行执行]]：DAG 依赖分析，并行执行

## 来源
- [[GSD 深度解析 · 第一篇：Context Rot 与上下文工程]] — 介绍其工作

## 相关
- [[GSD]] — created
- [[Claude Code]] — target platform