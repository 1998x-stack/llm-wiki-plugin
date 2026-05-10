---
type: concept
status: active
confidence: 0.9
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 计算理论
aliases:
- BNF
- Backus-Naur Form
- 巴科斯范式
relates_to:
- target: "[[John Backus]]"
  type: caused_by
  confidence: 0.99
  note: 1959年为 ALGOL 58 发明 Backus 范式
- target: "[[FORTRAN]]"
  type: extends
  confidence: 0.8
  note: BNF 的发明部分源于 FORTRAN 缺乏形式化规范的教训
- target: "[[编译器优化]]"
  type: related_to
  confidence: 0.7
  note: BNF 为编译器的语法分析提供了形式化工具
supersedes: null
---

# BNF

## 概述

BNF（Backus-Naur Form，巴科斯-诺尔[[规范化理论|范式]]）是描述编程语言语法的形式化表示法，由 [[John Backus]] 于1959年为 ALGOL 58 发明，后经 Peter Naur 扩展。

## 关键内容

### 起源

[[FORTRAN]] I 没有形式化的语言规范——语言的语义完全由编译器的行为来定义。当不同厂商开发自己的 [[FORTRAN]] 编译器时，由于缺乏精确的规范，不同实现之间出现了大量不兼容性。这一教训直接推动了 Backus 对形式化方法的追求。

1959年，Backus 为 ALGOL 58 报告发明了 Backus [[规范化理论|范式]]，后经 Peter Naur 扩展为 BNF。BNF 后来成为描述编程语言语法的标准工具，几乎所有现代语言规范都使用 BNF 或其变体。

### 形式

BNF 使用产生式规则描述语言的语法结构：
```
<expression> ::= <term> | <expression> "+" <term>
<term> ::= <factor> | <term> "*" <factor>
```

### 意义

- 从 [[FORTRAN]] 的实践出发、通向 BNF 理论的路径，是工程推动理论发展的经典案例
- BNF 为编译器的语法分析阶段提供了精确的形式化工具
- 现代语言规范（如 C、C++、Java、[[Python]]、Rust）都使用 BNF 或其变体

## 来源

- [[raw/books/计算机科学/04-backus-fortran.md]]

## 相关

- [[John Backus]] — 发明者
- [[FORTRAN]] — 缺乏形式化规范的教训推动了 BNF 的发明
- [[编译器优化]] — BNF 为语法分析提供形式化工具
