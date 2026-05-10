---
type: entity
entity_type: paper
status: active
confidence: 0.98
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
- MapReduce 论文
- Dean Ghemawat 2004 论文
- Simplified Data Processing on Large Clusters
relates_to:
- target: "[[Jeffrey Dean]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Sanjay Ghemawat]]"
  type: caused_by
  confidence: 0.99
  note: 第二作者
- target: "[[MapReduce]]"
  type: caused
  confidence: 0.99
  note: 首次提出 MapReduce 编程模型
- target: "[[分布式系统]]"
  type: caused
  confidence: 0.9
  note: 奠定了大数据处理的基础
- target: "[[函数式编程]]"
  type: extends
  confidence: 0.85
  note: 从函数式编程中汲取灵感
- target: "[[Backus 函数式编程论文]]"
  type: extends
  confidence: 0.7
  note: 函数式编程思想的工程化
supersedes: null
---

# MapReduce 论文

## 概述

[[Jeffrey Dean]] 和 [[Sanjay Ghemawat]] 于2004年发表的《[[MapReduce]]: Simplified Data Processing on Large Clusters》，提出了极简的大规模数据处理编程模型，开启了大数据时代。

## 关键内容

### 论文信息

| 字段 | 内容 |
|------|------|
| **标题** | [[MapReduce]]: Simplified Data Processing on Large Clusters |
| **作者** | [[Jeffrey Dean]], [[Sanjay Ghemawat]] |
| **发表时间** | 2004年 |
| **会议** | OSDI'04 |
| **所属机构** | [[Google]] |

### 核心贡献

- **[[MapReduce]] 编程模型**：用户只需定义 Map 和 Reduce 两个函数
- **自动并行化**：系统自动将[[计算]]分布到数千台机器
- **透明容错**：[[Worker Agent|Worker]] 故障自动重新调度任务
- **数据本地性优化**：移动[[计算]]而非移动数据

### 历史影响

- [[Google]] 三驾马车之一（GFS、[[MapReduce]]、Bigtable）
- 催生了 Hadoop 生态系统和整个大数据产业
- 2004年一个月内处理了 3.3 PB 输入数据

## 来源

- [[raw/books/计算机科学/19-dean-ghemawat-mapreduce.md]]

## 相关

- [[Jeffrey Dean]] — 第一作者
- [[Sanjay Ghemawat]] — 第二作者
- [[MapReduce]] — 首次提出
- [[分布式系统]] — 奠定的领域
- [[函数式编程]] — 思想来源
- [[Backus 函数式编程论文]] — 函数式思想的先驱
