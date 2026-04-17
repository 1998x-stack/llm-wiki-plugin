---
type: entity
entity_type: paper
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
- The FORTRAN Automatic Coding System
- FORTRAN 论文
- FORTRAN I 论文
relates_to:
- target: "[[John Backus]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者，FORTRAN 项目负责人
- target: "[[FORTRAN]]"
  type: caused
  confidence: 0.99
  note: 论文描述了 FORTRAN 语言及其编译器的设计
- target: "[[编译器优化]]"
  type: caused
  confidence: 0.95
  note: 论文首次系统描述了公共子表达式消除、循环优化、寄存器分配等技术
- target: "[[冯·诺依曼瓶颈]]"
  type: related_to
  confidence: 0.7
  note: FORTRAN 编译器优化试图缓解 CPU-内存带宽瓶颈
- target: "[[EDVAC 报告]]"
  type: extends
  confidence: 0.8
  note: 在存储程序计算机基础上，进一步解决了"如何编程"的问题
- target: "[[Grace Hopper]]"
  type: compares_to
  confidence: 0.8
  note: Hopper 的 A-0 是最早的编译器雏形，FORTRAN 是第一个真正实用的编译器
supersedes: null
---

# FORTRAN 编译器论文

## 概述

[[John Backus]] 等人于1957年发表的《The [[FORTRAN]] Automatic Coding System》，是编程语言史上第一篇系统描述高级语言编译器设计的论文，证明了编译生成的代码效率可达手写汇编的90%以上。

## 关键内容

### 论文信息

| 项目 | 内容 |
|------|------|
| **标题** | The [[FORTRAN]] Automatic Coding System |
| **作者** | John W. Backus, R.J. Beeber, S. Best 等13人 |
| **发表时间** | 1957年2月 |
| **Venue** | Proceedings of the Western Joint Computer Conference (WJCC), pp. 188-198 |

### 六阶段编译器架构

1. **原始分析与中间表示生成** — 扫描源代码，转换为三元组表示
2. **公共子表达式消除** — 识别重复计算的子表达式
3. **循环分析** — 识别循环结构，确定嵌套深度
4. **寄存器分配** — 智能分配 IBM 704 的三个索引寄存器
5. **指令合并与优化** — 强度削减、利用特殊指令格式
6. **最终代码生成与组装** — 生成可执行目标代码

### 性能数据

[[FORTRAN]] 生成的代码效率通常达到手写汇编的 90% 以上，在某些以循环为主的科学计算程序中甚至优于普通程序员的手写汇编。

### 工程规模

编译器由约 18,000 行 IBM 704 汇编代码组成，是当时最大的软件项目之一。开发耗时近三年（1954年秋至1957年春），团队高峰约20人。

### 历史影响

- 彻底击碎了"编译器不可能高效"的神话
- 1958年底超过半数 IBM 704 用户开始使用 [[FORTRAN]]
- 催生了编译器科学这一全新学科
- Backus 后来因 [[FORTRAN]] 和 BNF 的贡献获得1977年[[阿兰·图灵|图灵]]奖

## 来源

- [[raw/books/计算机科学/04-backus-fortran.md]]

## 相关

- [[John Backus]] — 第一作者，项目负责人
- [[FORTRAN]] — 论文描述的语言
- [[编译器优化]] — 论文开创的技术领域
- [[Grace Hopper]] — 先驱，A-0 系统开发者
