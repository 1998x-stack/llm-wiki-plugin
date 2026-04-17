---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- Louis Pouzin
- 路易·普赞
relates_to:
- target: "[[Vinton Cerf]]"
  type: related_to
  confidence: 0.85
  note: CYCLADES 项目启发了 TCP/IP 设计
- target: "[[Robert Kahn]]"
  type: related_to
  confidence: 0.85
  note: CYCLADES 项目启发了 TCP/IP 设计
- target: "[[TCP-IP]]"
  type: caused
  confidence: 0.85
  note: 数据报模型深刻影响了 TCP/IP 的端到端设计
- target: "[[分组交换]]"
  type: related_to
  confidence: 0.8
  note: CYCLADES 是分组交换网络的先驱之一
supersedes: null
---

# Louis Pouzin

## 概述

法国计算机科学家（1931–），CYCLADES 项目的领导者。其数据报（datagram）模型深刻影响了 [[TCP-IP|TCP/IP]] 的端到端设计哲学。

## 关键内容

### CYCLADES 项目

- 1970年代初主持法国 CYCLADES [[分组交换]]网络项目
- 核心理念：网络层应当是无连接的、不可靠的（"数据报"模型）
- 可靠性应由端系统负责，而非中间网络

### 对 TCP/IP 的影响

- Cerf 和 Kahn 明确承认 CYCLADES 对他们的工作产生了重要影响
- "数据报"概念直接启发了 [[TCP-IP|TCP/IP]] 的端到端设计哲学
- 网络是"哑"的、端系统是"智能"的这一思想，在 CYCLADES 中已有雏形

## 来源

- [[raw/books/计算机科学/10-cerf-kahn-tcp-ip.md]]

## 相关

- [[Vinton Cerf]] — 受其 CYCLADES 项目启发
- [[Robert Kahn]] — 受其 CYCLADES 项目启发
- [[TCP-IP]] — 数据报模型影响了设计
- [[分组交换]] — CYCLADES 是先驱之一
