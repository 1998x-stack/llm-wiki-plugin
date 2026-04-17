---
type: concept
status: active
confidence: 0.9
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 历史
- 计算理论
aliases:
- SQL
- Structured Query Language
- 结构化查询语言
relates_to:
- target: "[[关系模型]]"
  type: implements
  confidence: 0.95
  note: 关系模型的标准查询语言
- target: "[[关系模型论文]]"
  type: extends
  confidence: 0.9
  note: 论文为 SQL 奠定了理论基础
- target: "[[关系代数]]"
  type: implements
  confidence: 0.9
  note: SQL 的语义基于关系代数
- target: "[[关系演算]]"
  type: implements
  confidence: 0.85
  note: SQL 更接近关系演算的声明式风格
- target: "[[E.F. Codd]]"
  type: extends
  confidence: 0.8
  note: Codd 对 SQL 设计表达了不满
- target: "[[SQLite]]"
  type: implements
  confidence: 0.8
  note: SQLite 使用 SQL 作为查询语言
- target: "[[函数式编程]]"
  type: compares_to
  confidence: 0.7
  note: 两者都是声明式编程范式
supersedes: null
---

# SQL

## 概述

SQL（Structured Query Language，结构化查询语言）是关系模型的标准查询语言，将关系代数和关系演算的思想转化为人类可读的查询语言，是历史上使用最广泛的声明式编程语言。

## 关键内容

### 起源

- **System R**（IBM 圣何塞研究实验室，1970年代中期）：SQL 的前身 SEQUEL（Structured English Query Language）为 System R 设计
- **Ingres**（UC Berkeley）：使用 QUEL 查询语言，更忠实于 Codd 的元组关系演算
- **1986年**：SQL 被 ANSI 采纳为标准
- 此后经历了多次修订：SQL-89、SQL-92、SQL:1999、SQL:2003 等

### 设计哲学

用近似自然语言的方式表达查询意图，使得非专业程序员也能够有效地操纵数据库。`SELECT ... FROM ... WHERE ...` 的结构直接对应关系演算的声明式风格。

### Codd 的不满

Codd 对 SQL 语言的设计表达了不满，认为它在某些方面偏离了关系模型的数学纯粹性（如允许重复行、NULL 值的处理等），但到那时 SQL 已经成为了事实标准。

### 标准化历程

| 版本 | 年份 | 主要特性 |
|------|------|---------|
| SQL-86 | 1986 | 首个 ANSI 标准 |
| SQL-92 | 1992 | 大幅扩展 |
| SQL:1999 | 1999 | 引入递归查询、面向对象特性 |
| SQL:2003 | 2003 | XML 支持、窗口函数 |

### 当代地位

- "SQL-on-everything"成为通用数据查询趋势
- Text-to-SQL 技术使自然语言查询成为可能
- Presto/Trino、Apache Spark SQL、Amazon Athena 等将 SQL 扩展到分布式存储系统

## 来源

- [[raw/books/计算机科学/07-codd-relational-model.md]]

## 相关

- [[关系模型]] — SQL 的理论基础
- [[关系模型论文]] — 理论来源
- [[关系代数]] — SQL 的语义基础
- [[关系演算]] — SQL 的风格来源
- [[E.F. Codd]] — 理论基础奠基者
- [[SQLite]] — SQL 的轻量级实现
- [[函数式编程]] — 同为声明式范式
