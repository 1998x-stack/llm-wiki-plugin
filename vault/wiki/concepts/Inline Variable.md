---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化]
aliases: [Inline Variable, 内联变量]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Inline Variable

## 概述
内联变量是一种[[重构|重构技术]]，将变量替换为其初始值表达式，用于移除没有提供更多价值的中间变量。

## 关键内容

1. **适用场景**：
   - 变量名没有比表达式本身更清楚
   - 变量仅作为不必要的间接层存在
   - 变量的使用没有提供额外的语义价值

2. **实施步骤**：
   - 检查右侧表达式没有副作用
   - 如果变量不是不可变的，先改成不可变并测试
   - 找到第一次引用并替换成表达式
   - 进行测试
   - 对所有引用重复上述过程
   - 删除变量声明和赋值
   - 再次测试

3. **注意事项**：
   - 必须确保替换不会引入副作用
   - 需要在每次修改后测试
   - 确保表达式在多个使用点的行为一致

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Extract Variable]] — compares_to