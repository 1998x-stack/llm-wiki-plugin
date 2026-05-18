---
type: entity
entity_type: tool
status: active
confidence: 0.5
created: 2026-04-21
updated: 2026-04-21
last_accessed: 2026-04-21
source_count: 1
tags: [技术, 工具, 工具与框架]
aliases: []
relates_to:
  - 知识图谱树
  - 检索增强生成
supersedes: null
---

# Neo4j

## 概述
Neo4j 是一个原生图数据库，用于存储和查询图结构数据。在知识图谱树方案中，所有知识节点（目录节点、知识单元节点）及其父子、关联关系都存入 Neo4j，支持通过图遍历拉取完整知识链路进行复杂多跳推理。

## 关键内容
1. **在知识图谱树中的角色**：存储所有图谱树节点及其关系
2. **检索方式**：向量检索做全局节点匹配，图遍历拉取知识链路
3. **优势**：天然支持多跳查询和关系推理

## 来源
- [[raw/articles/essays/thinking-series/022-波克城市面试]] — 全文

## 相关
- [[知识图谱树]] — used_by
- [[检索增强生成]] — used_by
