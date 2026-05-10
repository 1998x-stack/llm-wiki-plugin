---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags:
- 技术
- 研究
- 数学
- 信息论
aliases:
- Berry Paradox
- 贝里悖论
relates_to:
- target: '[[柯尔莫哥洛夫复杂性]]'
  type: related_to
  confidence: 0.9
- target: '[[格雷戈里·柴廷]]'
  type: related_to
  confidence: 0.9
- target: '[[算法信息论]]'
  type: part_of
  confidence: 0.85
- target: '[[停机问题]]'
  type: related_to
  confidence: 0.85
supersedes: null
---

# Berry悖论

## 概述

Berry 悖论（1906）是"最小的不能用二十个英文单词定义的正整数"——这个描述本身只用了不到二十个词。Chaitin 将其形式化为 [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 复杂性不可[[计算]]性的证明。

## 关键内容

### 原始悖论

> "The smallest positive integer not definable in under twenty English words."

这个短语本身只用了 14 个英文单词，却定义了一个"不能用少于 20 个单词定义的数"——自相矛盾。

### Chaitin 的形式化

Chaitin 将 Berry 悖论转化为严格的数学定理：

假设存在程序 P 能[[计算]] [[安德烈·柯尔莫哥洛夫|Kolmogorov]] 复杂性 I(x)。构造程序 Q：
- 枚举所有字符串 x，对每个[[计算]] I(x)
- 输出第一个满足 I(x) ≥ N 的 x

Q 的长度约 |P| + log N，但它输出了一个"复杂度应该 ≥ N"的字符串。当 N 足够大时，|P| + log N < N——矛盾！

### 意义

Berry 悖论不是逻辑的 bug，而是 feature——它揭示了**形式系统的[[信息论]]极限**：一个复杂性有限的形式系统不能证明某个字符串具有超过系统自身复杂性的复杂性。

### 与 Gödel 不完备定理的关系

Chaitin 用 Berry 悖论的形式化给出了 Gödel 不完备定理的[[信息论]]版本：
- Gödel 版：存在真但不可证的命题（源于自指与对角化）
- Chaitin 版：存在复杂但无法被证明复杂的字符串（源于公理系统的信息量有限）

## 来源

- [[raw/books/信息论/10_chaitin_1966_length_of_programs.md]] — Chaitin (1966) 深度解析

## 相关

- [[柯尔莫哥洛夫复杂性]] — 形式化的目标
- [[格雷戈里·柴廷]] — 形式化者
- [[算法信息论]] — 所属学科
- [[停机问题]] — 不可计算性的根源
