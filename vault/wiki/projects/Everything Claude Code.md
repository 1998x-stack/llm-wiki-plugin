---
type: project
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [claude-code, plugin, ecosystem, ai-tools]
aliases: ["Everything Claude Code", "ECC"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
---

# Everything Claude Code

## 概述
Claude Code 的综合增强插件系统，通过 28 个专用 Agents、119 个 Skills、Hooks 和 Rules 构建完整的 AI 编程辅助生态。

## 关键内容

1. **核心组成**：
   - **28 个 Agents**：专用子代理（规划、审查、安全、调试等）
   - **119 个 Skills**：工作流定义 + 领域知识
   - **Hooks**：生命周期钩子（PreTool/PostTool）
   - **Rules**：硬约束规则

2. **Agents 分类**：
   - 规划与设计类：planner、architect、chief-of-staff
   - 代码审查类：code-reviewer、typescript-reviewer、python-reviewer
   - 安全与审计类：security-reviewer、dependency-auditor
   - 数据库与 API 类：database-reviewer、api-reviewer
   - 调试与优化类：debugger、performance-optimizer
   - 领域专家类：frontend-designer、backend-architect

3. **核心 Skills**：
   - tdd-workflow：TDD 方法论
   - verification-loop：五步验证流程
   - coding-standards：编码规范
   - e2e-testing：Playwright E2E 测试

4. **设计原则**：
   - 职责单一化（Single Responsibility）
   - 工具最小化（Minimal Toolset）
   - 专业知识注入（Domain Expertise Injection）

## 来源
- [[blog-01-overview-architecture]] — ECC 总览架构
- [[blog-02-agents-system]] — Agents 系统
- [[blog-03-skills-system]] — Skills 系统

## 相关
- [[Claude Code]] — extends
- [[Agent Skills]] — implements
- [[GSD]] — compares_to
