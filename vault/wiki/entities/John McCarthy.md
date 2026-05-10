---
type: entity
entity_type: person
status: active
confidence: 0.95
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 历史
- 研究
aliases:
- John McCarthy
- 约翰·麦卡锡
relates_to:
- target: "[[LISP]]"
  type: caused
  confidence: 0.99
  note: 发明者
- target: "[[LISP 论文]]"
  type: caused
  confidence: 0.99
  note: 1960年发表
- target: "[[函数式编程]]"
  type: caused
  confidence: 0.95
  note: 开创者
- target: "[[λ 演算]]"
  type: extends
  confidence: 0.9
  note: 将 Church 的 λ 演算引入编程语言实践
- target: "[[垃圾回收]]"
  type: caused
  confidence: 0.95
  note: 首次在编程语言中引入
- target: "[[John McCarthy]]"
  type: related_to
  confidence: 0.9
  note: 1956年达特茅斯会议上正式提出"人工智能"术语
- target: "[[John Backus]]"
  type: compares_to
  confidence: 0.8
  note: 分别开创函数式和命令式编程范式
- target: "[[FORTRAN]]"
  type: compares_to
  confidence: 0.75
  note: FORTRAN 面向数值计算，McCarthy 的 LISP 面向符号推理
supersedes: null
---

# John McCarthy

## 概述

美国[[计算]]机科学家（1927–2011），LISP 编程语言发明者，1956年达特茅斯会议上正式提出"人工智能"术语。1971年因 AI 领域开创性贡献获得 ACM [[阿兰·图灵|图灵]]奖。

## 关键内容

### LISP（1960）

- 基于 Church 的 [[λ 演算]]设计了 LISP 语言
- 引入了递归函数、条件表达式、[[垃圾回收]]和"[[同像性|代码即数据]]"等革命性概念
- 论文中用不到一页篇幅给出了 LISP 的自解释器 `eval`
- LISP 成为1960-1990年代 AI 研究的事实标准语言

### 人工智能

- 1956年夏天在达特茅斯学院会议上正式提出"人工智能"术语
- 与会者包括 [[Marvin Minsky|Minsky]]、Shannon、Simon 等日后的领军人物
- 在 MIT 主持人工智能项目（后来发展为 MIT AI Lab）

### 理论洞见

McCarthy 证明了编程语言可以从纯粹的数学理论出发来设计，而不必受制于硬件的偶然特性。这种"自上而下"的语言设计哲学影响了此后的 ML、Haskell、Prolog 等语言。

### 图灵奖（1971）

授奖理由是他在人工智能领域的开创性贡献。LISP 的设计是这些贡献中最持久的一项——半个多世纪后，LISP 的核心思想仍然活跃在现代编程实践中。

## 来源

- [[raw/books/计算机科学/05-mccarthy-lisp.md]]

## 相关

- [[LISP]] — 发明
- [[LISP 论文]] — 1960年发表
- [[函数式编程]] — 开创的范式
- 人工智能 — 术语提出者
- [[λ 演算]] — 理论基础来源
- [[垃圾回收]] — 首次引入
