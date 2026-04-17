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
- LISP
- LISt Processor
- Lisp
relates_to:
- target: "[[John McCarthy]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[LISP 论文]]"
  type: caused_by
  confidence: 0.99
  note: 首次系统描述
- target: "[[函数式编程]]"
  type: implements
  confidence: 0.99
  note: 第一个函数式编程语言
- target: "[[λ 演算]]"
  type: depends_on
  confidence: 0.95
  note: 理论基础
- target: "[[S-表达式]]"
  type: depends_on
  confidence: 0.99
  note: 统一的数据和程序表示
- target: "[[垃圾回收]]"
  type: implements
  confidence: 0.95
  note: 首次引入自动内存管理
- target: "[[同像性]]"
  type: implements
  confidence: 0.95
  note: 程序和数据共享 S-表达式
- target: "[[eval 函数]]"
  type: implements
  confidence: 0.99
  note: 自解释器
- target: "[[FORTRAN]]"
  type: compares_to
  confidence: 0.85
  note: FORTRAN 面向数值计算，LISP 面向符号推理
- target: "[[John McCarthy]]"
  type: related_to
  confidence: 0.9
  note: 1960-1990年代 AI 研究的标准语言
supersedes: null
---

# LISP

## 概述

LISP（LISt Processor）是世界上第二古老的高级编程语言（仅次于 [[FORTRAN]]），由 [[John McCarthy]] 于1958-1960年设计，基于 [[λ 演算]]，开创了[[函数式编程]][[规范化理论|范式]]。

## 关键内容

### 核心特性

- **[[S-表达式]]**：以原子和有序对递归定义的统一数据表示，程序和数据使用相同格式
- **五个基本函数**：`car`（取第一个元素）、`cdr`（取剩余元素）、`cons`（构造对）、`atom`（判断原子）、`eq`（判断相等）
- **条件表达式**：`(cond (p1 e1) (p2 e2) ...)` 将条件逻辑变为可嵌套的表达式
- **递归**：首选控制结构，天然适合树搜索、模式匹配和结构归纳
- **λ 表达式**：函数成为第一等值，支持高阶函数
- **[[eval 函数]]**：用 LISP 自身定义的通用解释器，不到一页代码
- **[[垃圾回收]]**：首次引入[[垃圾回收|自动内存管理]]

### 设计哲学

LISP 是"自上而下"设计的——从纯粹的数学理论（[[λ 演算]]）出发，而非从硬件特性出发。这与 [[FORTRAN]] 的"自下而上"设计形成鲜明对比。

### 方言谱系

- **Scheme**（1975）：精简和纯化，引入词法作用域
- **Common Lisp**（1984）：标准化版本
- **Clojure**（2007）：JVM 上的现代复兴
- **Emacs Lisp**：GNU Emacs 的扩展语言

### 历史影响

- 1960-1990年代 AI 研究的事实标准语言
- [[函数式编程]]的源头，影响了 JavaScript、Python、Ruby 等现代语言
- [[同像性]]催生了宏系统，使 LISP 在元编程领域无可匹敌

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[John McCarthy]] — 发明者
- [[LISP 论文]] — 首次系统描述
- [[函数式编程]] — 开创的范式
- [[λ 演算]] — 理论基础
- [[S-表达式]] — 数据表示
- [[垃圾回收]] — 首次引入
- [[eval 函数]] — 自解释器
