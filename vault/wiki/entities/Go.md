---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [编程语言, 并发计算, CSP, 计算理论]
aliases: ["Go programming language", "Golang"]
entity_type: tool
relates_to: []
supersedes: null
---

# Go

## 概述
由[[Google]]开发的编程语言，其并发模型直接基于CSP理论，通过[[goroutine]]和[[channel]]实现[[消息传递]]并发。

## 关键内容

1. **CSP实现**：Go的并发模型直接来源于CSP，[[goroutine]]对应CSP的进程，[[channel]]对应CSP的通信通道。

2. **[[goroutine|Goroutine]]**：轻量级线程，可大量创建，独立运行，符合CSP进程中每个进程内部顺序执行的理念。

3. **[[channel|Channel]]**：类型安全的通信通道，默认[[同步通信]]，对应CSP的同步[[消息传递]]机制。

4. **Select语句**：类似CSP的守卫命令，允许在多个[[channel]]操作间进行非确定性选择。

5. **工业影响**：Go语言的成功使CSP理念在现代基础设施中得到广泛应用，Docker、Kubernetes等关键组件均使用Go编写。

6. **官方格言**：Go官方将CSP核心理念总结为"不要通过共享内存来通信，而要通过通信来共享内存"，体现了CSP的深远影响。

## 来源
- [[14-hoare-csp]] — CSP理论对Go的影响分析
- [[]] —

## 相关
- [[Communicating Sequential Processes]] — 并发模型理论基础
- [[goroutine]] — Go的并发执行单元
- [[channel]] — Go的通信机制
- [[C.A.R. Hoare]] — 理论提出者