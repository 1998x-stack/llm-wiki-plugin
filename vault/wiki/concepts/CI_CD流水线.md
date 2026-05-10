---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ci-cd, devops, automation, 质量保障]
aliases: ["CI/CD Pipeline", "Continuous Integration/Continuous Deployment", "持续集成/持续部署"]
relates_to:
  - target: "[[Pre-commit Hooks]]"
    type: includes
    confidence: 0.8
  - target: "[[GitHub Actions]]"
    type: includes
    confidence: 0.8
  - target: "[[DevOps]]"
    type: part_of
    confidence: 0.8
  - target: "[[质量保障]]"
    type: implements
    confidence: 0.8
  - target: "[[部署专家]]"
    type: uses
    confidence: 0.7
supersedes: null
---

# CI/CD 流水线

## 概述
持续集成/持续部署流水线是软件开发中的自动化流程，用于构建、测试和部署代码变更。

## 关键内容
1. **定义与目的**：
   - CI/CD（持续集成/持续部署）是一种软件工程实践
   - 通过自动化流程确保代码质量、减少人为错误
   - 提高软件交付速度和可靠性

2. **核心组件**：
   - **持续集成（CI）**：开发者频繁地将代码变更合并到中央[[仓库]]
   - **持续部署（CD）**：自动化将代码变更部署到生产环境的过程
   - **质量门禁**：在部署前进行自动化测试和检查

3. **实施要素**：
   - **Pre-[[commit]] hooks**：在代码提交前进行格式化、检查和安全扫描
   - **[[GitHub Actions]]**：在推送/PR时执行与本地pre-[[commit]]相同的检查
   - **多版本/多平台[[矩阵]]测试**：确保代码在不同环境下兼容性
   - **构建和测试验证**：确保功能正确性和代码质量

## 来源
- [[setup-ci-cd]] — 实现 pre-commit hooks 和 GitHub Actions 质量保障

## 相关
- [[Pre-commit Hooks]] — relates_to
- [[GitHub Actions]] — relates_to
- [[DevOps]] — relates_to
- [[质量保障]] — relates_to