---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [编程语言, 并发计算, 消息传递]
aliases: ["Erlang programming language"]
entity_type: tool
relates_to: []
supersedes: null
---

# Erlang

## 概述
由爱立信开发的编程语言，主要用于电信系统，采用消息传递并发模型，受CSP理论深刻影响。

## 关键内容

1. **消息传递并发**：进程之间不共享内存，通过消息传递进行通信，与CSP"避免共享状态"的理念一致。

2. **工业验证**：在爱立信的AXD301交换机中实现了九个九的可用性(99.9999999%)，验证了消息传递并发模型的可靠性。

3. **容错性**："让它崩溃"(let it crash)哲学与CSP的进程独立性思想相呼应，每个进程独立运行，失败不影响整体系统。

4. **大规模应用**：WhatsApp使用Erlang支撑4.5亿用户，仅需少量工程师，展现了消息传递并发模型在大规模系统中的优势。

## 来源
- [[14-hoare-csp]] — CSP对Erlang的影响分析
- [[]] —

## 相关
- [[Communicating Sequential Processes]] — 理论影响来源
- [[Actor Model]] — 相关并发模型
- [[C.A.R. Hoare]] — 理论先驱