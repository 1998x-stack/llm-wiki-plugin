---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [git, 版本控制, 提交, 工具与框架]
aliases: ["Git 提交", "git commit"]
relates_to:
  - target: "[[Git]]"
    type: part_of
    confidence: 0.8
  - target: "[[Conventional Commits]]"
    type: uses
    confidence: 0.7
supersedes: null
---

# Git Commit

## 概述
Git Commit 是 Git 版本控制系统中的基本操作，用于将暂存区的更改保存到本地[[仓库]]中。

## 关键内容

1. **基本功能**：
   - 将暂存区的更改记录到[[仓库]]历史中
   - 创建一个唯一的提交标识符（[[commit]] hash）
   - 记录提交者信息和时间戳
   - 保存提交消息描述变更内容

2. **工作流程**：
   - 使用 `git add` 将更改添加到暂存区
   - 使用 `git commit` 保存更改到[[仓库]]
   - 可以使用 `git commit -m` 直接指定提交消息

3. **最佳实践**：
   - 编写清晰、有意义的提交消息
   - 遵循[[Conventional Commits|约定式提交]]规范（[[Conventional Commits]]）
   - 保持提交粒度合理，一次提交完成一个逻辑单元的更改

## 来源
- [[]] — 

## 相关
- [[Git]] — part_of
- [[Conventional Commits]] — uses
- [[版本控制系统]] — part_of