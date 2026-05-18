---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [编程语言, 系统编程, 计算机科学, 推荐系统]
aliases: [C Programming Language, C, C程序设计语言]
entity_type: tool
relates_to:
  - target: "[[Dennis Ritchie]]"
    type: invented_by
    confidence: 0.99
  - target: "[[Ken Thompson]]"
    type: influenced_by
    confidence: 0.85
  - target: "[[B语言]]"
    type: evolved_from
    confidence: 0.9
  - target: "[[BCPL语言]]"
    type: evolved_from
    confidence: 0.85
  - target: "[[UNIX]]"
    type: used_for_implementing
    confidence: 0.99
  - target: "[[系统编程]]"
    type: enables
    confidence: 0.95
  - target: "[[操作系统]]"
    type: used_for_implementing
    confidence: 0.9
supersedes: null
---

# C语言

## 概述
C语言是由[[Dennis Ritchie]]在[[贝尔实验室]]开发的高级编程语言，因其接近硬件的控制能力和良好的可移植性，成为系统编程的首选语言，广泛用于[[操作系统]]、嵌入式系统和高性能[[计算]]领域。

## 关键内容
1. **为UNIX而生**：C语言最初是为了编写UNIX[[操作系统]]而设计的，Ritchie在B语言（来源于BCPL）的基础上发展了C语言，增加了类型系统、结构体、指针运算等特性。

2. **高级语言与底层控制的平衡**：C语言既有高级语言的可读性，又有接近汇编语言的底层控制能力，使得程序员可以直接操控内存和硬件资源。

3. **可移植性革命**：用C语言重写UNIX打破了"[[操作系统]]必须用汇编语言编写"的偏见，使得[[操作系统]]可以相对容易地移植到不同的硬件平台。

4. **影响深远的设计**：C语言的语法和设计理念影响了后续几乎所有主流编程语言，包括C++、Java、C#、JavaScript等。

## 来源
- [[09-ritchie-thompson-unix]] — 论文分析
- [[UNIX]] — 应用背景

## 相关
- [[Dennis Ritchie]] — invented_by
- [[UNIX]] — used_for_implementing
- [[B语言]] — evolved_from
- [[BCPL语言]] — evolved_from
- [[系统编程]] — enables