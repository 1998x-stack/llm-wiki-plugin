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
- 历史
- 计算理论
aliases:
- FORTRAN
- Formula Translation
- 公式翻译
relates_to:
- target: "[[John Backus]]"
  type: caused_by
  confidence: 0.99
  note: 发明者，1954-1957年领导团队开发
- target: "[[FORTRAN 编译器论文]]"
  type: caused_by
  confidence: 0.99
  note: 论文首次系统描述了 FORTRAN 语言及其编译器
- target: "[[编译器优化]]"
  type: depends_on
  confidence: 0.95
  note: FORTRAN 的成功依赖于编译器的优化能力
- target: "[[存储程序计算机]]"
  type: uses
  confidence: 0.9
  note: 运行在存储程序计算机上的第一个成功的高级语言
- target: "[[John Backus]]"
  type: related_to
  confidence: 0.9
  note: IBM 704 上开发，IBM 商业投资
- target: "[[BNF]]"
  type: related_to
  confidence: 0.8
  note: Backus 后来为 ALGOL 发明 BNF，部分源于 FORTRAN 缺乏形式化规范的教训
- target: "[[冯·诺依曼瓶颈]]"
  type: related_to
  confidence: 0.7
  note: FORTRAN 编译器优化试图缓解 CPU-内存带宽瓶颈
- target: "[[Grace Hopper]]"
  type: compares_to
  confidence: 0.75
  note: Hopper 的 A-0 是先驱，FORTRAN 是第一个真正实用的
supersedes: null
---

# FORTRAN

## 概述

FORTRAN（FORmula TRANslation，公式翻译）是世界上第一个广泛使用的高级编程语言，由 John Backus 领导的 IBM 团队于1954-1957年开发，专为科学计算设计。

## 关键内容

### 语言特性

- **算术表达式**：直接书写数学公式 `Y = A*X**2 + B*X + C`
- **DO 循环**：`DO n i = m1, m2, m3`，对应科学计算中最常见的迭代模式
- **算术 IF**：`IF (expression) n1, n2, n3`，根据表达式值的正负零三路分支
- **数组和下标运算**：`DIMENSION` 声明支持矩阵和向量运算
- **子程序和函数**：`SUBROUTINE`、`FUNCTION` 支持代码复用
- **格式化 I/O**：`FORMAT` 和 `READ`/`WRITE` 语句

### 设计哲学

**实用主义**：与后来的 ALGOL 不同，FORTRAN 从不追求理论上的优雅或形式化的完美，每一个特性都直接服务于两个目标——让科学家能自然地表达计算，让编译器能高效地翻译代码。

### 编译器六阶段架构

1. 原始分析与中间表示生成
2. 公共子表达式消除
3. 循环分析
4. 寄存器分配
5. 指令合并与优化
6. 最终代码生成与组装

### 性能

生成的代码效率通常达到手写汇编的 90% 以上，在某些循环为主的程序中甚至优于普通程序员的手写汇编。

### 历史影响

- 开启了高级编程语言时代
- 催生了编译器科学
- 证明了"抽象不等于低效"
- 至今仍是高性能科学计算的主力语言之一
- Backus 因 FORTRAN 和 BNF 获得1977年图灵奖

## 来源

- [[raw/books/计算机科学/04-backus-fortran.md]]

## 相关

- [[John Backus]] — 发明者
- [[FORTRAN 编译器论文]] — 首次系统描述
- [[编译器优化]] — FORTRAN 开创的技术领域
- [[存储程序计算机]] — 运行平台
- IBM — 开发机构
- [[Grace Hopper]] — 先驱
