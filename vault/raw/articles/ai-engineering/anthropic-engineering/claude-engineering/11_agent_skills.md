# Agent 的现实装备：Agent Skills 体系

> **原文**：[Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)  
> **发布日期**：2025 年 10 月 16 日  
> **类别**：Agent Skills · 工具生态 · Claude Code

---

## 摘要

本文介绍了 Claude 的 Agent Skills 体系——一种允许开发者为 Claude Code 定义可复用领域知识和工作流的机制。Skills 以结构化的 SKILL.md 文件形式存在，Claude 会在相关上下文中自动加载或由用户显式调用，是将领域专业知识持久化并传递给 Agent 的重要工程工具。

---

## 一、Skills 的设计动机

### 1.1 知识传递的挑战

Claude Code 每次会话开始时上下文为空。为了让 Agent 了解：
- 项目特有的架构模式
- 团队的编码约定
- 特定领域的最佳实践
- 可复用的工作流程

开发者需要一种**结构化且可复用**的方式来注入这些知识。CLAUDE.md 解决了项目级的持久化问题，但对于领域知识（特别是只在特定情境下相关的知识），将所有内容都放进 CLAUDE.md 会导致过度膨胀。

### 1.2 Skills vs CLAUDE.md

| 特性 | CLAUDE.md | Skills |
|---|---|---|
| 加载时机 | **每次会话开始** | **按需/相关时** |
| 内容范围 | 普遍适用的项目规则 | 特定领域或工作流 |
| 触发方式 | 自动 | 自动（相关时）或显式（/skill-name） |
| 上下文成本 | 每次会话固定消耗 | 仅在使用时消耗 |

---

## 二、Skills 的结构

### 2.1 领域知识 Skill

```markdown
---
name: api-conventions
description: 我们服务的 REST API 设计约定
---
# API 约定
- URL 路径使用 kebab-case
- JSON 属性使用 camelCase
- 列表端点始终包含分页
- URL 路径中版本化 API（/v1/, /v2/）
```

### 2.2 工作流 Skill

```markdown
---
name: fix-issue
description: 修复 GitHub Issue
disable-model-invocation: true
---
分析并修复 GitHub Issue：$ARGUMENTS。

1. 用 `gh issue view` 获取 Issue 详情
2. 理解问题描述
3. 搜索代码库中的相关文件
4. 实现修复所需的更改
5. 编写并运行测试验证修复
6. 确保代码通过 lint 和类型检查
7. 创建描述性提交消息
8. 推送并创建 PR
```

运行 `/fix-issue 1234` 即可调用。

---

## 三、Skills 的工程价值

### 3.1 知识的组件化

Skills 将"如何做某事"的知识从"做什么"中分离出来。一个 Agent 系统可以积累大量专业 Skills，按需组合使用。

### 3.2 可维护性

Skills 可以像代码一样进行版本控制、审查和更新。团队可以共享和协作维护 Skills 库，形成组织级的 AI 能力积累。

### 3.3 上下文效率

通过只在需要时加载 Skills，避免了 CLAUDE.md 过长的问题，保持主上下文的清洁。

---

## 四、Skills 的实际应用场景

| 场景 | Skill 示例 |
|---|---|
| 代码库迁移 | API 约定、命名规则、架构模式 |
| 标准工作流 | fix-issue、code-review、deploy-staging |
| 领域知识 | 法律合规检查、安全扫描、性能优化原则 |
| 团队实践 | PR 格式、文档标准、测试覆盖要求 |

---

*本文分析基于 Anthropic Engineering Blog 原文，写于 2026 年 4 月。*
