---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [compiler-optimization, programming-language, computer-science]
aliases: ["Common Subexpression Elimination", "CSE"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[FORTRAN]]"
    type: implemented_in
  - target: "[[Compiler Optimization]]"
    type: part_of
  - target: "[[Loop Optimization]]"
    type: related_to
-->

# Common Subexpression Elimination

## 概述
公共子表达式消除是一种编译器优化技术，用于识别并消除程序中重复计算的子表达式，将重复的计算替换为对先前计算结果的引用。

## 关键内容
1. **技术原理**：
   - 扫描程序的中间表示，识别在同一基本块内被重复计算的子表达式
   - 将后续的相同计算替换为对首次计算结果的引用
   - 减少了不必要的重复计算，提高了代码效率

2. **实现细节**：
   - 在FORTRAN编译器的第二阶段实施，是编译器的第一个优化阶段
   - 例如，如果代码中出现A(I) + B(I)和A(I) * C，编译器会识别出A(I)的地址计算是重复的，只执行一次
   - 这项技术至今仍是所有优化编译器的标准步骤

3. **历史意义**：
   - 首次在实用系统中实现的关键优化技术之一
   - 为后续的编译器优化研究奠定了基础
   - 在FORTRAN编译器中证明了优化技术的实际价值

## 来源
- [[The FORTRAN Automatic Coding System]] — 描述了该技术在FORTRAN编译器中的实现

## 相关
- [[FORTRAN]] — implemented_in
- [[Compiler Optimization]] — part_of
- [[Loop Optimization]] — related_to
- [[Optimizing Compiler]] — relates_to