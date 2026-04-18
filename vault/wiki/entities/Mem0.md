---
type: entity
title: "Mem0"
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [工具, AI, 记忆系统, 云API]
aliases: []
relates_to:
  - target: "[[MemPalace]]"
    type: compares_to
  - target: "[[Zep]]"
    type: compares_to
  - target: "[[信息提取损耗]]"
    type: causes
supersedes: null
---

# Mem0

## 概述
主流 AI [[记忆工具]]之一，采用 AI 提取关键信息的存储策略。与 Zep 同属传统方案阵营，被 [[MemPalace]] 作为主要对比对象。

## 关键内容
- **存储策略**：AI 提取关键信息，例如从一段两小时的 GraphQL 决策讨论中仅提取"用户偏好 GraphQL"
- **根本缺陷**：让 AI 来决定该记什么，提取时丢失推理链。当用户问"为什么我们用 GraphQL"时，AI 无法还原当时的三个痛点、两小时讨论、DataLoader 决策等完整推理过程
- **性能**：[[LongMemEval]] [[候选生成|Recall]]@5 约 85%，低于 [[MemPalace]] 的 96.6%（差距约 11pp）
- **运行环境**：依赖云 API
- **索引结构**：平铺向量数据库

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 深度解析系列总览篇

## 相关
- [[MemPalace]] — compares_to
- [[Zep]] — compares_to
- [[信息提取损耗]] — causes
