---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- Steve Russell
- 史蒂夫·拉塞尔
relates_to:
- target: "[[John McCarthy]]"
  type: related_to
  confidence: 0.9
  note: McCarthy 的学生
- target: "[[LISP]]"
  type: implements
  confidence: 0.95
  note: 实现了第一个 LISP 解释器
- target: "[[eval 函数]]"
  type: implements
  confidence: 0.95
  note: 将 eval 定义直接翻译为机器码
- target: "[[LISP 论文]]"
  type: extends
  confidence: 0.9
  note: 论文中的 eval 启发他实现了第一个解释器
supersedes: null
---

# Steve Russell

## 概述

美国计算机科学家，[[John McCarthy]] 的学生。1958年将 McCarthy 论文中的 `eval` 定义直接翻译为 IBM 704 机器码，无意中创造了历史上第一个 LISP 解释器。

## 关键内容

### 第一个 LISP 解释器

- 看到 McCarthy 论文中的 `eval` 定义后，意识到它可以直接翻译为机器码
- 于是他就这么做了——创造了历史上第一个 LISP 解释器
- McCarthy 本人最初认为 `eval` 只是一种理论上的定义方式，并没有想到它会被直接实现
- Russell 的这一举动无意中开创了 LISP 的实际实现历史

### 与 McCarthy 的关系

- McCarthy 的学生
- 在 MIT 的 IBM 704 计算机上完成了 LISP 解释器的实现

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[John McCarthy]] — 导师
- [[LISP]] — 实现者
- [[eval 函数]] — 实现来源
- [[LISP 论文]] — 灵感来源
