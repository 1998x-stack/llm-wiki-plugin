---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI, 工具, 方法论, 工具与框架]
aliases:
  - "Thariq Shihipar"
  - "塔里克·希希帕尔"
relates_to:
  - target: "[[Claude-Code]]"
    type: part_of
    confidence: 0.95
  - target: "[[Anthropic]]"
    type: part_of
    confidence: 0.95
  - target: "[[渐进式披露 -Progressive-Disclosure]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Thariq Shihipar

## 概述

Anthropic 技术人员，Claude Code 项目核心成员。2025 年发表官方博客文章《Seeing like an agent: how we design tools in Claude Code》，系统阐述了 Claude Code 的工具设计哲学和演进历程。

## 关键内容

### 在 Anthropic 的角色

Thariq Shihipar 是 Anthropic 的技术团队成员（member of technical staff），主要负责 Claude Code 项目的开发和工具设计工作。

### 核心贡献

**Claude Code 工具设计哲学**：
- 提出"像智能体一样观察"（See like an agent）的设计理念
- 强调工具设计需要契合模型自身能力，而非人类直觉
- 记录了 [[AskUserQuestion-Tool|AskUserQuestion]]、[[ExitPlanTool]]、[[TodoWrite-Tool|TodoWrite]]、Task 等核心工具的演进历程
- 揭示了[[渐进式披露（Progressive Disclosure）]]在工具设计中的应用

**工具演进洞察**：
- 从 RAG 预索引到 Grep 自主搜索的[[规范化理论|范式]]转变
- [[TodoWrite-Tool|TodoWrite]] 到 [[Task-Tool|Task Tool]] 的演进：从"保持模型轨道"到"Agent 间协调"
- 随着模型能力提升，旧工具可能从"帮助"变为"约束"

### 发表作品

- "Seeing like an agent: how we design tools in Claude Code" (2025) — Anthropic 官方博客

## 来源

- [[raw/articles/ai-engineering/claude-blog/Seeing like an agent_ how we design tools in Claude Code.md]] — 作者简介

## 相关

- [[Claude-Code]] — 主要工作项目
- [[Anthropic]] — 所属机构
- [[渐进式披露-Progressive-Disclosure]] — 提出的核心设计方法论
