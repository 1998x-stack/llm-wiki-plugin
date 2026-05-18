---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Replace Temp with Query, 用查询替换临时变量]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Replace Temp with Query

## 概述
用查询替换临时变量是一种[[重构|重构技术]]，将临时变量替换为一个查询函数，使代码更清晰。

## 关键内容

1. **适用场景**：
   - 临时变量保存的是一个表达式的结果
   - 临时变量在多处被使用
   - 表达式[[计算]]逻辑较为复杂

2. **实施步骤**：
   - 确保变量只被赋值一次
   - 把赋值右边的表达式提取成一个方法
   - 用方法调用替换临时变量引用
   - 进行测试
   - 删除临时变量声明和赋值

3. **实施效果**：
   - 提高代码的可读性
   - 通过方法名明确表达意图
   - 避免临时变量的重复使用

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Extract Method]] — relates_to