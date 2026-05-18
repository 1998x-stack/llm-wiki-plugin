---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Change Function Declaration, 函数声明变更]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Change Function Declaration

## 概述
变更函数声明是一种[[重构|重构技术]]，通过修改函数名或参数来改善其意图表达和可用性。

## 关键内容

1. **适用场景**：
   - 函数名不能清楚说明其用途
   - 需要修改函数参数
   - 函数接口需要改进以提高易用性

2. **实施步骤（简单情况）**：
   - 删除不需要的参数
   - 修改函数名
   - 添加需要的参数
   - 进行测试

3. **实施步骤（迁移式，适用于复杂改动）**：
   - 确保要删除的参数没有被使用
   - 创建一个新函数，采用新的声明方式
   - 让旧函数调用新函数
   - 进行测试
   - 让调用方逐步改用新函数
   - 每次改动后进行测试
   - 删除旧函数

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[函数命名]] — relates_to