---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Move Field, 移动字段]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Move Field

## 概述
移动字段是一种[[重构|重构技术]]，将更多被另一个类使用的字段移动到那个类中。

## 关键内容

1. **适用场景**：
   - 字段更多被另一个类使用
   - 字段与当前类的职责不够紧密
   - 字段和使用它的方法分布在不同类中

2. **实施步骤**：
   - 如果还没有封装，先封装字段
   - 进行测试
   - 在目标类中创建字段
   - 把引用改成使用目标字段
   - 进行测试
   - 删除原字段

3. **实施效果**：
   - 让数据和使用它的函数靠在一起
   - 改善类的内聚性
   - 符合数据和行为应该在一起的设计原则

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Move Method]] — relates_to