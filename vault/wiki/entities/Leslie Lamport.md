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
- Leslie Lamport
- 莱斯利·兰伯特
relates_to:
- target: "[[Lamport 逻辑时钟论文]]"
  type: caused
  confidence: 0.99
  note: 1978年发表
- target: "[[逻辑时钟]]"
  type: caused
  confidence: 0.99
  note: 发明者
- target: "[[happened-before 关系]]"
  type: caused
  confidence: 0.99
  note: 定义者
- target: "[[分布式系统]]"
  type: caused
  confidence: 0.95
  note: 理论奠基者
- target: "[[Paxos]]"
  type: caused
  confidence: 0.95
  note: 共识协议发明者
- target: "[[拜占庭将军问题]]"
  type: caused
  confidence: 0.9
  note: 1982年提出
- target: "[[向量时钟]]"
  type: related_to
  confidence: 0.7
  note: 其逻辑时钟的局限催生了向量时钟
supersedes: null
---

# Leslie Lamport

## 概述

美国[[计算]]机科学家（1941–），[[分布式系统]]理论的奠基者，2013年 ACM [[阿兰·图灵|图灵]]奖得主。发明了[[逻辑时钟]]、拜占庭将军问题、[[Paxos 算法|Paxos]] 共识协议和 TLA+ 规约语言。

## 关键内容

### 逻辑时钟（1978）

- 定义了 [[happened-before 关系|happened-before]] 偏序关系
- 发明了[[逻辑时钟]]机制
- 给出了分布式互斥[[算法]]
- 论文仅8页，被引超过14,000次

### 拜占庭将军问题（1982）

- 形式化了[[分布式系统]]中的容错问题
- 提出了拜占庭容错（BFT）的概念

### Paxos 共识协议（1989/1998）

- 解决了分布式共识问题
- 成为现代[[分布式系统]]的核心组件

### TLA+

- 高级规约语言，用于描述和验证并发和[[分布式系统]]

### 图灵奖（2013）

授奖理由是"对分布式和并发系统的理论与实践做出的根本性贡献"。

### 写作风格

Lamport 以其清晰、简洁、精确的技术写作而广受赞誉。他的论文被视为[[分布式系统]]论文写作的典范。

## 来源

- [[raw/books/计算机科学/13-lamport-time-clocks.md]]

## 相关

- [[Lamport 逻辑时钟论文]] — 1978年发表
- [[逻辑时钟]] — 发明
- [[happened-before 关系]] — 定义
- [[分布式系统]] — 理论奠基
- [[Paxos]] — 共识协议
- [[拜占庭将军问题]] — 1982年提出
- [[向量时钟]] — 后续发展
- [[分布式互斥算法]] — 提出
