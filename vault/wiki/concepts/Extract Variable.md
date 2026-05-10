---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Extract Variable, 提取变量]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Extract Variable

## 概述
提取变量是一种[[重构|重构技术]]，为复杂的表达式创建一个变量名，以提高代码的可读性和理解性。

## 关键内容

1. **适用场景**：
   - 复杂表达式难以理解
   - 表达式重复出现
   - 需要为[[计算]]结果提供有意义的名称

2. **实施步骤**：
   - 确保表达式没有副作用
   - 声明一个不可变变量
   - 将表达式结果赋值给变量
   - 用变量替换原表达式
   - 进行测试验证

3. **最佳实践**：
   - 确保提取的表达式没有副作用
   - 变量名应该清楚地反映其含义
   - 使用不可变变量以避免后续修改带来的风险

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Inline Variable]] — compares_to