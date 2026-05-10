---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: ["推荐系统", "协同过滤", "查询语言", "Xerox PARC"]
aliases: ["Tapestry Query Language"]
relates_to: 
  - target: "[[Tapestry 系统]]"
    type: part_of
  - target: "[[协同过滤]]"
    type: enables
  - target: "[[SQL]]"
    type: extends
supersedes: null
---

# TQL

## 概述
TQL（[[Tapestry 系统|Tapestry]] Query Language）是 [[Tapestry 系统]]为信息过滤量身定制的查询语言，扩展了 SQL 以更好地处理半结构化文档数据，支持内容过滤与[[协同过滤]]的有机结合。

## 关键内容

1. **设计特点**：
   - 支持可扩展的字段集合，不同文档类型可有不同字段
   - 支持集合值字段，如收件人列表等
   - 可在查询中直接引用其他用户的[[标注]]，实现[[协同过滤]]

2. **核心功能**：
   - [[基于内容的过滤]]：通过 words、sender、subject 等字段进行关键词匹配
   - [[协同过滤]]：通过 annotation 字段引用其他用户的评价和[[标注]]
   - 组合查询：将内容过滤与[[协同过滤]]条件组合使用

3. **技术实现**：
   - 三层处理流程：查询转换→SQL翻译→查询优化
   - 转换为单调查询再转换为增量查询，优化扫描效率
   - 基于商业关系数据库的实现

## 来源
- [[Using Collaborative Filtering to Weave an Information Tapestry]] — 原始论文

## 相关
- [[Tapestry 系统]] — part_of
- [[协同过滤]] — enables
- [[SQL]] — extends