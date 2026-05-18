---
type: tool
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [database, query-language, technology, 计算理论]
aliases: ["Structured Query Language", "结构化查询语言"]
relates_to:
  - target: "[[Data Scientist Agent]]"
    type: used_by
    confidence: 0.8
supersedes: null
---

# SQL

## 概述
结构化查询语言（Structured Query Language），是用于管理关系数据库的标准语言，广泛应用于数据查询、更新和管理。

## 关键内容

1. **核心功能**：
   - 数据查询（SELECT语句）
   - 数据操纵（INSERT、UPDATE、DELETE）
   - 数据定义（CREATE、ALTER、DROP）
   - 数据控制（GRANT、REVOKE[[Permissions|权限]]管理）

2. **SQL最佳实践**：
   - 优化查询性能，尽早使用WHERE子句过滤
   - 合理使用索引提高查询效率
   - 避免生产环境中使用SELECT *操作
   - 在探索数据时限制结果集大小
   - 为复杂逻辑添加清晰注释

3. **常见应用场景**：
   - 数据库管理系统交互
   - [[数据分析]]和报表生成
   - 数据[[仓库]]查询
   - 业务智能系统支持

## 来源
- [[data-scientist.md]] — SQL查询最佳实践
- [[数据库系统概念]] — 理论基础

## 相关
- [[BigQuery]] — SQL执行平台
- [[数据分析]] — 应用领域
- [[Data Scientist Agent]] — 使用工具
- [[数据库]] — 技术基础