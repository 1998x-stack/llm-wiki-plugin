---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [software-engineering, ai-engineering, knowledge-management]
aliases: ["Repository as System of Record", "仓库即记录系统", "Repo as System of Record"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: part_of
    confidence: 0.9
  - target: "[[CLAUDE.md文档]]"
    type: implements
    confidence: 0.8
  - target: "[[Knowledge-Base]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Version-Control]]"
    type: depends_on
    confidence: 0.8
  - target: "[[Harness分层架构]]"
    type: implements
    confidence: 0.7
supersedes: null
---

# Repo as System of Record

## 概述
Repo as System of Record 是一种软件工程实践，指将任务定义、架构约束、质量标准等信息全部写在代码[[仓库]]中，而不是依赖口头约定或即时消息传递，使 AI 代理能够读取[[仓库]]获取所需的所有信息。

## 关键内容

1. **核心理念**：
   - [[仓库]]作为唯一的真实来源（Source of Truth）
   - 将所有项目规则、约束和规范编码到[[仓库]]中
   - 让 AI 代理能够自主获取必要的上下文信息

2. **实施方式**：
   - 任务定义写入[[仓库]]
   - 架构约束写入[[仓库]]
   - 质量标准写入[[仓库]]
   - 不依赖 [[Slack]] 消息或口头约定
   - 通过文档文件（如[[CLAUDE.md]]）定义项目规范

3. **优势**：
   - 确保 AI 代理能够访问最新的规范
   - 避免因沟通不畅导致的错误
   - 支持自动化验证和约束执行
   - 提高团队协作的一致性和透明度
   - 在[[Harness分层架构]]中实现规范的系统化管理

4. **在[[Harness-Engineering|Harness Engineering]]中的应用**：
   - 作为Harness框架的重要组成部分
   - 支持Agent对项目环境的全面理解
   - 实现规范的自动化执行和验证

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 知乎文章
- [[Harness Engineering: Leveraging Codex in an Agent-First World]] — OpenAI官方文章

## 相关
- [[Harness-Engineering]] — relates_to
- [[CLAUDE.md文档]] — relates_to
- [[Knowledge-Base]] — relates_to
- [[Version-Control]] — relates_to
- [[Harness分层架构]] — relates_to
- [[Software-Engineering-Best-Practices]] — relates_to