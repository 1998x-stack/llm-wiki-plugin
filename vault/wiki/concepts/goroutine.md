---
type: entity
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [编程语言概念, Go语言, CSP, 计算理论]
aliases: ["Goroutine"]
relates_to: []
supersedes: null
---

# goroutine

## 概述
Go语言中的轻量级并发执行单元，对应CSP理论中的进程概念。

## 关键内容

1. **CSP对应**：goroutine在Go语言中扮演了CSP理论中"进程"的角色，每个goroutine在自己的空间中独立工作。

2. **轻量特性**：相比[[操作系统]]线程，goroutine非常轻量，可以轻松创建数千甚至数万个而不会耗尽系统资源。

3. **调度机制**：由Go运行时系统调度，使用M:N调度模型（M个goroutine运行在N个[[操作系统]]线程上）。

4. **独立性**：每个goroutine拥有自己的栈空间和执行状态，符合CSP中进程拥有私有状态的设计原则。

5. **通信方式**：goroutine之间通过[[channel]]进行通信，而不是通过共享内存，实现了CSP"不要通过共享内存来通信，而要通过通信来共享内存"的原则。

6. **工程价值**：使Go语言能够高效地处理大量并发任务，成为现代高并发[[服务]]器开发的重要工具。

## 来源
- [[14-hoare-csp]] — CSP理论对goroutine的影响
- [[]] —

## 相关
- [[Go]] — Go语言
- [[channel]] — 通信机制
- [[Communicating Sequential Processes]] — 理论基础
- [[C.A.R. Hoare]] — 理论提出者