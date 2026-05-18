---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags: [技术, 研究, 计算理论, 概率论]
- 技术
- 研究
- 计算理论
aliases:
- happened-before
- 因果顺序
- 事件偏序
relates_to:
- target: "[[Lamport 逻辑时钟论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次定义
- target: "[[Leslie Lamport]]"
  type: caused_by
  confidence: 0.99
  note: 定义者
- target: "[[逻辑时钟]]"
  type: implements
  confidence: 0.95
  note: 逻辑时钟实现了 happened-before 关系
- target: "[[分布式系统]]"
  type: part_of
  confidence: 0.95
  note: 分布式系统理论的基本语言
- target: "[[向量时钟]]"
  type: extends
  confidence: 0.85
  note: 向量时钟完整捕获了 happened-before 关系
- target: "[[TCP-IP]]"
  type: related_to
  confidence: 0.7
  note: 消息传递基于网络通信
supersedes: null
---

# happened-before 关系

## 概述

happened-before 关系是[[分布式系统]]中事件之间的因果偏序关系，由 [[Leslie Lamport]] 于1978年首次精确定义，是[[分布式系统]]理论的基本语言。

## 关键内容

### 三条定义规则

1. **进程内顺序**：同一进程中，先执行的事件因果上先于后执行的事件
2. **[[消息传递]]因果**：消息的发送事件因果上先于接收事件
3. **传递性**：如果 a --> b 且 b --> c，则 a --> c

### 并发（Concurrency）

如果 a -/-> b 且 b -/-> a（不存在 happened-before 关系），则 a 和 b 是**并发的**。

**关键洞察**：并发不等于同时。两个并发事件之间没有因果关系，它们可能在物理时间上相隔很远。

### 偏序性质

happened-before 是一个**严格偏序**——具有不可[[反身性]]和传递性。之所以是"偏"序，是因为并非所有事件对之间都存在 --> 关系。

### 核心意义

Lamport 将[[分布式系统]]中的"时间"问题还原为"因果关系"问题——我们不需要知道事件的绝对时间，只需要知道它们之间的因果关系。时间只是因果关系的一种不完美的近似。

### 应用

- 一致性模型（因果一致性、顺序一致性、线性一致性）的定义基础
- 分布式调试和追踪
- 复制协议和并发控制
- CRDT 的正确性论证

## 来源

- [[raw/books/计算机科学/13-lamport-time-clocks.md]]

## 相关

- [[Lamport 逻辑时钟论文]] — 首次定义
- [[Leslie Lamport]] — 定义者
- [[逻辑时钟]] — 实现机制
- [[分布式系统]] — 所属领域
- [[向量时钟]] — 完整捕获因果信息
- [[TCP-IP]] — 消息传递基础
- [[分布式互斥算法]] — 应用之一
