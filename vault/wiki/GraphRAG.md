---
type: concept
status: active
confidence: 0.5
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: [技术, 研究]
aliases: [Graph RAG]
relates_to:
  - 检索增强生成
  - 知识图谱树
supersedes: null
---

# GraphRAG

## 概述
GraphRAG 是一种结合知识图谱与检索增强生成的技术方案。其核心思路是自下而上为每个文档分块生成三元组（实体-关系-实体），再将三元组聚合成图谱，通过社区检测实现深层次推理。适用于需要跨文档关联和复杂推理的场景，但在具有强原生框架结构的数据（如书籍、课件）上可能失效。

## 关键内容
1. **构建方式**：自下而上，先对分块生成三元组，再聚合为图谱
2. **核心能力**：社区检测、深层次推理、跨文档关联
3. **局限性**：会丢失原文档的完整框架结构，不适合具有强层级关系的数据（如书籍目录、教学大纲）
4. **与知识图谱树的对比**：GraphRAG 自下而上构建，知识图谱树自上而下还原原生框架

## 来源
- [[raw/articles/essays/thinking-series/022-波克城市面试]] — 全文

## 相关
- [[检索增强生成]] — extends
- [[知识图谱树]] — compares_to
- [[RAG项目90%从第一步就错了]] — relates_to
