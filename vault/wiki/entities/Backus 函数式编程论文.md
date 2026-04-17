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
- Can Programming Be Liberated from the von Neumann Style?
- Backus 1978 论文
- 函数式编程论文
relates_to:
- target: "[[John Backus]]"
  type: caused_by
  confidence: 0.99
  note: 作者，1977年图灵奖演讲
- target: "[[函数式编程]]"
  type: caused
  confidence: 0.99
  note: 为函数式编程正名
- target: "[[冯·诺依曼瓶颈]]"
  type: caused
  confidence: 0.95
  note: 首次从思维层面定义冯·诺依曼瓶颈
- target: "[[FORTRAN]]"
  type: contradicts
  confidence: 0.9
  note: FORTRAN 之父批判自己创造的范式
- target: "[[LISP]]"
  type: extends
  confidence: 0.85
  note: 函数式编程的思想源头
- target: "[[MapReduce]]"
  type: caused
  confidence: 0.9
  note: map/reduce 模式的理论源头
- target: "[[Edsger Dijkstra]]"
  type: compares_to
  confidence: 0.7
  note: 同时代对编程范式的深刻反思
supersedes: null
---

# Backus 函数式编程论文

## 概述

[[John Backus]] 于1978年发表的[[阿兰·图灵|图灵]]奖演讲《Can Programming Be Liberated from the von Neumann Style?》，[[FORTRAN]] 之父对自己创造的编程[[规范化理论|范式]]发起系统性批判，提出了[[函数式编程]]（FP）系统和程序代数。

## 关键内容

### 论文信息

| 字段 | 内容 |
|------|------|
| **标题** | Can Programming Be Liberated from the von Neumann Style? A Functional Style and Its Algebra of Programs |
| **作者** | [[John Backus]] |
| **发表时间** | 1978年8月（1977年[[阿兰·图灵|图灵]]奖演讲） |
| **刊物** | Communications of the ACM, Vol. 21, No. 8, pp. 613-641 |

### 核心贡献

- **"[[冯·诺依曼瓶颈]]"概念**：不仅是硬件层面的数据传输限制，更是思维层面的"逐字操作"桎梏
- **FP 系统**：具体的[[函数式编程]]方案，没有变量、没有赋值、没有状态
- **程序代数**：程序服从代数法则，可以像数学表达式一样推理和变换
- **map/reduce 模式**：`alpha f`（映射）和 `/f`（归约），后来成为 [[MapReduce]] 的理论源头

### 历史影响

- 2004年：[[Google]] [[MapReduce]] 在工业规模上验证了 Backus 的核心论点
- [[函数式编程]]获得前所未有的合法性
- 多[[规范化理论|范式]]融合成为现代编程语言的主流

## 来源

- [[raw/books/计算机科学/12-backus-liberated-von-neumann.md]]

## 相关

- [[John Backus]] — 作者
- [[函数式编程]] — 为函数式编程正名
- [[冯·诺依曼瓶颈]] — 从思维层面定义
- [[FORTRAN]] — 批判自己创造的范式
- [[LISP]] — 思想源头
- [[MapReduce]] — map/reduce 模式的源头
- [[Edsger Dijkstra]] — 同时代对编程范式的反思
