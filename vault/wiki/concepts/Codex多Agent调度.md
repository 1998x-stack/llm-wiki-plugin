---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具, Agent系统]
aliases: [Codex Multi-Agent, Codex多智能体, Codex Subagent]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[Codex会话管理器]]"
    type: uses
    confidence: 0.8
  - target: "[[MCP协议层]]"
    type: uses
    confidence: 0.75
  - target: "[[Codex沙箱系统]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# Codex多Agent调度

[[Codex CLI]] 的并行任务执行系统，让 [[Codex CLI|Codex]] 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。主 Agent 将复杂任务分解后，派遣多个子 Agent 并行执行，收集汇总结果。

## 核心价值

单 Agent 面临[[上下文窗口]]有限、顺序执行、单点失败三大局限。Multi-Agent 解决：任务分解（每个 subagent 专注较小上下文）、并行执行、专业分工、隔离失败（subagent 失败不影响主流程）。

## 核心工具集（feature flag: multi_agents）

| 工具 | 功能 |
|------|------|
| `spawn_agent` | 派遣单个 subagent，指定 role/prompt/workspace，返回 agent_id |
| `spawn_agents_on_csv` | 批量派遣（每行 CSV = 一个任务），适合批量同构任务 |
| `send_input(id, msg)` | 向运行中的 subagent 追加指令 |
| `wait_agent(id)` | 阻塞等待 subagent 完成，返回结果摘要 |
| `resume_agent(id)` | 恢复暂停的 subagent |
| `close_agent(id)` | 终止 subagent，释放资源 |
| `list_agents()` | 列出所有 subagent 及其状态 |

## 角色系统（Role Configuration）

Subagent 有专业角色，在 config.toml 中定义：

```toml
[agents.coder]
guidance = "专注实现，不跨模块边界"
display_names = ["Alice", "Bob", "Charlie"]  # 多实例随机昵称

[agents.reviewer]
guidance = "关注安全、性能、API 设计，只提建议不改代码"

[agents.documenter]
guidance = "生成技术文档、README、架构决策记录"
```

## 地址系统

基于路径的可读地址（2026 年引入）：

```
/root                  → 主 Agent
/root/agent_a          → 主 Agent 的 subagent
/root/agent_a/sub_1    → 嵌套 subagent
```

人类可读（vs UUID），便于 TUI 中展示 agent 树结构。

## 并发与资源限制

```toml
[agents]
max_concurrent_agents = 6    # 默认 6，防止资源失控
max_nesting_depth = 1         # 默认 1，subagent 不能再派 subagent
default_worker_timeout = 1800 # 默认 30 分钟超时
```

嵌套深度限制为 1 是刻意的工程决策：防止递归爆炸（token 呈指数增长），保持可调试性。

## 典型场景：spawn_agents_on_csv

批量同构任务（50 个 API endpoint 各写测试、30 个模块迁移框架）：
1. 主 Agent 枚举任务目标 → 生成 CSV → 调用 spawn_agents_on_csv
2. 每个 Worker Agent 独立上下文、独立沙箱
3. 主 Agent wait 所有 worker → 汇总报告

**DevDay 2025 案例**：7 个终端同时跑 7 个 [[Codex CLI|Codex]] 实例，各自开发一款 Phaser.js 游戏，开发者只做审批和方向把控——开发者带宽的杠杆化。

## 工程哲学

> **Multi-Agent 把"人类团队的分工协作"映射到 AI Agent 层面**。好的团队有架构师、工程师、Review 者各司其职。Role 系统让不同 subagent 各自专注，用结构化分工取代"一个 Agent 包揽一切"的脆弱模式。

## 来源

- [[raw/articles/ai-tools/codex/07_codex_multi_agent.md]]
