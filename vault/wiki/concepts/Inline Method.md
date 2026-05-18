---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Inline Method, 内联方法]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Inline Method

## 概述
内联方法是一种[[重构|重构技术]]，将方法的内容直接替换其所有调用处，用于消除没有额外价值的方法调用。

## 关键内容

1. **适用场景**：
   - 方法体和方法名一样清楚
   - 方法仅作为多余的转发层存在
   - 方法没有提供足够的抽象价值

2. **实施步骤**：
   - 确认该方法不是多态方法
   - 找到所有调用该方法的位置
   - 用方法体内容替换每个调用点
   - 每次替换后进行测试
   - 删除原方法定义

3. **注意事项**：
   - 必须确保该方法不是多态的，否则可能影响继承体系
   - 替换后需要确保代码逻辑不变
   - 需要在每次修改后测试，保证功能正确性

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Extract Method]] — compares_to