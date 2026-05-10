---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [compiler-optimization, programming-language, computer-science]
aliases: ["Loop-Invariant Code Motion"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[FORTRAN]]"
    type: implemented_in
  - target: "[[Compiler Optimization]]"
    type: part_of
  - target: "[[Common Subexpression Elimination]]"
    type: related_to
-->

# Loop Invariant Code Motion

## 概述
循环不变量外提是一种编译器优化技术，将循环体内值在循环执行期间不会改变的表达式计算移到循环之前，只执行一次。

## 关键内容
1. **技术原理**：
   - 识别循环体内使用但未被修改的表达式（如循环体内使用N+1但N在循环中未被修改）
   - 将这些不变的计算从循环内部移出到循环之前
   - 在循环迭代次数较多时，可显著减少冗余计算

2. **实现细节**：
   - 是FORTRAN编译器实现的重要循环优化之一
   - 在迭代万次的循环中，这意味着节省了9999次冗余计算
   - 体现了FORTRAN团队对科学计算特点的深刻理解

3. **应用场景**：
   - 特别适用于科学计算程序，这类程序的绝大部分执行时间花在循环中
   - 在FORTRAN的六阶段编译器架构中专门用于循环分析和优化
   - 为后续编译器优化研究提供了重要启示

## 来源
- [[The FORTRAN Automatic Coding System]] — 描述了该技术在FORTRAN编译器中的实现

## 相关
- [[FORTRAN]] — implemented_in
- [[Compiler Optimization]] — part_of
- [[Common Subexpression Elimination]] — related_to
- [[Strength Reduction]] — relates_to