---
type: entity
entity_type: paper
status: active
confidence: 0.98
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
- Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I
- LISP 论文
- McCarthy 1960 论文
relates_to:
- target: "[[John McCarthy]]"
  type: caused_by
  confidence: 0.99
  note: 唯一作者
- target: "[[LISP]]"
  type: caused
  confidence: 0.99
  note: 论文首次系统描述了 LISP 语言
- target: "[[函数式编程]]"
  type: caused
  confidence: 0.99
  note: 开创了函数式编程范式
- target: "[[λ 演算]]"
  type: extends
  confidence: 0.95
  note: 将 Church 的 λ 演算从理论带入实践
- target: "[[垃圾回收]]"
  type: caused
  confidence: 0.95
  note: 首次在编程语言中引入自动内存管理
- target: "[[S-表达式]]"
  type: caused
  confidence: 0.99
  note: 定义了 LISP 的统一数据表示
- target: "[[同像性]]"
  type: caused
  confidence: 0.95
  note: 程序和数据共享 S-表达式表示
- target: "[[eval 函数]]"
  type: caused
  confidence: 0.99
  note: 论文中用 LISP 自身定义了通用解释器
- target: "[[John Backus]]"
  type: compares_to
  confidence: 0.8
  note: 两人分别开创了函数式和命令式编程范式
- target: "[[FORTRAN]]"
  type: compares_to
  confidence: 0.85
  note: FORTRAN 面向数值计算，LISP 面向符号推理
supersedes: null
---

# LISP 论文

## 概述

[[John McCarthy]] 于1960年发表的《Recursive Functions of [[S-表达式|Symbolic Expression]]s and Their Computation by Machine, Part I》，是[[计算]]机科学史上最具影响力的论文之一，首次系统描述了 LISP 语言，开创了[[函数式编程]][[规范化理论|范式]]。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | Recursive Functions of [[S-表达式|Symbolic Expression]]s and Their Computation by Machine, Part I |
| **作者** | [[John McCarthy]] |
| **发表时间** | 1960年4月 |
| **刊物** | Communications of the ACM, Vol. 3, No. 4, pp. 184-195 |

### 核心贡献

- **[[S-表达式]]**：以原子和有序对递归定义的统一数据表示
- **五个基本函数**：`car`、`cdr`、`cons`、`atom`、`eq`
- **条件表达式**：将 `if-then-else` 从语句提升为表达式
- **递归函数定义**：将递归提升为首选控制结构
- **λ 表达式和高阶函数**：函数成为第一等值
- **[[eval 函数]]**：用不到一页篇幅定义的 LISP 自解释器，被称为"[[计算]]机科学史上最美丽的一页"
- **[[垃圾回收]]**：首次引入[[垃圾回收|自动内存管理]]

### 实现传奇

[[Steve Russell]]（McCarthy 的学生）看到论文中的 `eval` 定义后，直接将其翻译为 [[IBM 704]] 机器码，无意中创造了历史上第一个 LISP 解释器。McCarthy 本人最初认为 `eval` 只是理论定义。

### 历史影响

- 开创了[[函数式编程]][[规范化理论|范式]]
- 1960-1990年代 AI 研究的事实标准语言
- McCarthy 于1971年因 AI 贡献获[[阿兰·图灵|图灵]]奖
- 影响了 JavaScript、[[Python]]、Ruby 等现代语言

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[John McCarthy]] — 作者
- [[LISP]] — 论文描述的语言
- [[函数式编程]] — 开创的范式
- [[λ 演算]] — 理论基础
- [[eval 函数]] — 论文中最优美的贡献
- [[垃圾回收]] — 首次引入
