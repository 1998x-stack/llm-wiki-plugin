---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [git, workflow, commands, 工具与框架]
aliases: ["Git Push All", "git push all", "Push All Changes"]
relates_to: []
supersedes: null
---

# Git Push All

## 概述
一次性暂存、提交并推送所有变更到远程[[仓库]]的Git工作流程命令，包含安全检查以防止敏感信息泄露。

## 关键内容

1. ****工作流程概述**：
   - 分析变更（git status, git diff --stat, git log -1）
   - 安全检查（检测secrets、API密钥、大文件等）
   - 用户确认后执行提交和推送

2. ****安全检查机制**：
   - 检测敏感文件：.env*, *.key, *.pem, credentials.json等
   - 检测API密钥：OPENAI_API_KEY, AWS_SECRET_KEY等实际值
   - 防止大文件和构建产物被提交
   - 验证.gitignore[[Configuration|配置]]正确性

3. ****提交规范**：
   - 使用[[Conventional Commits]]格式
   - 支持多种类型：feat, fix, docs, style, refactor, test, chore, perf, build, ci
   - 自动生成摘要和详细变更列表

## 来源
- [[Push All Command]] — 

## 相关
- [[Conventional Commits]] — relates_to
- [[Git Commit]] — relates_to
- [[Pull Request 准备清单]] — relates_to