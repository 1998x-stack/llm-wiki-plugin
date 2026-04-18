---
type: project
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 8
tags: ["ai-tools", "autonomous-coding", "agent-loop", "Agent系统"]
aliases: ["Ralph Loop", "Ralph Coding Agent", "Ralph 循环"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Agent Harness模式]]"
    type: implements
  - target: "[[PRD 驱动开发]]"
    type: implements
  - target: "[[Agent 迭代循环]]"
    type: implements
  - target: "[[Session 交接机制]]"
    type: implements
  - target: "[[Context Engineering]]"
    type: depends_on
  - target: "[[AGENTS.md 项目约定文件]]"
    type: uses
  - target: "[[Initializer Agent]]"
    type: uses
  - target: "[[愚钝区（The Dumb Zone）]]"
    type: relates_to
  - target: "[[固定提示栈（Fixed Prompt Stack）]]"
    type: uses
  - target: "[[完成信号机制（Completion Signal）]]"
    type: uses
  - target: "[[双重验证（Dual Verification）]]"
    type: uses
  - target: "[[子 Agent 模式（Sub-Agent Pattern）]]"
    type: uses
  - target: "[[上下文策略]]"
    type: implements
  - target: "[[上下文预算管理]]"
    type: implements
  - target: "[[Clean State Protocol]]"
    type: implements
  - target: "[[E2E 验证模式]]"
    type: implements
  - target: "[[Geoffrey Huntley]]"
    type: depends_on
  - target: "[[工作台 vs 长期记忆]]"
    type: implements
  - target: "[[PRD 生成提示词]]"
    type: uses
  - target: "[[User Story 粒度原则]]"
    type: implements
  - target: "[[prd.json 格式规范]]"
    type: uses
supersedes: null
---

# Ralph Loop

## 概述
Ralph Loop 是一种自主编码代理系统，通过 CLAUDE.md 提示词模板驱动 [[Claude Code]] 实例按迭代循环逐个实现 PRD 中的 User Story，利用 prd.json、progress.txt 和 AGENTS.md 三个核心文件实现跨会话进度继承与知识积累。

## 关键内容

1. **起源与核心哲学**：Ralph Loop 基于 [[Geoffrey Huntley]] 的 Ralph Wiggum 技术，核心哲学是 **"The technique is deterministically bad in an undeterministic world."** ——不试图让单个 Agent 记住一切，而是把状态全部写进文件，让每一个新鲜的 Agent 从文件中快速定位，继续上一个 Agent 中断的工作。这一理念具体化为 [[工作台 vs 长期记忆]] 心智模型：[[上下文窗口]]是用完就扔的工作台，文件系统是永久存储的长期记忆。

2. **触发短语**：系统可通过以下短语激活——"run ralph"、"ralph loop"、"autonomous coding loop"、"set up ralph for"、"run until complete"、"AFK agent"、"continuous agent"、"让 AI 自动跑"。

3. **核心架构**：每次迭代启动一个全新的 [[Claude Code]] 实例，通过 `cat CLAUDE.md | claude --dangerously-skip-permissions` 注入完整提示词模板。Agent 从文件系统中读取进度状态，继续未完成任务，而非依赖上下文记忆。

2. **强制启动序列**：每个 Agent 实例启动时必须按顺序执行 7 步确认仪式——确认工作目录、查看 Git 历史、读取 progress.txt（交班日记）、读取 AGENTS.md（经验手册）、解析 prd.json 查找最高优先级未完成任务、启动开发环境、执行 Smoke Test 验证代码可运行。

3. **单次迭代约束**：每次迭代只实现 ONE 个 User Story，禁止跨 Story 并行。前端变更必须通过 [[Puppeteer MCP]] [[浏览器自动化验证]]（截图、填表、点击、验证 DOM），验证通过后方可设置 `passes: true`。

4. **进度追踪三文件**：
   - **prd.json**：产品需求文档，包含 User Story 列表、优先级、依赖关系、`passes` 状态
   - **progress.txt**：交班日记，记录每轮 Session 的完成状态、变更点、阻塞信息
   - **AGENTS.md**：项目约定手册，由 Agent 维护，积累 Learnings、Gotchas、依赖映射

5. **Bug 处理策略**：尝试 2 次失败后执行回退流程——`git stash` 或 `git revert HEAD`，在 progress.txt 中标记 BLOCKED，在 AGENTS.md 中记录坑点，将该 Story priority 改为 99 并移动到下一个 Story。

6. **[[Context Management|上下文管理]]**：当上下文快满时不强行完成任务，而是 `git stash` 保存未完成工作，在 progress.txt 中标注 Early exit，提交干净状态后输出 `<promise>COMPLETE</promise>`，由外循环决定是否继续迭代。

7. **[[完成信号机制（Completion Signal）|完成信号]]**：无论是否还有未完成的 Story，每次迭代结束必须输出 `<promise>COMPLETE</promise>`，Ralph 外循环检查 prd.json 决定是否启动下一个 Agent 实例。

## 来源
- [[raw/articles/ai-tools/ralph-loop/SKILL.md]] — Ralph Loop Skill 完整定义（核心哲学、五组件、快速启动流程、关键约束、文件结构）
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Ralph Coding Agent 固定提示词模板
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — 项目约定模板（文件结构、命名规范、代码约定、NEVER DO 规则）
- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — Coding Agent 完整协议（启动序列、铁规则、实现流程、Bug 处理、progress.txt 格式、特殊情况处理）
- [[raw/articles/ai-tools/ralph-loop/initializer-agent.md]] — Initializer Agent 完整提示词、init.sh 模板、AGENTS.md 模板、progress.txt 模板
- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — Ralph Loop 核心原理深度解析（上下文内存模型、愚钝区、完成信号、状态持久化、固定提示栈、子 Agent 模式）
- [[raw/articles/ai-tools/ralph-loop/context-strategies.md]] — Context Strategies 完整文档（六大策略、模型对比、预算估算）
- [[raw/articles/ai-tools/ralph-loop/testing-patterns.md]] — Testing Patterns 完整文档（四种验证模式、失败处理树、命令速查表）
- [[raw/articles/ai-tools/ralph-loop/prd-generator-prompt.md]] — PRD 生成提示词模板（Ralph Loop 前置技能、Story 粒度原则、验证脚本、专项场景模板）

## 相关
- [[Claude Code]] — uses（底层编码代理）
- [[Agent Harness模式]] — implements（自主编码 Harness 的具体实现）
- [[PRD 驱动开发]] — implements（以 prd.json 为进度驱动核心）
- [[Agent 迭代循环]] — implements（单次迭代一个 Story 的循环模式）
- [[Session 交接机制]] — implements（三文件跨会话状态传递）
- [[Puppeteer MCP]] — uses（前端 E2E 验证工具）
- [[Context Engineering]] — depends_on（上下文窗口管理与交接）
- [[E2E 验证模式]] — implements（外部运行时验证方法论）
- [[PRD 生成提示词]] — uses（Ralph Loop 启动前必须通过 PRD 生成提示词生成 prd.json）
- [[User Story 粒度原则]] — implements（每个 Story 必须足够小，能在单个上下文窗口内完成）
- [[prd.json 格式规范]] — uses（prd.json 是 Ralph Loop 的权威任务源）
- [[Geoffrey Huntley]] — depends_on（Ralph Wiggum 技术原创者）
- [[工作台 vs 长期记忆]] — implements（核心架构心智模型）
