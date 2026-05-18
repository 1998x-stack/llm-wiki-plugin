---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: [技术, 工具, AI工程]
aliases: [ES]
relates_to:
  - Milvus
  - 检索增强生成
supersedes: null
---

# Elasticsearch

## 概述
Elasticsearch 是一个分布式搜索和分析引擎，支持全文检索、结构化搜索和分析。在 RAG 系统中常用于关键词检索，与向量数据库配合实现混合检索链路，保证自主可控和模块化。

## 关键内容
1. **在 RAG 中的角色**：关键词检索组件，与向量数据库组成混合检索
2. **典型搭配**：Elasticsearch（关键词）+ Milvus（向量）
3. **适用场景**：精确匹配、全文搜索、结构化过滤

## 来源
- [[raw/articles/essays/thinking-series/022-波克城市面试]] — 全文

## 相关
- [[Milvus]] — compares_to
- [[检索增强生成]] — used_by
