---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Replace Subclass with Delegate, 用委托替换子类]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Replace Subclass with Delegate

## 概述
用委托替换子类是一种[[重构|重构技术]]，在合适的地方使用组合而不是继承来实现功能。

## 关键内容

1. **适用场景**：
   - 继承用得不对
   - 需要更灵活的解决方案
   - 继承关系过于僵化

2. **实施步骤**：
   - 创建一个空的委托类
   - 在宿主类中加一个持有委托的字段
   - 在宿主类构造委托
   - 把功能迁移到委托类
   - 每次迁移后测试
   - 用委托替代继承

3. **实施效果**：
   - 提供比继承更灵活的设计
   - 在运行时可以动态改变行为
   - 遵循组合优于继承的原则

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[组合优于继承]] — relates_to