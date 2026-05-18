---
type: concept
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["路由", "RAG", "LLM", "分类", "检索架构", "AI工程"]
aliases: [LLM Routing, 模型路由, AI 路由]
relates_to:
  - target: "[[词汇不匹配问题]]"
    type: causes
  - target: "[[确定性内存设计]]"
    type: contradicts
  - target: "[[MemPalace]]"
    type: used_by
  - target: "[[关键词评分检测]]"
    type: compares_to
supersedes: null
---

# LLM 路由

## 概述
使用 LLM 模型在索引期和查询期自动分类和路由请求到不同数据分区的策略。

## 关键内容
- **Mem[[MemPalace 宫殿架构|Palace Architecture]] v1 实践**：
  - 索引时：[[Claude 3 Haiku|Haiku]] 模型给每个会话分配 Room 标签
  - 查询时：[[Claude 3 Haiku|Haiku]] 模型把问题路由到 1-2 个 Room
  - 结果：R@5 = 34.2%，62.5% 的查询零召回，比朴素基线还低 26 个百分点
- **失败根因**：两个独立的 LLM 调用产生词汇不匹配。索引时标记为"relationship_advice"，查询时路由到"personal_guidance"——标签向量相似度不够
- **关键教训**：用 LLM 做双端路由，必须保证两端共享同一套词汇体系
- **v2 改进方案**：去掉查询期 LLM，改用关键词重叠度（词频统计）路由，R@5 提升到 75.6%
- **工程启示**：两端 LLM 路由要共享词汇，最安全的方式是查询期改用确定性匹配

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析

## 相关
- [[词汇不匹配问题]] — causes
- [[确定性内存设计]] — contradicts
- [[MemPalace]] — used_by
- [[关键词评分检测]] — compares_to
