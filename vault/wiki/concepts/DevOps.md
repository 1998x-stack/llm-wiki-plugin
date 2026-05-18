---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [devops, ci-cd, automation, culture, AI工程]
aliases: ["DevOps Culture", "Development and Operations", "开发运维"]
relates_to:
  - target: "[[CI/CD 流水线]]"
    type: encompasses
    confidence: 0.8
  - target: "[[Pre-commit Hooks]]"
    type: supported_by
    confidence: 0.8
  - target: "[[GitHub Actions]]"
    type: enabled_by
    confidence: 0.8
  - target: "[[质量保障]]"
    type: requires
    confidence: 0.8
  - target: "[[部署专家]]"
    type: encompasses
    confidence: 0.7
supersedes: null
---

# DevOps

## 概述
DevOps是一种软件工程文化和实践，旨在统一软件开发（Dev）和软件运维（Ops），强调团队协作、自动化和共享责任。

## 关键内容
1. **核心理念**：
   - 打破开发与运维团队之间的壁垒
   - 促进跨职能团队的合作
   - 通过自动化提高效率和可靠性
   - 持续改进和学习的文化

2. **关键实践**：
   - **[[CI_CD流水线|持续集成/持续部署]]（CI/CD）**：自动化构建、测试和部署流程
   - **基础设施即代码（IaC）**：通过代码管理和[[Configuration|配置]]基础设施
   - **监控和日志记录**：实时了解应用性能和用户影响
   - **自动化测试**：确保质量和稳定性

3. **实施工具**：
   - **[[质量保障]]工具**：pre-[[commit]] hooks、自动化测试
   - **CI/CD平台**：[[GitHub Actions]]、Jenkins、GitLab CI等
   - **协作文化**：共享指标、共同目标、开放沟通

## 来源
- [[setup-ci-cd]] — 实现 pre-commit hooks 和 GitHub Actions 质量保障

## 相关
- [[CI/CD 流水线]] — relates_to
- [[Pre-commit Hooks]] — relates_to
- [[GitHub Actions]] — relates_to
- [[质量保障]] — relates_to