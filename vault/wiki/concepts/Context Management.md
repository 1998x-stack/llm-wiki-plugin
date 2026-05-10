---
type: concept
title: Context Management
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 方法论, AI工程]
aliases:
- 上下文管理
- Agent Context Management
- 工作记忆管理
relates_to:
- target: '[[Context-Engineering]]'
  type: implements
  confidence: 0.95
- target: '[[ACI 设计原则]]'
  type: uses
  confidence: 0.9
- target: '[[上下文窗口]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# Context Management

## 概述

Context Management（上下文管理）是 Agent 系统中决定哪些历史保留、哪些删除、错误格式如何处理、哪些 observation 更值得进入 prompt 的机制。它本质上是 agent 的"[[工作记忆]]管理"。

## 关键内容

### 核心问题

LM 不是外部记忆无限的系统。每条历史都占用[[上下文预算管理|上下文预算]]，而且错误、冗余、过时信息会污染后续决策。

### 论文发现

在 [[SWE-bench]] Lite 的[[Ablation Study|消融实验]]中：
- **Last 5 observations** 的效果优于 **Full history**
- 去掉 demonstration 后也会略有下降

### 核心洞察

> "不是历史越多越好，而是最近、相关、结构化的历史更好。这和人类[[工作记忆]]很像：解决当前 bug，最有用的是最近几步的操作与反馈，而不是完整人生回放。"

### 与 Context Engineering 的关系

Context Management 是 [[Context-Engineering]] 在 Agent 层面的具体实现：
- 决定了哪些历史要保留、哪些要删
- 错误格式怎么处理
- 哪些 observation 更值得进入 prompt

这与 [[Context Engineering]] 中的"分层记忆（hot/warm/cold）"和"按需检索"理念一致。

### 设计原则

| 原则 | 说明 |
|------|------|
| **最近优先** | 最近几步的操作与反馈最有用 |
| **相关性过滤** | 只保留与当前任务相关的信息 |
| **结构化存储** | 以结构化形式而非原始文本存储历史 |
| **错误隔离** | 错误信息需要标记，避免污染后续决策 |

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/03-SWE-agent 论文的所有核心概念 展开详细分析 一个一个.md]] — SWE-agent 核心概念分析

## 相关

- [[Context-Engineering]] — implements（上下文管理是上下文工程的具体实现）
- [[ACI 设计原则]] — uses（遵循简洁反馈原则）
- [[上下文窗口]] — related_to（受上下文窗口容量约束）
