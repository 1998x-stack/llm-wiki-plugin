---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ci-cd, devops, automation, github]
aliases: ["GitHub Action", "GitHub Workflows", "GitHub 自动化"]
relates_to:
  - target: "[[CI/CD 流水线]]"
    type: implements
    confidence: 0.8
  - target: "[[Pre-commit Hooks]]"
    type: mirrors
    confidence: 0.8
  - target: "[[DevOps]]"
    type: enables
    confidence: 0.8
  - target: "[[持续集成]]"
    type: realizes
    confidence: 0.7
supersedes: null
---

# GitHub Actions

## 概述
[[GitHub]] Actions是[[GitHub]]提供的持续集成和持续部署(CI/CD)[[服务]]，允许在[[GitHub]][[仓库]]中直接创建自定义软件开发生命周期工作流。

## 关键内容
1. **工作原理**：
   - 将工作流[[Configuration|配置]]文件存储在 `.github/workflows/` 目录中
   - 基于事件触发（如push、PR、定时等）
   - 在虚拟环境中执行自动化任务

2. **核心特性**：
   - **事件驱动**：支持多种触发方式（推送、拉取请求、计划任务等）
   - **镜像检查**：在云端复现本地pre-[[commit]] hooks的全部检查
   - **[[矩阵]]测试**：支持多版本、多平台并行测试
   - **构建与验证**：包含完整的构建和测试流程

3. **最佳实践**：
   - 与本地pre-[[commit]] hooks保持一致的检查规则
   - [[Configuration|配置]]多版本/多平台[[矩阵]]以确保兼容性
   - 包含构建验证和[[测试覆盖率|测试覆盖]]
   - 在部署前进行全面的质量检查

## 来源
- [[setup-ci-cd]] — 实现 pre-commit hooks 和 GitHub Actions 质量保障

## 相关
- [[CI/CD 流水线]] — relates_to
- [[Pre-commit Hooks]] — relates_to
- [[DevOps]] — relates_to
- [[持续集成]] — relates_to