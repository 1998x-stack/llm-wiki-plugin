---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Extract Method, 提取方法]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Extract Method

## 概述
提取方法是一种[[重构|重构技术]]，将一段代码抽取成一个具有描述性名称的新方法，以提高代码可读性和复用性。

## 关键内容

1. **适用场景**：
   - [[长函数]]需要分解
   - 存在[[重复代码]]
   - 需要为特定概念命名

2. **实施步骤**：
   - 创建一个新方法，名字应描述"做什么"而不是"怎么做"
   - 将目标代码片段复制到新方法中
   - 检查代码片段中使用的局部变量
   - 将局部变量作为参数传入新方法，或在方法内声明
   - 正确处理返回值
   - 用新方法调用替换原始代码片段
   - 进行测试验证

3. **实施效果**：
   - 通过提取方法可以将复杂函数分解为更小、更易理解的部分
   - 提高代码复用性，便于维护
   - 使代码意图更加明确

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Inline Method]] — compares_to