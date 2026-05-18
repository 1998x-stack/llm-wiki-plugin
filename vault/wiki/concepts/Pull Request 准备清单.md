---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [git, pull-request, conventional-commits, code-review, AI工程]
aliases: ["Pull Request Preparation Checklist", "PR Preparation", "PR Checklist"]
relates_to: []
supersedes: null
---

# Pull Request 准备清单

## 概述
一份用于清理代码、暂存变更并准备 Pull Request 的详细操作清单，确保提交符合规范并经过充分测试。

## 关键内容

1. **代码格式化与测试**：
   - 运行 prettier 格式化工具确保代码风格统一
   - 执行 npm test 运行所有测试，确保功能正常

2. **变更审查与暂存**：
   - 通过 `git diff HEAD` 查看当前工作区与 HEAD 的差异
   - 使用 `git add .` 暂存所有相关变更

3. **提交信息规范**：
   - 遵循 [[Conventional Commits]] 规范创建提交信息
   - 使用 `fix:` 表示 bug 修复，`feat:` 表示新功能，`docs:` 表示文档更新等

4. **PR 内容结构**：
   - 包含变更内容、变更原因、测试情况和可能影响的详细说明

## 来源
- [[PR Preparation Guide]] — 详细操作指南

## 相关
- [[Conventional Commits]] — extends
- [[Git Commit]] — relates_to
- [[commit]] — relates_to