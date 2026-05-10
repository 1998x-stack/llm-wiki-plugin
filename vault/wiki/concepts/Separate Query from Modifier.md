---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Separate Query from Modifier, 分离查询和修改]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Separate Query from Modifier

## 概述
分离查询和修改是一种[[重构|重构技术]]，将既有返回值又有副作用的函数分离为查询函数和修改函数。

## 关键内容

1. **适用场景**：
   - 函数既返回值又有副作用
   - 查询操作与状态修改混合在一起
   - 难以[[区分]]哪些操作有副作用

2. **实施步骤**：
   - 创建新的查询函数
   - 复制原函数的返回逻辑
   - 修改原函数，让它只负责副作用
   - 替换依赖返回值的调用点
   - 进行测试

3. **实施效果**：
   - 明确哪些操作会产生副作用
   - 提高代码的可预测性
   - 遵循命令查询分离原则

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[副作用]] — relates_to