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
- C.A.R. Hoare
- Tony Hoare
- 托尼·霍尔
- Charles Antony Richard Hoare
relates_to:
- target: "[[Hoare CSP 论文]]"
  type: caused
  confidence: 0.99
  note: 1978年发表
- target: "[[CSP 模型]]"
  type: caused
  confidence: 0.99
  note: 发明者
- target: "[[快速排序]]"
  type: caused
  confidence: 0.95
  note: 1962年发明
- target: "[[Hoare 逻辑]]"
  type: caused
  confidence: 0.95
  note: 1969年提出
- target: "[[Edsger Dijkstra]]"
  type: compares_to
  confidence: 0.8
  note: 同时代对编程范式的深刻反思
- target: "[[Go 语言]]"
  type: caused
  confidence: 0.8
  note: Go 的并发模型来源于 CSP
supersedes: null
---

# Tony Hoare

## 概述

英国计算机科学家（1934–），1980年 ACM [[阿兰·图灵|图灵]]奖得主。发明了快速排序算法（1962）、Hoare 逻辑（1969）和 CSP 并发模型（1978）。

## 关键内容

### 快速排序（1962）

- 发明了快速排序算法
- 至今仍是使用最广泛的排序算法之一

### Hoare 逻辑（1969）

- 用公理化方法推理程序正确性的框架
- 为形式化验证奠定了基础

### CSP 模型（1978）

- 提出"[[CSP 模型|通信顺序进程]]"模型
- 将并发编程从"共享内存+锁"转变为"消息传递"
- 催生了著名格言："不要通过共享内存来通信，而要通过通信来共享内存"

### 图灵奖（1980）

授奖理由是"对编程语言的定义和设计做出的根本性贡献"。

### 后续影响

- 1985年出版专著 *[[CSP 模型|Communicating Sequential Processes]]*
- CSP 影响了 occam、Erlang、Go、Clojure core.async、Rust 等语言
- Go 语言的设计者 Rob Pike 明确表示 Go 的并发模型直接来源于 CSP

## 来源

- [[raw/books/计算机科学/14-hoare-csp.md]]

## 相关

- [[Hoare CSP 论文]] — 1978年发表
- [[CSP 模型]] — 发明
- [[快速排序]] — 1962年发明
- [[Hoare 逻辑]] — 1969年提出
- [[Edsger Dijkstra]] — 同时代反思
- [[Go 语言]] — CSP 的当代实现
