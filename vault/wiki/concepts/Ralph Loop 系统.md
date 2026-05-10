---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [ai-tools, agent-patterns]
aliases: ["Ralph Loop", "Ralph Loop System", "拉尔夫循环"]
relates_to:
  - target: "[[编码 Agent 协议]]"
    type: implements
  - target: "[[项目约定手册]]"
    type: uses
  - target: "[[PRD 驱动开发]]"
    type: depends_on
supersedes: null
---

# Ralph Loop 系统

## 概述

[[Ralph Loop]] 是一种自主编码代理循环系统，通过外循环不断启动新的 Agent 实例，每个实例从文件状态继承进度，实现一个 User Story 后退出，由外循环检查 PRD 状态决定是否继续下一轮迭代。

## 关键内容

1. **[[Ralph Loop 核心原理|外循环机制]]**：外层脚本（如 `init.sh`）负责检查 `prd.json` 中是否还有未完成的 Story，若有则启动新的 [[Claude Code]] 实例，注入 `CLAUDE.md` 作为固定提示词。
2. **文件驱动的状态管理**：所有进度通过文件系统持久化——`prd.json` 跟踪 Story 完成状态，`progress.txt` 记录每次迭代的交班日记，`AGENTS.md` 积累经验和约定。
3. **[[强制启动序列]]**：每个 Agent 实例启动后必须按顺序执行 7 步：确认工作目录 → 查看 Git 历史 → 读取 progress.txt → 加载 [[项目约定手册|AGENTS.md]] → 查找最高优先级未完成任务 → 启动开发环境 → 冒烟测试。
4. **单 Story 迭代**：每次迭代只实现一个 User Story（最高优先级未完成的），完成后更新状态、[[Git Commit|git commit]]、输出 `<promise>COMPLETE</promise>` 信号。
5. **Bug 处理策略**：尝试 2 次失败后执行 git revert/stash，在 progress.txt 中记录 BLOCKED，将该 Story priority 设为 99（最低），跳到下一个 Story。
6. **[[Context Management|上下文管理]]**：当上下文快满时不强行完成任务，而是 git stash 保存进度、更新 progress.txt、输出 [[完成信号机制（Completion Signal）|COMPLETE 信号]]让外循环重启新实例继续。
7. **支持多种 CLI 工具**：可对接 [[Claude Code]]、Amp 等终端 AI 编码工具，通过 `cat CLAUDE.md | claude --dangerously-skip-permissions` 方式注入提示词。

## 来源

- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — 完整模板
- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — 编码 Agent 协议
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — 项目约定手册

## 相关

- [[编码 Agent 协议]] — implements
- [[项目约定手册]] — uses
- [[PRD 驱动开发]] — depends_on
