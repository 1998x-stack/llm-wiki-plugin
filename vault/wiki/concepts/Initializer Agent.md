---
type: concept
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["ai-tools", "ralph-loop", "agent-pattern", "bootstrap", "Agent系统"]
aliases: ["Initializer Agent", "初始化 Agent", "Project Initializer", "项目初始化代理"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: part_of
  - target: "[[Agent Harness模式]]"
    type: implements
  - target: "[[AGENTS.md 项目约定文件]]"
    type: creates
  - target: "[[PRD 驱动开发]]"
    type: enables
supersedes: null
---

# Initializer Agent

## 概述
Initializer Agent 是 [[Ralph Loop]] 系统中仅运行一次的项目初始化代理，负责在首个 context window 内建立完整的[[游戏脚手架模式|项目脚手架]]（init.sh、prd.json、progress.txt、AGENTS.md 和初始 git commit），不实现任何业务功能。

## 关键内容

1. **职责边界**：Initializer Agent 的唯一职责是"设置，不开发"。它创建五样产物——`init.sh` 环境启动脚本、`prd.json` 任务清单（50-200 个 User Story）、`progress.txt` 交班日记模板、`AGENTS.md` 项目约定手册、以及初始 git commit。严禁写业务代码、运行应用或安装不必要的依赖。

2. **init.sh 设计规范**：幂等性（多次运行结果相同）、安装依赖、启动开发服务器、健康检查等待就绪、成功打印 "=== READY ==="、失败 exit 1。支持多技术栈模板（Node.js/[[Next.js]]、Python/FastAPI），每种都包含依赖安装、环境变量检查、数据库初始化、进程管理和健康检查循环。

3. **prd.json 生成规范**：每个 User Story 包含 `id`（category-NNN 格式）、`category`、`title`、`description`（"用户可以..."格式）、`acceptanceCriteria`、`passes`（初始 false）、`priority`（1=最高）、`estimatedMinutes`、`dependencies`。前端 Story 的 acceptanceCriteria 必须包含 "Verify in browser using dev-browser skill"。

4. **AGENTS.md 初始模板**：包含 Project Overview、Running Commands、File Structure、Naming Conventions、NEVER DO 规则清单、Known Gotchas（运行时填充）、Learnings from Previous Sessions（运行时维护）。这是 [[AGENTS.md 项目约定文件]] 的初始种子。

5. **progress.txt 初始模板**：记录 Session 日志格式——角色、行动、详情、完成特性数、下一轮建议。Initializer Agent 写入第一条 Session 记录并标注 "Next session should" 指向最高优先级 Story。

6. **完成后验证**：运行 `bash init.sh` 确认 READY、用 Python 验证 prd.json Story 数量、`git log --oneline -1` 确认 commit 存在。输出标准化完成信息：Stories 数量、init.sh 测试结果、git commit 状态。

7. **与 [[Agent Harness模式]] 的关系**：Initializer Agent 是 Harness 模式的"准备阶段"——在 Coding Agent 开始工作前，确保环境、任务清单、约定文件全部就位。它体现了 Harness 设计中"环境先于执行"的原则。

## 来源
- [[raw/articles/ai-tools/ralph-loop/initializer-agent.md]] — Initializer Agent 完整提示词、init.sh 模板（Node.js/Python）、AGENTS.md 模板、progress.txt 模板

## 相关
- [[Ralph Loop]] — part_of（Ralph 系统的初始化阶段）
- [[Agent Harness模式]] — implements（Harness 的准备阶段模式）
- [[AGENTS.md 项目约定文件]] — creates（生成初始约定文件种子）
- [[PRD 驱动开发]] — enables（生成 prd.json 任务清单驱动后续开发）
- [[Session 交接机制]] — relates_to（创建 progress.txt 交班日记模板）
