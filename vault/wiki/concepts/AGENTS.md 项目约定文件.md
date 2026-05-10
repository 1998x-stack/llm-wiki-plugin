---
type: concept
status: active
confidence: 0.75
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["AI工程", "Agent模式", "项目规范", "Ralph-Loop", "Agent系统"]
aliases: ["AGENTS.md Pattern", "Agent Convention File", "项目约定文件"]
relates_to:
  - target: "[[SKILL.md 格式规范]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Claude Code 记忆系统]]"
    type: extends
    confidence: 0.7
  - target: "[[Agent Harness模式]]"
    type: part_of
    confidence: 0.75
supersedes: null
---

# AGENTS.md 项目约定文件

## 概述
面向 AI Agent 的项目级约定文件，在每次 Agent 会话开始时读取，定义技术栈、运行命令、代码规范、安全规则和已知问题，是 [[Agent Harness模式|Agent Harness]] 模式中的项目上下文载体。

## 关键内容

1. **核心定位**：与 [[SKILL.md 格式规范]]（可复用能力包）和 `CLAUDE.md`（项目记忆）不同，[[项目约定手册|AGENTS.md]] 聚焦于**当前项目的工程约定**——技术栈、文件结构、命名规范、代码风格和禁止操作清单。

2. **标准结构**：
   - **Project Overview**：项目名称、技术栈、开发[[服务]]器地址、创建日期
   - **How to Run**：启动、开发、构建、数据库迁移、测试、验证命令
   - **File Structure**：目录树及用途注释（如 `src/app/` → [[Next.js]] App [[网关与路由器|Router]] 页面）
   - **Naming Conventions**：各类文件的命名规则表（组件 PascalCase、工具函数 camelCase、API 路由 kebab-case 等）
   - **Code Conventions**：代码示例展示正确实践（Server Components 优先、Client Components 按需、Route Handlers 等）
   - **NEVER DO**：不可变规则清单（不删除通过测试、不硬编码密钥、不跳过启动仪式等）
   - **[[Environment Variables]]**：`.env.local` [[Configuration|配置]]模板
   - **Known Issues & [[Gotchas]]**：由 Agent 在运行中动态填充的已知问题
   - **Learnings from Previous Sessions**：跨会话知识积累
   - **Dependency Map**：PRD 依赖关系图

3. **与 [[Agent Harness模式|Agent Harness]] 的关系**：[[项目约定手册|AGENTS.md]] 是 [[Agent Harness模式]] 中项目层约定的载体。Harness 提供通用能力（规划、工具、沙箱），[[项目约定手册|AGENTS.md]] 注入项目特定约束，两者结合使 Agent 既能通用操作又遵守项目规范。

4. **维护机制**：文件由 Agent 自动维护——发现新模式时更新 [[项目约定手册|AGENTS.md]]，Known Issues 和 Learnings 部分在会话过程中动态填充。这体现了"约定即代码"在 AI 开发中的延伸。

5. **NEVER DO 规则示例**：
   - 不删除或修改当前通过的测试
   - 不在未运行验证的情况下[[Settings|设置]] `passes: true`
   - 不提交构建失败的代码
   - 不硬编码密钥或 API 密钥
   - 不跳过 [[CLAUDE.md]] 中的启动仪式

## 来源
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — Ralph Loop 项目约定模板
- [[raw/articles/ai-tools/ralph-loop/initializer-agent.md]] — Initializer Agent 的 AGENTS.md 初始模板规范

## 相关
- [[SKILL.md 格式规范]] — compares_to（可复用技能 vs 项目约定）
- [[Claude Code 记忆系统]] — extends（项目级记忆载体）
- [[Agent Harness模式]] — part_of（Harness 的项目上下文层）
- [[Context Engineering]] — relates_to（上下文工程实践）
- [[Ralph Loop]] — uses（Ralph 会话的启动读取文件）
- [[Initializer Agent]] — created_by（由 Initializer Agent 创建初始种子）
