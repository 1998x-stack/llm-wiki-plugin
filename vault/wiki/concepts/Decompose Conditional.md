---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Decompose Conditional, 分解条件]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Decompose Conditional

## 概述
分解条件是一种[[重构|重构技术]]，将复杂的[[switch语句|条件语句]]分解为更小的部分，使意图更清楚。

## 关键内容

1. **适用场景**：
   - 复杂的[[switch语句|条件语句]]
   - 条件判断和处理逻辑混合在一起
   - 条件表达式难以理解

2. **实施步骤**：
   - 对条件部分使用[[Extract Method|提取方法]]（[[Extract Method]]）
   - 对then分支使用[[Extract Method|提取方法]]（[[Extract Method]]）
   - 对else分支也使用[[Extract Method|提取方法]]（如果有）

3. **实施效果**：
   - 让条件判断和分支行为分离
   - 通过方法名明确表达意图
   - 提高代码的可读性和[[可维护性]]

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Extract Method]] — relates_to