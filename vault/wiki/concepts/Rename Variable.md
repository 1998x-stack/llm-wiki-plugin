---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Rename Variable, 重命名变量]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Rename Variable

## 概述
重命名变量是一种[[重构|重构技术]]，通过提供更具描述性的名称来改善代码的可读性和理解性。

## 关键内容

1. **适用场景**：
   - 变量名不能清楚表达其用途
   - 使用了不清晰的缩写
   - 变量名不符合领域术语

2. **实施步骤**：
   - 如果变量作用域很广，先考虑封装
   - 找到所有对该变量的引用
   - 逐个修改所有引用
   - 进行测试验证

3. **最佳实践**：
   - 使用能体现意图的名称
   - 避免使用缩写
   - 使用领域术语以增强语义
   - 确保命名在上下文中具有一致性

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[变量命名]] — relates_to