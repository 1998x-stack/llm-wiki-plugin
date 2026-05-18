---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [compiler-optimization, programming-language, computer-science, C++编程]
aliases: ["Strength Reduction"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[FORTRAN]]"
    type: implemented_in
  - target: "[[Compiler Optimization]]"
    type: part_of
  - target: "[[Loop Invariant Code Motion]]"
    type: related_to
-->

# Strength Reduction

## 概述
强度削减是一种[[编译器优化|编译器优化技术]]，将代价高昂的运算替换为代价较低的等价运算，例如将循环中的乘法替换为加法。

## 关键内容
1. **技术原理**：
   - 将高代价运算替换为低代价的等价运算
   - 例如，将循环中数组A(I)的地址[[计算]]（基地址 + I * 元素大小）优化为每次迭代在上一次结果上加一个常数
   - 避免了循环中的昂贵乘法运算

2. **实现细节**：
   - 在[[FORTRAN]]编译器的第五阶段（指令合并与优化）实现
   - 特别适用于循环结构，因为循环中相同类型的优化可以被重复利用
   - 需要分析循环变量的步长和使用模式才能正确应用

3. **优化效果**：
   - 显著提高循环密集型程序的执行效率
   - 在[[FORTRAN]]编译器中证明了自动优化的有效性
   - 成为后续[[编译器优化]]的标准技术之一

## 来源
- [[The FORTRAN Automatic Coding System]] — 描述了该技术在FORTRAN编译器中的实现

## 相关
- [[FORTRAN]] — implemented_in
- [[Compiler Optimization]] — part_of
- [[Loop Invariant Code Motion]] — related_to
- [[Common Subexpression Elimination]] — relates_to