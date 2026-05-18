---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Consolidate Conditional Expression, 合并条件表达式]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Consolidate Conditional Expression

## 概述
合并条件表达式是一种[[重构|重构技术]]，将多个返回相同结果的条件合并为一个，让人一眼看出这些条件其实是一道检查。

## 关键内容

1. **适用场景**：
   - 多个条件最后都返回同一个结果
   - 一系列独立的if语句检查相关条件
   - 条件检查逻辑重复

2. **实施步骤**：
   - 确认条件没有副作用
   - 用and/or操作符合并条件
   - 视情况对合并后的条件使用[[Extract Method|提取方法]]（[[Extract Method]]）

3. **实施效果**：
   - 简化条件逻辑
   - 让相同的检查意图更明显
   - 减少代码重复

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[条件逻辑]] — relates_to