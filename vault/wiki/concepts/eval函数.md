---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags:
  - 技术
  - 编程语言
  - 编译原理
aliases:
  - eval function
  - eval
  - 自解释器
  - 元循环解释器
relates_to:
  - target: "[[LISP]]"
    type: core_component
    confidence: 0.9
  - target: "[[John McCarthy]]"
    type: created_by
    confidence: 0.9
  - target: "[[S-表达式]]"
    type: operates_on
    confidence: 0.9
  - target: "[[同像性]]"
    type: enables
    confidence: 0.9
  - target: "[[λ演算]]"
    type: implements
    confidence: 0.9
  - target: "[[元编程]]"
    type: enables
    confidence: 0.9
supersedes: null
---

# eval函数

## 概述

eval函数是LISP语言中的一个核心函数，它接受一个S-表达式（代表LISP程序）和一个环境（变量绑定），返回该程序的求值结果。eval是LISP的自解释器，能够在不到一页纸的篇幅内定义LISP语言的完整语义。

## 关键内容

1. **核心逻辑**：eval的定义只有大约一页纸的篇幅，却完整地定义了一种图灵完备的编程语言的语义。其核心规则包括：如果表达式是原子则查找其值、如果是quote形式则直接返回、如果是cond形式则求值条件、如果是lambda形式则创建闭包、否则为函数调用。

2. **元循环解释器**：eval被称为元循环解释器，因为它用LISP自身定义了LISP语言的解释器。这种"用自身定义自身"的能力根源于LISP的同像性：程序本身就是S-表达式，而eval是操纵S-表达式的函数。

3. **历史意义**：Alan Kay后来评价eval为"整个计算机科学中最美丽的东西"，并将其比作物理学中的Maxwell方程组。

4. **实现的简洁性**：整个eval的定义只有几条规则，却完整定义了LISP的语义，展示了LISP设计的数学优雅性。

5. **现代影响**：eval的概念在现代编程语言中仍然可见，如JavaScript的eval函数、Python的eval和exec函数等，尽管出于安全考虑通常有所限制。

## 来源

- [[05-mccarthy-lisp]] — 论文分析

## 相关

- [[LISP]] — core_component
- [[John McCarthy]] — created_by
- [[S-表达式]] — operates_on
- [[同像性]] — enables
- [[λ演算]] — implements
- [[元编程]] — enables