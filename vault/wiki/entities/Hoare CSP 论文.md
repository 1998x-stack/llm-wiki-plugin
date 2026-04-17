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
- Communicating Sequential Processes
- Hoare CSP 论文
- CSP 论文
relates_to:
- target: "[[Tony Hoare]]"
  type: caused_by
  confidence: 0.99
  note: 作者
- target: "[[CSP 模型]]"
  type: caused
  confidence: 0.99
  note: 首次提出 CSP 模型
- target: "[[Go 语言]]"
  type: caused
  confidence: 0.9
  note: Go 的并发模型直接来源于 CSP
- target: "[[Erlang]]"
  type: related_to
  confidence: 0.85
  note: Erlang 的消息传递受 CSP 影响
- target: "[[分布式系统]]"
  type: related_to
  confidence: 0.8
  note: CSP 为分布式并发提供了理论基础
- target: "[[Leslie Lamport]]"
  type: compares_to
  confidence: 0.7
  note: 同时代对并发/分布式的深刻思考
supersedes: null
---

# Hoare CSP 论文

## 概述

[[Tony Hoare]] 于1978年发表的《[[CSP 模型|Communicating Sequential Processes]]》，提出了 [[CSP 模型]]——并发程序由多个独立的顺序进程组成，进程之间通过同步消息传递而非共享内存进行通信。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | [[CSP 模型|Communicating Sequential Processes]] |
| **作者** | [[Tony Hoare|C.A.R. Hoare]]（[[Tony Hoare]]） |
| **发表时间** | 1978年8月 |
| **刊物** | Communications of the ACM, Vol. 21, No. 8, pp. 666-677 |
| **引用量** | 超过10,000次 |

### 核心贡献

- **进程（Process）**：每个进程是严格顺序的，拥有私有状态
- **同步通信**：`P!e`（发送）和 `P?x`（接收），通过"会合"（rendezvous）实现
- **守卫命令**：将 [[Edsger Dijkstra|Dijkstra]] 的守卫命令与输入/输出命令结合
- **并行组合**：`[P1 || P2 || ... || Pn]`

### 经典示例

- **缓冲进程**：生产者-消费者问题，没有锁和信号量
- **素数筛法**：用递归进程链实现埃拉托斯特尼筛法
- **哲学家就餐**：用 CSP 解决经典死锁问题

### 历史影响

- 直接影响了 occam、Erlang、Go、Clojure core.async、Rust 等语言
- Go 语言的 goroutine + channel 是 CSP 的当代实现
- 催生了著名格言："不要通过共享内存来通信，而要通过通信来共享内存"

## 来源

- [[raw/books/计算机科学/14-hoare-csp.md]]

## 相关

- [[Tony Hoare]] — 作者
- [[CSP 模型]] — 首次提出
- [[Go 语言]] — CSP 的当代实现
- [[Erlang]] — 受 CSP 影响
- [[分布式系统]] — 应用领域
- [[Leslie Lamport]] — 同时代对并发的思考
