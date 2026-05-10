---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [programming-language, compiler, numerical-analysis, scientific-computing]
aliases: ["Formula Translation", "FORmula TRANslation", "Fortran"]
relates_to: []
supersedes: null
entity_type: tool
---
<!-- relates_to 示例:
relates_to:
  - target: "[[John Backus]]"
    type: created_by
  - target: "[[IBM 704]]"
    type: runs_on
  - target: "[[Compiler]]"
    type: implements
  - target: "[[ALGOL]]"
    type: predecessor_to
-->

# FORTRAN

## 概述
FORTRAN（Formula Translation）是世界上第一个成功的高级编程语言，由约翰·巴克斯领导的IBM团队于1957年开发，旨在让科学家能够用接近数学公式的方式编写程序。

## 关键内容
1. **开创性意义**：
   - 作为第一个真正实用的高级语言编译器，FORTRAN证明了高级语言可以生成接近手写汇编的高效代码
   - 该语言使科学家无需学习机器码即可与计算机交互，大大降低了编程门槛

2. **关键技术特点**：
   - 支持直接编写数学表达式，如`Y = A*X**2 + B*X + C`
   - DO循环结构专门用于科学计算中最常见的迭代模式
   - 数组和下标运算支持矩阵和向量运算
   - 格式化I/O允许科学家以可读方式输出计算结果

3. **编译器优化创新**：
   - 采用六阶段编译器架构，包含公共子表达式消除、循环不变量外提、强度削减等优化技术
   - 基于循环深度的优化优先级策略，集中资源优化内层循环
   - 智能寄存器分配算法，优先为热点变量分配寄存器

## 来源
- [[The FORTRAN Automatic Coding System]] — 论文基础信息及历史背景
- [[John Backus]] — 主要创造者及技术贡献

## 相关
- [[John Backus]] — created_by
- [[Compiler]] — implements
- [[IBM 704]] — runs_on
- [[Programming Language]] — relates_to