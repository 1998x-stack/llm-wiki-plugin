---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Replace Primitive with Object, 用对象替换原语]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Replace Primitive with Object

## 概述
用对象替换原语是一种[[重构|重构技术]]，将简单的数据值封装为对象，以便添加更多的行为和控制。

## 关键内容

1. **适用场景**：
   - 数据项需要的不只是简单值
   - 需要为数据添加验证逻辑
   - 数据有相关的业务行为

2. **实施步骤**：
   - 先[[Encapsulate Variable|封装变量]]（[[Encapsulate Variable]]）
   - 创建一个简单的值对象
   - 修改setter，让它创建新实例
   - 修改getter，让它返回值
   - 进行测试
   - 给新类增加更丰富的行为

3. **实施效果**：
   - 将数据和行为封装在一起
   - 提供对数据的有效性验证
   - 使代码更面向对象，更容易扩展

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[值对象]] — relates_to