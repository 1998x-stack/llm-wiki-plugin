---
type: concept
title: "FTS5"
status: active
confidence: 0.85
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [工具, 数据库, 技术, 搜索, AI工程]
aliases: ["Full-Text Search 5", "SQLite FTS5", "全文搜索"]
relates_to:
  - target: "[[SQLite]]"
    type: part_of
    confidence: 1.0
  - target: "[[Claude-Mem]]"
    type: related_to
    confidence: 0.9
supersedes: null
---

# FTS5

## 概述
FTS5（Full-Text Search version 5）是 [[SQLite]] 的内置全文搜索扩展模块，提供高效的文本索引和检索能力。在 [[Claude-Mem]] 中，FTS5 被用于对存储的记忆观察记录进行快速关键词搜索，支持 BM25 相关度排序、前缀匹配和短语查询。FTS5 在 [[Claude-Mem]] 中有 332 个测试用例保证 SQL 注入安全，是其搜索层的核心组件。

## 关键内容
- **工作原理**：对文本字段建立[[倒排索引]]，查询时快速定位包含关键词的行
- **支持功能**：布尔查询（AND/OR/NOT）、短语搜索（引号）、前缀通配符（`term*`）、BM25 相关度评分
- **与 [[SQLite]] 集成**：作为虚拟表（Virtual Table）接入，语法兼容普通 SQL 查询
- **局限**：不支持语义搜索（需向量数据库如 [[ChromaDB]] 补充）；对中文等无空格语言需配合分词器

## 来源
- 综合自内部引用：[[Claude-Mem]] 等

## 相关
- [[SQLite]]
- [[Claude-Mem]]
- [[ChromaDB]]
