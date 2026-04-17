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
- Time, Clocks, and the Ordering of Events in a Distributed System
- Lamport 1978 论文
- 逻辑时钟论文
relates_to:
- target: "[[Leslie Lamport]]"
  type: caused_by
  confidence: 0.99
  note: 作者
- target: "[[逻辑时钟]]"
  type: caused
  confidence: 0.99
  note: 首次提出逻辑时钟机制
- target: "[[happened-before 关系]]"
  type: caused
  confidence: 0.99
  note: 首次精确定义
- target: "[[分布式系统]]"
  type: caused
  confidence: 0.95
  note: 奠定了分布式系统理论的基础
- target: "[[向量时钟]]"
  type: caused
  confidence: 0.85
  note: Lamport 时钟的局限催生了向量时钟
- target: "[[TCP-IP]]"
  type: related_to
  confidence: 0.7
  note: 分布式系统运行在 TCP/IP 之上
- target: "[[Paxos]]"
  type: related_to
  confidence: 0.8
  note: Lamport 后续工作
supersedes: null
---

# Lamport 逻辑时钟论文

## 概述

[[Leslie Lamport]] 于1978年发表的《Time, Clocks, and the Ordering of Events in a [[分布式系统|Distributed System]]》，定义了 [[happened-before 关系|happened-before]] 偏序关系和[[逻辑时钟]]机制，奠定了整个[[分布式系统]]理论的基础。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | Time, Clocks, and the Ordering of Events in a [[分布式系统|Distributed System]] |
| **作者** | [[Leslie Lamport]] |
| **发表时间** | 1978年7月 |
| **刊物** | Communications of the ACM, Vol. 21, No. 7, pp. 558-565 |
| **篇幅** | 仅8页 |

### 核心贡献

- **[[happened-before 关系]]（-->）**：由三条规则归纳定义的严格偏序——进程内顺序、消息传递因果、传递性
- **[[逻辑时钟]]**：每个进程维护一个整数计数器，通过 IR1（进程内递增）和 IR2（消息中取最大值+1）保证时钟条件
- **全序扩展**：用进程 ID 打破并发事件的平局，将偏序扩展为全序
- **分布式互斥算法**：基于全序的完全分布式互斥方案

### 历史影响

- 被引用超过14,000次，计算机科学中被引最多的论文之一
- [[happened-before 关系]]成为[[分布式系统]]理论的基本语言
- 直接催生了[[向量时钟]]、因果一致性、因果广播等后续工作
- Lamport 于2013年因此系列工作获得[[阿兰·图灵|图灵]]奖

## 来源

- [[raw/books/计算机科学/13-lamport-time-clocks.md]]

## 相关

- [[Leslie Lamport]] — 作者
- [[逻辑时钟]] — 首次提出
- [[happened-before 关系]] — 首次定义
- [[分布式系统]] — 奠定的领域
- [[向量时钟]] — 后续发展
- [[TCP-IP]] — 运行基础
- [[Paxos]] — Lamport 后续工作
