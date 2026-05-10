---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Remove Flag Argument, 移除标志参数]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Remove Flag Argument

## 概述
移除标志参数是一种[[重构|重构技术]]，通过拆分成明确函数来替代使用布尔参数改变函数行为的做法。

## 关键内容

1. **适用场景**：
   - 布尔参数改变函数行为
   - 函数根据标志参数执行不同逻辑
   - 标志参数降低了代码可读性

2. **实施步骤**：
   - 针对不同标志值创建显式函数
   - 替换每个调用点
   - 每次改动后进行测试
   - 删除原函数

3. **实施效果**：
   - 让行为更清楚明确
   - 提高代码的可读性
   - 消除基于布尔值的条件逻辑

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[函数参数]] — relates_to