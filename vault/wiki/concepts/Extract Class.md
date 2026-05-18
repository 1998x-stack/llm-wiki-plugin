---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Extract Class, 提取类]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Extract Class

## 概述
提取类是一种[[重构|重构技术]]，将[[大类]]中具有不同职责的部分拆分到新的类中，以维持[[SOLID原则|单一职责原则]]。

## 关键内容

1. **适用场景**：
   - [[大类]]里有多个职责
   - 类变得过于庞大和复杂
   - 违反[[SOLID原则|单一职责原则]]

2. **实施步骤**：
   - 决定如何拆分职责
   - 创建新类
   - 把字段从原类移到新类
   - 进行测试
   - 把方法从原类移到新类
   - 每次移动后测试
   - 重新检查并命名两个类
   - 决定如何暴露新类

3. **实施效果**：
   - 拆分类以维持单一职责
   - 提高代码的[[可维护性]]
   - 使类的结构更清晰

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[单一职责原则]] — relates_to