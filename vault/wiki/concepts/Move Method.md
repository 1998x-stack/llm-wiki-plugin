---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Move Method, 移动方法]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Move Method

## 概述
移动方法是一种[[重构|重构技术]]，将更多依赖于另一个类数据的方法移动到那个类中。

## 关键内容

1. **适用场景**：
   - 方法更依赖另一个类的数据而不是自己类的数据
   - 方法频繁访问另一个类的私有成员
   - 违反了数据和行为应该在一起的原则

2. **实施步骤**：
   - 检查方法使用到的所有程序元素
   - 确认方法不是多态的
   - 把方法复制到目标类
   - 调整上下文
   - 让原方法委托给目标方法
   - 进行测试
   - 视情况删除原方法

3. **实施效果**：
   - 改善类的内聚性
   - 使代码结构更加合理
   - 符合数据和行为应该在一起的设计原则

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Move Field]] — relates_to