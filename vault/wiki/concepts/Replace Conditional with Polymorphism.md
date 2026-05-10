---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Replace Conditional with Polymorphism, 用多态替换条件]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Replace Conditional with Polymorphism

## 概述
用多态替换条件是一种[[重构|重构技术]]，通过对象自己处理自己的行为来替换按类型分支的switch/条件逻辑。

## 关键内容

1. **适用场景**：
   - 按类型分支的switch/条件逻辑
   - 基于类型的条件判断
   - 当需要根据不同类型执行不同行为时

2. **实施步骤**：
   - 创建类层次（如果还没有）
   - 用工厂函数创建对象
   - 把条件逻辑移到超类方法里
   - 给每种情况创建子类方法
   - 删除原条件

3. **实施效果**：
   - 让对象自己处理自己的行为
   - 遵循[[SOLID原则|开闭原则]]（对扩展开放，对修改封闭）
   - 使代码更易于扩展新的类型

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[多态]] — relates_to