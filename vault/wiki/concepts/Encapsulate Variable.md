---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Encapsulate Variable, 封装变量]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Encapsulate Variable

## 概述
封装变量是一种[[重构|重构技术]]，通过创建访问器方法来控制对数据的访问，从而提供更好的封装性。

## 关键内容

1. **适用场景**：
   - 多个地方直接访问某个数据
   - 需要控制对数据的访问[[Permissions|权限]]
   - 数据访问需要增加逻辑或验证

2. **实施步骤**：
   - 创建getter和setter方法
   - 找到所有对变量的直接引用
   - 用getter替换读取操作
   - 用setter替换写入操作
   - 每次改动后进行测试
   - 降低原始变量的可见性

3. **实施效果**：
   - 提供对数据访问的统一入口
   - 可以在访问器中添加验证或其他逻辑
   - 更好地控制数据的变化

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[数据封装]] — relates_to