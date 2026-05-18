---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Introduce Special Case, 引入特例]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Introduce Special Case

## 概述
引入特例是一种[[重构|重构技术]]，通过返回一个特殊对象来处理特殊情况，从而避免重复的null检查。

## 关键内容

1. **适用场景**：
   - 重复出现null检查
   - 有多种特殊情况需要统一处理
   - 需要简化对特殊值的处理

2. **实施步骤**：
   - 创建一个具备预期接口的特殊情况类
   - 增加isSpecialCase检查
   - 引入工厂方法
   - 用特殊对象替换null检查
   - 进行测试

3. **实施效果**：
   - 消除重复的null检查
   - 提供一致的接口处理特殊情况
   - 简化客户端代码

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[空对象模式]] — relates_to