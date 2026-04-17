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
- 历史
- 计算理论
aliases:
- C Programming Language
- C 程序设计语言
- C
relates_to:
- target: "[[Dennis Ritchie]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[UNIX]]"
  type: caused
  confidence: 0.95
  note: C 语言是为了编写 UNIX 而发展起来的
- target: "[[Brian Kernighan]]"
  type: related_to
  confidence: 0.9
  note: 《C 程序设计语言》合著者
- target: "[[Dennis Ritchie]]"
  type: related_to
  confidence: 0.85
  note: C 语言来源于 B 语言，B 语言来源于 BCPL
- target: "[[操作系统]]"
  type: implements
  confidence: 0.9
  note: 第一次用高级语言编写操作系统内核
- target: "[[Multics]]"
  type: related_to
  confidence: 0.6
  note: Ritchie 曾参与 Multics 项目
supersedes: null
---

# C 语言

## 概述

C 语言是由 Dennis Ritchie 在1970年代初期设计的一种编程语言，既有高级语言的可读性，又有接近汇编语言的底层控制能力。它是为了编写 UNIX 操作系统而发展起来的，并彻底改变了系统软件的开发方式。

## 关键内容

### 起源

- Thompson 最初使用 B 语言（来源于 BCPL）
- B 语言缺少类型系统和结构体，不适合编写需要直接操控内存的系统软件
- Ritchie 在 B 语言的基础上设计了 C 语言——增加了类型系统、结构体、指针运算等特性

### 重写 UNIX（1973）

- 1973年，Thompson 和 Ritchie 用 C 语言重写了 UNIX 内核
- 这是人类历史上第一次用高级语言编写操作系统内核
- 性能损失约20%（后来的分析显示实际差距更小），但可读性、可维护性和可移植性的提升巨大

### 可移植性

- 用 C 语言重写 UNIX 意味着 UNIX 可以被移植到不同的硬件平台
- 只要为新平台编写一个 C 编译器（以及少量与硬件相关的汇编代码），整个操作系统就可以在新硬件上运行
- 这在操作系统历史上是第一次

### 《C 程序设计语言》

- Ritchie 与 Brian Kernighan 合著的《The C Programming Language》成为 C 语言的权威参考
- 这本书本身也成为了技术写作的典范

### 影响

- C 语言成为了系统编程的事实标准
- 影响了 C++、Java、Python、Go、Rust 等几乎所有后来的编程语言
- 至今仍然是最广泛使用的编程语言之一

## 来源

- [[raw/books/计算机科学/09-ritchie-thompson-unix.md]]

## 相关

- [[Dennis Ritchie]] — 发明者
- [[UNIX]] — C 语言的主要应用
- [[Brian Kernighan]] — 《C 程序设计语言》合著者
- BCPL — C 语言的祖先
- [[操作系统]] — 第一次用高级语言编写内核
- [[Multics]] — Ritchie 曾参与的项目
