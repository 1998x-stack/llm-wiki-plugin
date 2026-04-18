---
type: entity
title: "Zep"
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
  - target: "[[Mem0]]"
    type: compares_to
  - target: "[[信息提取损耗]]"
    type: causes
supersedes: null
---

# Zep

## 概述
主流 AI [[记忆工具]]之一，与 Mem0 同属传统方案阵营，采用 AI 提取关键信息的存储策略，被 [[MemPalace]] 作为主要对比对象。

## 关键内容
- **存储策略**：AI 提取关键信息，与 Mem0 设计哲学相同
- **根本缺陷**：让 AI 来决定该记什么，提取时丢失推理链和上下文
- **性能**：[[LongMemEval]] [[候选生成|Recall]]@5 约 85%，低于 [[MemPalace]] 的 96.6%（差距约 11pp）
- **运行环境**：依赖云 API
- **索引结构**：平铺向量数据库

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 深度解析系列总览篇

## 相关
- [[MemPalace]] — compares_to
- [[Mem0]] — compares_to
- [[信息提取损耗]] — causes
