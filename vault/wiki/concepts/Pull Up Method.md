---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [重构, 代码优化, AI工程]
aliases: [Pull Up Method, 上拉方法]
relates_to:
  - target: "[[重构目录]]"
    type: part_of
  - target: "[[代码重构]]"
    type: extends
supersedes: null
---

# Pull Up Method

## 概述
上拉方法是一种[[重构|重构技术]]，将多个子类中的相同方法移到父类中，以消除类层次中的重复。

## 关键内容

1. **适用场景**：
   - 多个子类中有相同的方法
   - 方法在多个子类中重复实现
   - 需要去除类层次中的[[重复代码]]

2. **实施步骤**：
   - 检查方法是否完全相同
   - 确认签名一致
   - 在超类中新建方法
   - 从一个子类复制实现
   - 删除一个子类中的方法并测试
   - 删除其他子类中的方法并测试

3. **实施效果**：
   - 去掉类层次中的重复
   - 提高代码的复用性
   - 遵循DRY原则

## 来源
- [[重构目录]] — refactoring-catalog.md
- [[]] —

## 相关
- [[重构目录]] — part_of
- [[代码重构]] — extends
- [[Push Down Method]] — compares_to