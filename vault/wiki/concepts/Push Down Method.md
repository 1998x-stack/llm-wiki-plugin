---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Push Down Method, 下推方法]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Push Down Method

## 概述
下推方法是一种[[重构|重构技术]]，将仅适用于部分子类的行为移到相应的子类中。

## 关键内容

1. **适用场景**：
   - 某个行为只适用于部分子类
   - 父类包含了不适用于所有子类的方法
   - 需要将方法放到真正使用它的地方

2. **实施步骤**：
   - 把方法复制到需要它的子类
   - 从超类删除方法
   - 进行测试
   - 删除不需要该方法的子类副本
   - 进行测试

3. **实施效果**：
   - 把方法放到真正使用它的地方
   - 避免父类包含不通用的方法
   - 提高类层次的合理性

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Pull Up Method]] — compares_to