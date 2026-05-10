---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [compiler-optimization, programming-language, computer-science]
aliases: ["Automatic Coding System"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[FORTRAN]]"
    type: implemented_in
  - target: "[[Compiler]]"
    type: category_of
  - target: "[[High-level Programming Language]]"
    type: exemplifies
-->

# Automatic Coding

## 概述
自动编码是指早期计算机时代开发的系统，旨在让程序员使用更接近数学或自然语言的形式编写程序，而非直接使用汇编语言或机器码。

## 关键内容
1. **发展历程**：
   - 在FORTRAN之前已有若干先驱性尝试，如Grace Hopper的A-0系统
   - MIT的Laning和Zierler实现了允许用户直接书写代数表达式的系统
   - 但这些早期系统生成的代码效率极低，通常比手写汇编慢5到10倍

2. **FORTRAN突破**：
   - FORTRAN首次证明了高级语言可以通过优化编译器生成接近手写汇编的高效机器码
   - 项目的核心目标是使科学家能够用数学公式而非机器指令编写程序
   - 同时保证编译器生成的代码效率接近手写汇编

3. **技术挑战**：
   - 面临"编译器不可能高效"的普遍怀疑
   - 在计算资源昂贵的1950年代，任何效率损失都是不可接受的
   - 需要在有限的内存空间（IBM 704仅有约18KB核心存储器）内实现高效的代码优化

## 来源
- [[The FORTRAN Automatic Coding System]] — 详细描述了自动编码的概念及FORTRAN的突破

## 相关
- [[FORTRAN]] — implemented_in
- [[Compiler]] — category_of
- [[High-level Programming Language]] — exemplifies
- [[Programming Language]] — relates_to