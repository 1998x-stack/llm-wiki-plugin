---
type: entity
entity_type: project
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 8
tags: [AI, LLM, Agent, LangChain, 开源, Python]
aliases: [langchain-ai/deepagents, deep agents, deepagents]
relates_to:
  - target: "[[Agent Harness模式]]"
    type: implements
    confidence: 0.95
  - target: "[[DeepAgents中间件体系]]"
    type: implements
    confidence: 0.95
  - target: "[[DeepAgents后端协议]]"
    type: implements
    confidence: 0.95
  - target: "[[DeepAgents评估体系]]"
    type: implements
    confidence: 0.9
  - target: "[[ACP协议]]"
    type: implements
    confidence: 0.85
  - target: "[[LLM-as-Judge]]"
    type: related_to
    confidence: 0.85
supersedes: null
---

# DeepAgents

## 概述

LangChain 官方开源的 **生产级 [[Agent Harness模式|Agent Harness]]**（`langchain-ai/deepagents`），基于 [[LangGraph]] 构建。定位"batteries-included"——不强迫用户从零拼装，通过可组合的[[ROS (Robot Operating System)|中间件]]、后端协议和默认系统提示，快速得到"像 Claude Code 一样能干活"的智能体，再按需裁剪扩展。

## 关键内容

### 仓库结构（Monorepo）

| 子包 | 职责 |
|------|------|
| `libs/deepagents/` | 核心 SDK：`create_deep_agent`、[[ROS (Robot Operating System)|中间件]]、后端协议 |
| `libs/cli/` | 基于 Textual 的终端 TUI，延迟加载重型依赖 |
| `libs/acp/` | [[ACP协议|Agent Client Protocol]] 服务端集成 |
| `libs/evals/` | 评估套件，含 Harbor、Terminal Bench 集成 |
| `libs/repl/` | REPL [[ROS (Robot Operating System)|中间件]]（`langchain-repl`） |
| `libs/partners/` | 合作方沙箱：Daytona、Modal、QuickJS、Runloop |
| `examples/` | 示例项目（各自独立 pyproject.toml） |

各包**独立版本、独立锁文件**，无根级 uv workspace。工具链：uv（包管理）、make（任务聚合）、ruff（lint/format）、ty（类型检查）、pytest（测试）。

### 核心 API

**`create_deep_agent()`**（`libs/deepagents/deepagents/graph.py`）：唯一公共装配入口，声明式配置返回 `CompiledStateGraph`。关键参数：
- `model`：默认 `claude-sonnet-4-6`（需 `ANTHROPIC_API_KEY`）
- `tools`、`middleware`、`backend`、`subagents`、`skills`、`memory`、`interrupt_on`
- `recursion_limit=9999`（避免复杂任务被 LangGraph 截断）
- `BASE_AGENT_PROMPT` 始终附加在系统提示末尾（不可省略的行为基线）

### 默认工具集

`write_todos`、`ls`、`read_file`、`write_file`、`edit_file`、`glob`、`grep`、`execute`（需沙箱 backend）、`task`（子代理分发）。

### 子代理分发

三种子代理规格：同步 `SubAgent`（内联执行）、`CompiledSubAgent`（已编译图）、`AsyncSubAgent`（异步/远程，含 `graph_id`）。默认自动插入 `general-purpose` 子代理，保证 `task` 工具始终可用。

### CLI 特点

- 启动链延迟导入 LangChain/LangGraph（轻量命令如 `-v` 毫秒级）
- SDK 版本精确 pin，与 CI 联动
- Python 版本：`acp` 包用 3.14，其余用 3.12

### 示例项目

`deep_research`（多步检索+反思）、`content-builder-agent`（记忆+skills）、`text-to-sql-agent`、`ralph_mode`（循环自治）、`downloading_agents`（智能体即文件夹）、`async-subagent-server`。

### CI/CD

- GitHub Actions + release-please 自动版本化
- pre-commit：格式化、换行检查，evals 数据目录受保护（字节级一致）
- 提交规范：Conventional Commits（feat/fix/refactor/docs/test/chore）

## 来源
- [[raw/books/deepagents-book-main/01-项目概览与仓库结构.md]]
- [[raw/books/deepagents-book-main/02-核心设计哲学与架构总览.md]]
- [[raw/books/deepagents-book-main/03-入口函数-create_deep_agent.md]]
- [[raw/books/deepagents-book-main/13-模型解析与Provider支持.md]]
- [[raw/books/deepagents-book-main/14-CLI架构与入口.md]]
- [[raw/books/deepagents-book-main/28-CI-CD与发布流程.md]]
- [[raw/books/deepagents-book-main/29-代码规范与质量保障.md]]
- [[raw/books/deepagents-book-main/31-示例项目解析.md]]

## 相关
- [[Agent Harness模式]]
- [[DeepAgents中间件体系]]
- [[DeepAgents后端协议]]
- [[DeepAgents评估体系]]
- [[LLM-as-Judge]]
- [[ACP协议]]
