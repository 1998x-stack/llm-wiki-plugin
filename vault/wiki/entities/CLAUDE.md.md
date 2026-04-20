---
type: entity
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [Claude Code, 工具, 上下文管理, 最佳实践]
aliases:
- CLAUDE.md
- Claude Markdown
- 项目约定文件
relates_to:
  - target: '[[Claude Code]]'
    type: part_of
    confidence: 0.95
  - target: '[[上下文窗口]]'
    type: depends_on
    confidence: 0.9
  - target: '[[上下文经济学]]'
    type: part_of
    confidence: 0.85
  - target: '[[AGENTS.md 项目约定文件]]'
    type: compares_to
    confidence: 0.8
  - target: '[[Agent Skills]]'
    type: compares_to
    confidence: 0.9
supersedes: null
---

# CLAUDE.md

## 概述
CLAUDE.md 是 [[Claude Code]] 每次会话开始时自动读取的特殊项目文件，用于承载项目知识的持久化上下文，包括代码风格、工作流约定和团队规范。

## 关键内容

1. **自动读取机制**：CLAUDE.md 位于项目根目录，[[Claude Code]] 在每次新会话启动时自动读取其内容，无需用户手动指定。这使得它成为跨会话持久化知识的载体。

2. **应该包含的内容**：
   - Claude 无法通过阅读代码猜到的 Bash 命令
   - 区别于语言默认值的代码风格规则（如"使用 ES 模块而非 CommonJS"）
   - 测试指令和首选测试运行器
   - 分支命名、PR 规范等团队约定
   - 完成代码修改后必须执行的步骤（如类型检查）

3. **不应包含的内容**：
   - Claude 通过读代码就能弄明白的信息
   - 标准语言惯例（Claude 已知的）
   - 详细 API 文档（提供链接即可）
   - 频繁变化的信息

4. **长度约束**：CLAUDE.md 过长会导致 Claude 开始忽视其中的内容。对每行应提问："删除这行会导致 Claude 犯错吗？"若不会，则删除该行。这是 [[上下文窗口]] 约束的直接体现。

5. **与 [[AGENTS.md 项目约定文件]] 的比较**：两者都是项目级约定文件，但 CLAUDE.md 专为 Claude Code 设计，而 AGENTS.md 是更通用的 AI Agent 约定格式。

6. **定期精简的必要性**：CLAUDE.md 会随项目演进而膨胀，重要规则被噪声淹没是常见失败模式。需要定期精简，保留高杠杆规则。

## 来源
- [[08_claude_code_best_practices.md]] — Anthropic 官方 Claude Code 最佳实践指南
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/11_agent_skills.md]] — Skills vs CLAUDE.md 对比分析

## 相关
- [[Claude Code]] — part_of（CLAUDE.md 是 Claude Code 的核心功能）
- [[上下文窗口]] — depends_on（长度受上下文窗口约束驱动）
- [[上下文经济学]] — part_of（是持久化上下文策略的核心组件）
- [[AGENTS.md 项目约定文件]] — compares_to（同类但不同生态的约定文件）
