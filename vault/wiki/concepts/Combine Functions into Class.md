---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Combine Functions into Class, 组合函数到类]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Combine Functions into Class

## 概述
组合函数到类是一种[[重构|重构技术]]，将操作同一份数据的多个函数组织到一个类中，以提高内聚性。

## 关键内容

1. **适用场景**：
   - 多个函数操作同一份数据
   - 函数和数据分离导致代码分散
   - 需要将相关行为组织在一起

2. **实施步骤**：
   - 对公共数据先进行封装记录（Encapsulate Record）
   - 将每个函数移动到类中
   - 每移动一个函数就进行测试
   - 使用类字段替代数据参数

3. **实施效果**：
   - 将函数与其操作的数据放在同一个地方
   - 提高代码的内聚性
   - 改善代码的[[可维护性]]

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[面向对象编程]] — relates_to