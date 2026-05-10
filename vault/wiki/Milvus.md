---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: [技术, 工具]
aliases: []
relates_to:
  - Elasticsearch
  - 检索增强生成
supersedes: null
---

# Milvus

## 概述
Milvus 是一个开源向量数据库，专为大规模向量相似度检索设计。在 RAG 系统中负责向量检索，与 Elasticsearch 配合实现关键词+向量的混合检索链路，支持语义级别的文档匹配。

## 关键内容
1. **在 RAG 中的角色**：向量检索组件，处理语义相似度匹配
2. **典型搭配**：与 Elasticsearch 组成混合检索
3. **局限性**：仅靠向量检索无法解决多跳推理和跨章节关联问题

## 来源
- [[raw/articles/essays/thinking-series/022-波克城市面试]] — 全文

## 相关
- [[Elasticsearch]] — compares_to
- [[检索增强生成]] — used_by
