---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [git, 版本控制, 提交规范, 工具与框架]
aliases: ["约定式提交", "Conventional Commits specification"]
relates_to:
  - target: "[[Git Commit]]"
    type: extends
    confidence: 0.7
supersedes: null
---

# 约定式提交

## 概述
约定式提交是一种提交消息的规范，提供了一种简单的方式来描述提交所包含的更改类型。

## 关键内容

1. **提交类型**：
   - `feat:` - 新功能
   - `fix:` - 修复 bug
   - `docs:` - 文档变更
   - `refactor:` - [[代码重构]]
   - `test:` - 新增测试
   - `chore:` - 维护任务

2. **用途**：
   - 自动化版本号管理
   - 生成变更日志
   - 便于团队协作和[[代码审查]]
   - 提高提交历史的可读性

3. **结构**：
   约定式提交消息遵循特定格式，通常包括类型、作用域和描述信息，使得机器可以解析并自动化处理提交历史。

## 来源
- [[]] — 

## 相关
- [[Git]] — extends
- [[版本控制系统]] — relates_to
- [[提交规范]] — relates_to