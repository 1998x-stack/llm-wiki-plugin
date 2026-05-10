---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Split Phase, 分割阶段]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Split Phase

## 概述
分割阶段是一种[[重构|重构技术]]，将处理不同事物的代码拆分成边界清晰的两个或多个阶段。

## 关键内容

1. **适用场景**：
   - 代码在处理两件或更多不同的事情
   - 单个函数承担了过多职责
   - 需要将复杂逻辑分解为更简单的步骤

2. **实施步骤**：
   - 为第二阶段创建新函数
   - 进行测试
   - 在两个阶段之间引入中间数据结构
   - 进行测试
   - 将第一阶段提取成独立函数
   - 进行测试

3. **实施效果**：
   - 将复杂代码拆分为边界清晰的不同阶段
   - 提高代码的可理解性和[[可维护性]]
   - 使每个阶段的职责更加单一

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[单一职责原则]] — relates_to