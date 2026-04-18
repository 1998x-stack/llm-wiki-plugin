---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [基准测试, 评估, AI记忆, 数据集, 长期记忆]
aliases: [LoCoMo dataset, Long-term Conversational Memory]
relates_to:
  - target: "[[LongMemEval]]"
    type: compares_to
  - target: "[[MemPalace]]"
    type: used_by
supersedes: null
---

# LoCoMo

## 概述
专注于人际关系和个人历史长期记忆场景的基准数据集，用于评估 AI 记忆系统在社交关系、个人经历等维度的检索能力。

## 关键内容
- **应用场景**：人际关系记忆、个人历史回溯、社交关系推理
- **与 [[LongMemEval]] 的区别**：[[LongMemEval]] 侧重跨会话多轮对话召回，LoCoMo 侧重人际关系和个人历史场景
- **[[MemPalace]] 成绩**：在 LoCoMo 数据集上 R@10 = 88.9%，超过 [[Memori]] 的 81.95%（+7pp）
- **测试方式**：通过宫殿结构路由 + [[混合搜索]]（BM25 + 向量）进行检索评估

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 深度解析系列总览篇

## 相关
- [[LongMemEval]] — compares_to
- [[MemPalace]] — used_by
- [[Memori]] — compares_to
