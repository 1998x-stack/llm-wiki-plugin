---
type: entity
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [AI记忆, 分层记忆, 基准测试]
aliases: [Memori memory system]
relates_to:
  - target: "[[LoCoMo]]"
    type: used_by
  - target: "[[MemPalace]]"
    type: compares_to
  - target: "[[分层记忆系统]]"
    type: implements
supersedes: null
---

# Memori

## 概述
[[分层记忆系统]]，在 [[LoCoMo]] 基准数据集上 [[候选生成|Recall]]@10 达到 81.95%，被 [[MemPalace]]（88.9%）超越约 7 个百分点。

## 关键内容
- **定位**：[[分层记忆架构]]的竞争性实现方案
- **[[LoCoMo]] 成绩**：R@10 = 81.95%
- **对比**：[[MemPalace]] 在 [[LoCoMo]] 上达到 88.9%，领先 7pp
- **架构特点**：具体架构细节未在 [[MemPalace]] benchmark 文档中展开

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析

## 相关
- [[LoCoMo]] — used_by
- [[MemPalace]] — compares_to
- [[分层记忆系统]] — implements
