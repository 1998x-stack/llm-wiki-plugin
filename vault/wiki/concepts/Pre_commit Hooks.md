---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ci-cd, devops, automation, 代码质量, AI工程]
aliases: ["Pre-commit Hook", "预提交钩子", "Git Hooks"]
relates_to:
  - target: "[[CI/CD 流水线]]"
    type: part_of
    confidence: 0.8
  - target: "[[GitHub Actions]]"
    type: mirrors
    confidence: 0.8
  - target: "[[DevOps]]"
    type: supports
    confidence: 0.8
  - target: "[[代码质量]]"
    type: ensures
    confidence: 0.8
supersedes: null
---

# Pre-commit Hooks

## 概述
Pre-[[commit]] hooks是在代码提交到版本控制系统之前自动运行的脚本，用于执行格式化、代码检查、安全扫描等质量保证任务。

## 关键内容
1. **作用机制**：
   - 在开发者执行 `git commit` 命令时触发
   - 验证即将提交的代码是否符合项目规范
   - 如检查失败则阻止提交，直到问题修复

2. **常见工具**：
   - **格式化工具**：[[Prettier]]、Black、gofmt、rustfmt 等
   - **代码检查工具**：[[ESLint]]、Ruff、golangci-lint、Clippy 等
   - **安全扫描工具**：Bandit、gosec、cargo-audit、npm audit 等
   - **类型检查工具**：[[TypeScript]]、mypy、flow 等

3. **实施策略**：
   - 根据项目语言选择匹配的工具集
   - [[Configuration|配置]]与CI/CD流水线一致的检查规则
   - 确保本地检查与远程检查行为相同

## 来源
- [[setup-ci-cd]] — 实现 pre-commit hooks 和 GitHub Actions 质量保障

## 相关
- [[CI/CD 流水线]] — relates_to
- [[GitHub Actions]] — relates_to
- [[代码质量]] — relates_to
- [[DevOps]] — relates_to