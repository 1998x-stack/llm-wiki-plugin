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
- eval
- Meta-circular Interpreter
- 元循环解释器
relates_to:
- target: "[[LISP]]"
  type: part_of
  confidence: 0.99
  note: LISP 的自解释器
- target: "[[John McCarthy]]"
  type: caused_by
  confidence: 0.99
  note: 定义者
- target: "[[LISP 论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文中首次定义
- target: "[[同像性]]"
  type: depends_on
  confidence: 0.95
  note: eval 之所以可能，根本原因在于 LISP 的同像性
- target: "[[S-表达式]]"
  type: depends_on
  confidence: 0.9
  note: eval 操纵 S-表达式
- target: "[[Steve Russell]]"
  type: implements
  confidence: 0.9
  note: 将 eval 定义直接翻译为机器码
supersedes: null
---

# eval 函数

## 概述

eval 是 McCarthy 在1960年 LISP 论文中用 LISP 自身定义的通用解释器。它接受一个 S-表达式（代表 LISP 程序）和一个环境，返回该程序的求值结果。不到一页篇幅的定义被称为"计算机科学史上最美丽的一页"。

## 关键内容

### 核心逻辑

1. 如果表达式是原子，在环境中查找它的值
2. 如果表达式是 `(quote x)` 形式，直接返回 `x`（不求值）
3. 如果表达式是 `(cond ...)` 形式，依次求值条件
4. 如果表达式是 `(lambda ...)` 形式，创建一个闭包
5. 否则，表达式是函数调用 `(f a1 a2 ...)`——求值函数和参数，将函数应用于参数

### 为什么美丽

- 整个定义只有大约一页纸，却完整地定义了一种图灵完备语言的语义
- Alan Kay 评价："这是整个计算机科学中最美丽的东西......Maxwell 方程组之于物理学，如同 eval 之于计算机科学。"
- 这种"用自身定义自身"的解释器后来被称为**元循环解释器**（meta-circular interpreter）

### 实现传奇

Steve Russell（McCarthy 的学生）看到论文中的 eval 定义后，意识到它可以直接翻译为机器码——于是他就这么做了。McCarthy 本人最初认为 eval 只是理论定义，没想到它会被直接实现。

### 现代回声

大语言模型（LLM）根据自然语言描述生成代码的能力，在结构上类似于 eval——接受一种表示（自然语言），生成另一种表示（可执行代码），然后执行它。

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[LISP]] — eval 定义的语言
- [[John McCarthy]] — 定义者
- [[LISP 论文]] — 首次定义
- [[同像性]] — eval 之所以可能的基础
- [[S-表达式]] — eval 操纵的数据格式
- [[Steve Russell]] — 第一个实现者
