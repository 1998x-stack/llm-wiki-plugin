---
type: concept
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- CSP
- 通信顺序进程
- Communicating Sequential Processes
relates_to:
- target: "[[Hoare CSP 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次提出
- target: "[[Tony Hoare]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[Go 语言]]"
  type: implements
  confidence: 0.95
  note: goroutine + channel 是 CSP 的实现
- target: "[[Erlang]]"
  type: implements
  confidence: 0.85
  note: 消息传递受 CSP 影响
- target: "[[分布式系统]]"
  type: implements
  confidence: 0.8
  note: 为分布式并发提供理论基础
- target: "[[Actor 模型]]"
  type: compares_to
  confidence: 0.85
  note: 另一种消息传递范式
supersedes: null
---

# CSP 模型

## 概述

CSP（通信顺序进程）是 [[Tony Hoare]] 于1978年提出的并发编程模型：程序由多个独立的顺序进程组成，进程之间通过同步消息传递而非共享内存进行通信。

## 关键内容

### 核心思想

- **进程**：每个进程是严格顺序的，拥有私有状态，不与其他进程共享任何变量
- **同步通信**：发送方和接收方必须同时就绪才能完成通信（"会合"）
- **没有共享状态**：不存在数据竞争、锁、信号量

### 基本命令

- **输出**：`P!e` — 将表达式 e 的值发送给进程 P
- **输入**：`P?x` — 从进程 P 接收一个值，存入变量 x
- **守卫命令**：`guard → command` — 只有守卫为真时命令才可能执行

### 经典示例

- **缓冲进程**：生产者-消费者问题，没有锁
- **素数筛法**：递归进程链实现埃拉托斯特尼筛法
- **哲学家就餐**：用 CSP 解决死锁

### 著名格言

> "Don't communicate by sharing memory; share memory by communicating."
> （不要通过共享内存来通信，而要通过通信来共享内存。）

### 现代实现

- **Go 语言**：goroutine + channel + select
- **Erlang**：轻量级进程 + 消息传递
- **Clojure core.async**：通道和 go 块
- **Rust**：`std::sync::mpsc` 通道

## 来源

- [[raw/books/计算机科学/14-hoare-csp.md]]

## 相关

- [[Hoare CSP 论文]] — 首次提出
- [[Tony Hoare]] — 发明者
- [[Go 语言]] — 当代实现
- [[Erlang]] — 工业验证
- [[分布式系统]] — 应用领域
- [[Actor 模型]] — 另一种消息传递范式
