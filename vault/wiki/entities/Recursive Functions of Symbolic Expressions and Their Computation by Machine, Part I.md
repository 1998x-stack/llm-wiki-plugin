---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [技术, 计算机科学, 人工智能, 计算理论]
  - 技术
  - 计算机科学
  - 人工智能
aliases:
  - Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I
  - LISP 论文
  - McCarthy 1960
relates_to:
  - target: "[[John McCarthy]]"
    type: authored
    confidence: 0.9
  - target: "[[LISP]]"
    type: introduces
    confidence: 0.9
  - target: "[[S-表达式]]"
    type: defines
    confidence: 0.9
  - target: "[[eval函数]]"
    type: defines
    confidence: 0.9
  - target: "[[λ演算]]"
    type: builds_upon
    confidence: 0.9
  - target: "[[函数式编程]]"
    type: pioneers
    confidence: 0.9
  - target: "[[垃圾回收]]"
    type: introduces
    confidence: 0.9
supersedes: null
---

# Recursive Functions of Symbolic Expressions and Their Computation by Machine, Part I

## 概述

《Recursive Functions of [[S-表达式|Symbolic Expression]]s and Their Computation by Machine, Part I》是 [[John McCarthy]] 于 1960 年发表在《Communications of the ACM》上的开创性论文。这篇论文介绍了 LISP 编程语言的设计和实现，奠定了[[函数式编程]]的基础。

## 关键内容

1. **LISP语言介绍**：论文介绍了 LISP 编程语言，这是一种以列表处理为核心的语言，引入了递归函数、条件表达式、[[垃圾回收]]和"[[同像性|代码即数据]]"等革命性概念。

2. **[[S-表达式]]定义**：定义了 [[S-表达式]]（[[S-表达式|Symbolic Expression]]s）作为 LISP 的统一数据表示方法，原子是 [[S-表达式]]，如果 e1 和 e2 都是 [[S-表达式]]，则有序对 (e1 · e2) 也是 [[S-表达式]]。

3. **五个基本函数**：定义了 car（取对的第一个元素）、cdr（取对的第二个元素）、cons（构造新的对）、atom（判断是否为原子）、eq（判断两个原子是否相等）。

4. **条件表达式**：引入了 (cond (p1 e1) (p2 e2) ... (pn en)) 的形式，使得递归定义成为可能。

5. **[[eval 函数]]**：论文中最令人惊叹的部分是用 LISP 自身定义了一个通用的 LISP 解释器，这是[[eval 函数|元循环解释器]]的原型。

6. **[[垃圾回收]]机制**：首次在编程语言中引入了[[垃圾回收|自动内存管理]]机制。

7. **[[同像性]]概念**：程序和数据使用相同的表示形式，使得程序可以将其他程序作为数据来处理。

8. **历史意义**：这篇论文开创了[[函数式编程]]范式，对后续几十年的编程语言设计产生了深远影响。

## 来源

- [[05-mccarthy-lisp]] — 原始论文分析

## 相关

- [[John McCarthy]] — author
- [[LISP]] — introduces
- [[S-表达式]] — defines
- [[eval函数]] — defines
- [[λ演算]] — builds_upon
- [[函数式编程]] — pioneers
- [[垃圾回收]] — introduces