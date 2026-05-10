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
- Edsger Wybe Dijkstra
- 艾兹格·迪杰斯特拉
- Dijkstra
relates_to:
- target: "[[Go To Statement Considered Harmful 论文]]"
  type: caused
  confidence: 0.99
  note: 1968年发表
- target: "[[结构化编程]]"
  type: caused
  confidence: 0.99
  note: 开创者
- target: "[[软件危机]]"
  type: related_to
  confidence: 0.85
  note: 论文发表的时代背景
- target: "[[Bohm-Jacopini 定理]]"
  type: extends
  confidence: 0.9
  note: 为结构化编程提供了理论基础
- target: "[[John Backus]]"
  type: compares_to
  confidence: 0.8
  note: Backus 1977年演讲批评冯诺依曼范式，Dijkstra 1968年批评 goto
- target: "[[函数式编程]]"
  type: related_to
  confidence: 0.8
  note: 晚年越来越倾向于函数式思维方式
- target: "[[LISP]]"
  type: compares_to
  confidence: 0.7
  note: LISP 天然支持结构化控制流
supersedes: null
---

# Edsger Dijkstra

## 概述

荷兰[[计算]]机科学家（1930–2002），1972年[[阿兰·图灵|图灵]]奖得主。1968年发表《[[Go To Statement Considered Harmful 论文|Go To Statement Considered Harmful]]》开创了[[结构化编程]]运动，对编程语言设计和软件工程方法论产生了深远影响。

## 关键内容

### 主要贡献

- **最短路径[[算法]]**（1956年）— 以他名字命名的 Dijkstra [[算法]]
- **ALGOL 60 语言设计** — 参与设计并开发了首个 ALGOL 60 编译器
- **信号量**（semaphore）— 解决并发编程中的同步问题
- **[[结构化编程]]** — 1968年论文开创了整个运动
- **最弱前置条件**（weakest precondition）— 程序推导和验证的理论框架

### Go To Statement Considered Harmful（1968）

- 以编辑来信形式发表，不到两页
- 原标题为"[[Go To Statement Considered Harmful 论文|A Case against the GO TO Statement]]"，被编辑 Niklaus Wirth 改为更具争议性的形式
- 论证了 goto 语句破坏了程序文本与执行过程之间的结构化对应关系
- 开创了"X Considered Harmful"的学术批评文体

### 图灵奖（1972）

获奖理由是"对编程作为一种高度智力挑战活动的基础性贡献"。

### 哲学立场

Dijkstra 的核心洞察是：程序应当被设计为可以被人类理解的。他将编程从一种试错的手艺提升为一种可推理的智识活动。晚年越来越倾向于函数式的思维方式。

### 名言

> "测试只能证明 bug 的存在，不能证明 bug 的不存在。"
> （"Testing shows the presence, not the absence of bugs."）

## 来源

- [[raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md]]

## 相关

- [[Go To Statement Considered Harmful 论文]] — 1968年发表
- [[结构化编程]] — 开创的运动
- [[软件危机]] — 时代背景
- [[John Backus]] — 分别批评了 goto 和冯诺依曼范式
- [[函数式编程]] — 晚年倾向的思维方式
