---
type: entity
status: active
confidence: 0.75
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [处理器, 并发计算, 硬件]
aliases: ["INMOS Transputer T9000", "Transputer processor"]
entity_type: tool
relates_to: []
supersedes: null
---

# INMOS Transputer

## 概述
由INMOS公司设计的专门用于并发计算的处理器，其通信机制直接来源于CSP理论。

## 关键内容

1. **CSP实现**：该处理器是专为并发计算设计的，其硬件层面包含了通信通道，直接对应CSP中的通信通道概念。

2. **硬件通信**：处理器内部实现了硬件级的通信机制，使CSP的同步通信理念能够在硬件层面得到直接支持。

3. **occam支持**：专为occam编程语言设计，occam语言的并发原语可以直接映射到Transputer的硬件功能。

4. **安全关键系统应用**：其核心通信协议使用CSP进行形式化验证，应用于需要高可靠性保证的系统中。

## 来源
- [[14-hoare-csp]] — CSP理论对Transputer的影响
- [[]] —

## 相关
- [[Communicating Sequential Processes]] — 理论基础
- [[occam]] — 配套编程语言
- [[C.A.R. Hoare]] — 理论影响