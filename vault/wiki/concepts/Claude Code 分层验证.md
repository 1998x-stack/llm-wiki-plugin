---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 方法论, AI工程]
aliases:
- Claude Code 分层验证
- Claude Code Layered Validation
- Edit 后验证分层
relates_to:
- target: "[[Edit 后验证]]"
  type: extends
  confidence: 0.95
- target: "[[Claude-Code]]"
  type: depends_on
  confidence: 0.9
- target: "[[Claude-Code-Hook-System|Claude Code Hook System]]"
  type: uses
  confidence: 0.85
- target: "[[Guardrails]]"
  type: implements
  confidence: 0.8
supersedes: null
---

# Claude Code 分层验证

## 概述

[[Claude Code]] 分层验证是将 edit 后 validate/linting 逻辑分散到四个层面（tool description、CLAUDE.md、hooks/settings.json、LSP）的架构设计，确保验证既"会被正确调用"又"必定会执行"。

## 关键内容

### 为什么不能只靠单一层面

**只靠 CLAUDE.md 的三个问题：**
1. Claude 可能在复杂任务中"知道但漏做"
2. 做法不一致（有时跑全量、有时跑单文件）
3. 失败时拿不到结构化、自动回灌的反馈

**只靠 tool description 的问题：**
- 决定的是"会不会正确调用"，不是"是不是必定会发生"
- 在 agentic loop 里，Claude 会根据任务自己选择工具
- 可能忘记调用、调错粒度、多文件任务只检查一个文件

### 四层分工架构

#### 第 1 层：Tool Description / Examples — 负责"会用"

**放什么：**
- `run_lint(file_paths, scope)` 的参数语义
- `scope=changed` 和 `scope=workspace` 的区别
- 什么时候先用 LSP，什么时候再用 Bash lint
- 失败输出如何阅读

**特点：** 不是硬约束，而是 [[Anthropic]] 强调的 **usage patterns from examples**。JSON schema 只能表达结构合法性，表达不了"什么时候该用、哪些参数组合有意义、约定的使用惯例"。

#### 第 2 层：CLAUDE.md — 负责"想这么做"

**放什么：**
- 项目验证策略
- 最小检查原则
- 提交前门槛
- 特定目录/语言的额外规则

**示例规则：**
- 修改 Python 文件后优先看 LSP 诊断
- 只跑最小相关测试，不要先跑全量
- formatter 可以自动修，但 typecheck 不通过不能提交
- 前端改动先跑 eslint + targeted test
- migration / schema 变更时要补相应检查

**特点：** CLAUDE.md 是"每个会话都会加载的指令层"，适合放长期稳定的项目规则，让 Claude 有稳定偏好。但它本身不会自动在写文件后触发命令。

#### 第 3 层：Hooks / settings.json — 负责"真的会做"

**放什么：**
- `PostToolUse` on Edit / Write
- 跑 eslint, ruff, mypy, pytest -k ...
- 返回 `additionalContext`
- 必要时 `decision: "block"` 阻断继续推进

**为什么这是主战场：**
- `PostToolUse` 就是为"工具成功执行后立刻跑额外逻辑"设计的
- 可以把 `additionalContext` 或 `decision: "block"` 返回给 Claude
- `PostToolUseFailure` 能在工具失败时提供纠偏信息
- 官方 hook lifecycle 把 PreToolUse / PostToolUse 放在每次 agentic loop 的工具调用里

**这是执行与 enforcement 层。**

#### 第 4 层：LSP — 负责"最快的即时反馈"

**放什么：**
- 每次 edit 后自动出现的 type errors / warnings
- 直接导航到定义、引用、实现

**特点：** 官方 Tools reference 明确写了：LSP 工具提供 code intelligence；**after each file edit, it automatically reports type errors and warnings**。它天然适合作为第一道快速反馈，和 edit 紧耦合，不用额外教 Claude"写完后先去哪里看诊断"。

### 一句话总结

> CLAUDE.md 负责"理念"，tool description 负责"会用"，hooks 负责"执行"，LSP 负责"即时反馈"。edit 后 validate / linting 的主战场应该是 hooks，不该只靠 CLAUDE.md。

### 常见误区

很多人把所有规则都写进 CLAUDE.md，期待 Claude 记住"写完就 lint → lint 失败就修 → 再跑 test → 再检查 changed files"。这在简单项目里可行，但一旦任务变长，就容易退化成"知道规则，但执行不稳定"。

[[Claude Code]] 官方把 hooks 单独做成生命周期自动化机制，本质上就是在告诉你：**重复、机械、必须执行的流程，不要只靠模型记忆，要下沉到生命周期自动化。**

### 落地四步

1. **先写 CLAUDE.md**：定义"先 LSP、后 targeted lint、提交前再 widened checks"的策略
2. **再配 PostToolUse 钩子**：匹配 Edit 或 Write，自动跑最轻量的 lint/check，并把结果回灌给 Claude
3. **自定义 MCP validate 工具**：把"正确用法 + 示例"写进 tool description，而不是只写参数 schema
4. **LSP 作为默认第一道反馈**：不要自己重造"每次 edit 后先跑重型检查"的流程

### 与 SWE-agent 的对比

| 维度 | [[SWE-agent]] | [[Claude Code]] 分层验证 |
|------|-----------|-------------------|
| 验证位置 | 编辑器内部（USE_LINTER + flake8） | 四层分散（LSP + hooks + CLAUDE.md + tool description） |
| 执行机制 | 内置于 edit function | 通过 PostToolUse 钩子自动化 |
| 反馈方式 | 返回错误文本 + 代码片段 | additionalContext + decision:block + LSP 自动诊断 |
| 策略控制 | 硬编码 | CLAUDE.md 定义策略偏好 |

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/12-claude code中，edit后做 validate  linting，需要在tool des.md]] — Claude Code edit 后 validate 分层设计

## 相关

- [[Edit 后验证]] — extends（将 SWE-agent 的 edit 后验证理念扩展到 Claude Code 分层架构）
- [[Claude-Code]] — depends_on（基于 Claude Code 的平台能力）
- [[Claude-Code-Hook-System|Claude Code Hook System]] — uses（利用 PostToolUse 钩子实现自动化执行）
- [[Guardrails]] — implements（分层验证是 Guardrails 理念在 Claude Code 中的具体实现）
