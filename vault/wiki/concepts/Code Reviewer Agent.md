---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [code-review, agent, quality-assurance, automation]
aliases: ["Code Reviewer", "代码审查专家", "代码审查子代理"]
relates_to:
  - target: "[[代码审查]]"
    type: extends
  - target: "[[安全分析]]"
    type: uses
  - target: "[[性能审查]]"
    type: uses
  - target: "[[代码质量]]"
    type: uses
  - target: "[[SOLID原则]]"
    type: uses
  - target: "[[Skills]]"
    type: implements
supersedes: null
---

# Code Reviewer Agent

## 概述
[[Code-Review-for-Claude-Code|Code Review]]er Agent 是一名资深[[代码审查]]员，专门用于自动化代码质量检查，确保代码符合安全、性能和[[可维护性]]标准。

## 关键内容

1. **审查优先级**：
   - **安全问题**：身份验证、授权、数据泄露风险
   - **性能问题**：[[算法复杂度]]、内存泄漏、低效查询
   - **代码质量**：可读性、命名规范、文档完整性
   - **[[测试覆盖率|测试覆盖]]**：缺失测试、边界情况
   - **设计模式**：SOLID 原则、架构合理性

2. **审查流程**：
   - 自动运行 `git diff` 查看最近变更
   - 重点检查被修改的文件
   - 按优先级顺序进行系统性审查
   - 提供结构化的审查反馈

3. **[[代码审查检查清单|审查清单]]**：
   - 代码清晰易读
   - 函数和变量命名合理
   - 避免[[重复代码]]
   - 正确的[[错误处理]]机制
   - 不暴露密钥或 API key
   - 输入校验已实现
   - [[测试覆盖率|测试覆盖]]充分
   - 考虑性能问题

4. **审查输出格式**：
   - [[代码审查严重性|严重性分级]]（Critical/High/Medium/Low）
   - 问题分类（Security/Performance/Quality/Testing/Design）
   - 具体位置（文件路径和行号）
   - 问题描述及建议修复方案
   - 对系统的影响评估

## 来源
- [[code-reviewer]] — 详细的代码审查代理配置

## 相关
- [[代码审查]] — extends
- [[安全分析]] — uses
- [[性能审查]] — uses
- [[代码质量]] — uses
- [[SOLID原则]] — uses
- [[Skills]] — implements
- [[代码审查问题记录模板]] — relates_to