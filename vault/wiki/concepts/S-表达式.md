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
- 计算理论
aliases:
- S-Expression
- Symbolic Expression
- 符号表达式
relates_to:
- target: "[[LISP]]"
  type: part_of
  confidence: 0.99
  note: LISP 的统一数据表示
- target: "[[John McCarthy]]"
  type: caused_by
  confidence: 0.95
  note: 设计者
- target: "[[同像性]]"
  type: caused
  confidence: 0.95
  note: S-表达式使程序和数据共享表示成为可能
- target: "[[λ 演算]]"
  type: depends_on
  confidence: 0.8
  note: 递归定义的思想源自 λ 演算
supersedes: null
---

# S-表达式

## 概述

S-表达式（Symbolic Expression，符号表达式）是 LISP 的统一数据表示形式，由原子和有序对递归定义，使程序和数据共享同一种表示成为可能。

## 关键内容

### 定义

仅两条规则：
1. **原子**（atom）是 S-表达式，如 `A`、`B`、`FOO`、`NIL`
2. 如果 $e_1$ 和 $e_2$ 都是 S-表达式，则**有序对** $(e_1 \cdot e_2)$ 也是 S-表达式

**列表**是 S-表达式的特例：`(A . (B . (C . NIL)))` 简写为 `(A B C)`。

### 深刻洞见

S-表达式设计中最深刻的洞见在于：**程序本身也用 S-表达式书写**。函数调用 `(+ 1 2)` 是一个列表，函数定义 `(lambda (x) (* x x))` 同样是一个列表。这意味着 LISP 程序可以像处理普通数据一样处理其他 LISP 程序。

### 同像性（Homoiconicity）

程序与数据共享同一种表示的性质被称为同像性，字面意思是"相同的表示"。它是 LISP 最具哲学深度的特征，也是其强大元编程能力的根源。

### 现代回声

- React 的 JSX 语法在结构上与 S-表达式有深层的同构性
- 深度学习框架中的计算图概念与 S-表达式有着惊人的相似性
- Clojure 等现代 LISP 方言仍然使用 S-表达式

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[LISP]] — 使用 S-表达式的语言
- [[John McCarthy]] — 设计者
- [[同像性]] — S-表达式带来的性质
- [[λ 演算]] — 递归定义的思想来源
