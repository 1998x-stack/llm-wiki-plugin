---
type: entity
entity_type: person
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- Edgar Frank Codd
- Ted Codd
- E.F. Codd
- 埃德加·科德
relates_to:
- target: "[[关系模型论文]]"
  type: caused
  confidence: 0.99
  note: 1970年发表
- target: "[[关系模型]]"
  type: caused
  confidence: 0.99
  note: 发明者
- target: "[[关系代数]]"
  type: caused
  confidence: 0.95
  note: 定义者
- target: "[[规范化理论]]"
  type: caused
  confidence: 0.95
  note: 开创者
- target: "[[数据独立性]]"
  type: caused
  confidence: 0.9
  note: 系统区分了物理和逻辑两个层面
- target: "[[SQL]]"
  type: caused
  confidence: 0.8
  note: 为 SQL 奠定了理论基础
- target: "[[Edsger Dijkstra]]"
  type: compares_to
  confidence: 0.7
  note: 同时代将计算机科学提升为数学化科学的先驱
- target: "[[John Backus]]"
  type: compares_to
  confidence: 0.7
  note: 分别开创了数据库和编程语言的数学化
supersedes: null
---

# E.F. Codd

## 概述

英国出生、后移居美国的[[计算]]机科学家（1923–2003），在 IBM 圣何塞研究实验室工作期间提出了[[关系模型|关系数据模型]]。1981年因"对关系数据库管理理论和实践的基础性和持续性贡献"获得 ACM [[阿兰·图灵|图灵]]奖。

## 关键内容

### 学术背景

- 兼具数学与化学的跨学科训练
- 天然倾向于用严格的数学工具来描述和解决工程问题

### 关系模型（1970）

- 在《[[关系模型论文|A Relational Model of Data for Large Shared Data Banks]]》中首次提出
- 用集合论和一阶谓词逻辑定义数据模型
- 将数据的逻辑表示与物理存储彻底分离
- 引入了[[关系代数]]、[[关系演算]]、[[规范化理论]]等核心概念

### 来自 IBM 内部的抵制

- IBM 当时在层次数据库 IMS 上有巨大商业利益
- IMS 开发团队认为[[关系模型]]过于理想化
- 这种内部抵制使得 Codd 的思想在 IBM 内部推广异常缓慢
- Larry Ellison 在阅读 Codd 论文后于1977年创立 Oracle，比 IBM 的 DB2（1983年）早了四年

### 对 SQL 的不满

- Codd 对 SQL 语言的设计表达了不满
- 认为 SQL 在某些方面偏离了[[关系模型]]的数学纯粹性
- 但到那时，SQL 已经成为了事实标准

### 图灵奖（1981）

授奖理由是"对关系数据库管理理论和实践的基础性和持续性贡献"。

## 来源

- [[raw/books/计算机科学/07-codd-relational-model.md]]

## 相关

- [[关系模型论文]] — 1970年发表
- [[关系模型]] — 发明
- [[关系代数]] — 定义
- [[规范化理论]] — 开创
- [[SQL]] — 理论基础
- [[Edsger Dijkstra]] — 同时代先驱
