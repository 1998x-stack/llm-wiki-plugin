---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Parameterize Function, 参数化函数]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Parameterize Function

## 概述
参数化函数是一种[[重构|重构技术]]，通过参数化减少做类似事情但数值不同的多个函数。

## 关键内容

1. **适用场景**：
   - 有多个做类似事情但数值不同的函数
   - 存在硬编码的字面值
   - 需要减少代码重复

2. **实施步骤**：
   - 选择一个函数
   - 为变化的字面值增加参数
   - 修改函数体使用该参数
   - 进行测试
   - 让调用方改用参数化版本
   - 删除不再使用的旧函数

3. **实施效果**：
   - 通过参数化减少重复
   - 提高代码的灵活性
   - 便于维护和扩展

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[函数参数]] — relates_to