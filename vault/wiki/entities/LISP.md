---
type: entity
entity_type: tool
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags:
  - 技术
  - 编程语言
  - 函数式编程
aliases:
  - LISP
  - Lisp
  - List Processing
relates_to: []
supersedes: null
---

# LISP

## 概述

LISP（LISt Processor）是历史上第一种将函数式编程作为核心范式的编程语言，由 John McCarthy 于 1960 年基于 λ 演算构造。LISP 引入了递归函数、条件表达式、垃圾回收和"代码即数据"等革命性概念。

## 关键内容

1. **S-表达式（Symbolic Expressions）**：LISP 使用统一的数据表示方法，S-表达式既可以表示数据，也可以表示程序。列表 (A B C) 实际是嵌套对 (A . (B . (C . NIL))) 的简写。

2. **五个基本函数**：car（取对的第一个元素）、cdr（取对的第二个元素）、cons（构造新的对）、atom（判断是否为原子）、eq（判断两个原子是否相等）。

3. **条件表达式**：(cond (p1 e1) (p2 e2) ... (pn en)) 使递归定义成为可能，将条件逻辑变为表达式而非语句。

4. **递归函数定义**：递归是 LISP 中最基本、最核心的编程技术，允许函数调用自身。

5. **λ 表达式和高阶函数**：将 Church 的 λ 表达式引入 LISP，使函数成为第一等值，可以被赋给变量、作为参数传递、作为返回值。

6. **eval 函数（自解释器）**：用 LISP 自身定义的通用 LISP 解释器，展示程序操纵程序的能力。

7. **自动垃圾回收**：首次在编程语言中引入自动内存管理机制，程序创建的数据结构可被自动回收。

8. **同像性（Homoiconicity）**：程序和数据使用相同的表示形式（S-表达式），程序可以将其他程序作为数据来创建、修改和执行。

## 来源

- [[05-mccarthy-lisp]] — 论文分析

## 相关

- [[John McCarthy]] — 发明者
- [[S-表达式]] — 核心数据表示
- [[λ演算]] — 理论基础
- [[函数式编程]] — 开创的编程范式
- [[eval函数]] — 核心概念
- [[垃圾回收]] — 首次引入