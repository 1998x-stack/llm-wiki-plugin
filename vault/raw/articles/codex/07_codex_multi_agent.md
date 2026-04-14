# Codex CLI 深度解析 Vol.7：Multi-Agent — 并行编码的调度与协同

> **组件定位**：Multi-Agent 系统让 Codex 从"单线程 AI 程序员"变成"AI 开发团队调度中心"。主 Agent 将复杂任务分解后，派遣多个子 Agent 并行执行，收集结果后汇总。

---

## 1. 为什么需要 Multi-Agent？

```
单 Agent 的局限：
  ├── 上下文窗口有限（复杂任务超出 context）
  ├── 顺序执行（无法并行处理独立子任务）
  └── 单点失败（一步失败，整个任务失败）

Multi-Agent 的优势：
  ├── 任务分解（每个 subagent 专注较小的上下文）
  ├── 并行执行（独立子任务同时推进）
  ├── 专业分工（不同 role 的 agent 处理不同类型工作）
  └── 隔离失败（subagent 失败不影响主流程）
```

---

## 2. 架构概览

```
主 Agent（Orchestrator）
    │
    │  spawn_agents_on_csv / spawn_agent
    │
    ├──► Subagent A（角色: coder）
    │      工作目录: /project/module_a
    │      任务: "为 user_service 写测试"
    │
    ├──► Subagent B（角色: coder）
    │      工作目录: /project/module_b
    │      任务: "为 payment_service 写测试"
    │
    └──► Subagent C（角色: reviewer）
           工作目录: /project
           任务: "Review 上面两个 PR 的改动"
    
          wait_agent(A, B)    # 等待 A B 完成
               ↓
          send_input(C, ...)  # 把 A B 的结果发给 C
               ↓
          wait_agent(C)       # 等待 Review 完成
```

---

## 3. 核心 Multi-Agent 工具集

Codex 的 subagent 工具（通过 feature flag `multi_agents` 启用）：

### 3.1 spawn_agent

```
工具名：spawn_agent
功能：派遣单个 subagent
参数：
  - role: 使用 config.toml 中定义的角色名
  - prompt: 任务描述
  - workspace: 工作目录（可与主 agent 不同）
返回：agent_id（用于后续的 send/wait/close）
```

### 3.2 spawn_agents_on_csv

```
工具名：spawn_agents_on_csv
功能：批量派遣 subagent（每行 CSV = 一个任务）
典型用法：
  主 agent 先枚举所有子模块 → 生成 CSV → 批量 spawn
  
示例 CSV：
  module,task
  user_service,写单元测试
  payment_service,写单元测试
  auth_service,写单元测试
```

### 3.3 其他协调工具

```
send_input(agent_id, message)
  → 向运行中的 subagent 发送追加指令

wait_agent(agent_id)
  → 阻塞直到 subagent 完成，返回结果摘要

resume_agent(agent_id)
  → 恢复暂停的 subagent

close_agent(agent_id)
  → 终止 subagent，释放资源

list_agents()
  → 列出当前所有 subagent 及其状态
```

---

## 4. 角色系统（Role Configuration）

Subagent 不是通用的，而是有**专业角色**：

```toml
# config.toml 中定义 agent 角色

[agents.coder]
config_path = "~/.codex/roles/coder.toml"
guidance = """
你是一名专注于实现的工程师。
专注于代码质量、测试覆盖和边界情况。
不要修改架构或跨模块边界。
"""
display_names = ["Alice", "Bob", "Charlie"]   # 多个 subagent 时的随机昵称

[agents.reviewer]
config_path = "~/.codex/roles/reviewer.toml"
guidance = """
你是一名资深代码审查员。
关注安全漏洞、性能问题、API 设计合理性。
不要直接修改代码，只提出建议。
"""

[agents.documenter]
config_path = "~/.codex/roles/documenter.toml"
guidance = "你负责生成技术文档，包括 API 文档、README、架构决策记录。"
```

---

## 5. Subagent 的地址系统

Subagent 使用**基于路径的可读地址**（2026 年引入）：

```
/root                 → 主 Agent
/root/agent_a         → 主 Agent 派遣的第一个 subagent
/root/agent_a/sub_1   → agent_a 派遣的 subagent（嵌套）
/root/agent_b         → 主 Agent 派遣的第二个 subagent
```

**地址路由的优势：**
- 人类可读（vs UUID）
- 支持结构化的层级消息传递
- 便于在 TUI 中展示 agent 树结构

---

## 6. 并发与资源限制

```toml
[agents]
max_concurrent_agents = 6    # 同时运行的 subagent 上限（默认 6）
max_nesting_depth = 1         # 嵌套层数上限（默认 1，即 subagent 不能再派 subagent）
default_worker_timeout = 1800 # 单个 subagent 超时（秒，默认 30 分钟）
```

**为什么限制嵌套深度？**
- 防止递归爆炸：Agent A 派 Agent B 派 Agent C...
- token 消耗呈指数增长
- 调试难度随嵌套深度急剧增加

---

## 7. 实战：7 个并行 Agent 的开发场景

OpenAI DevDay 2025 的真实案例：

```
场景：需要 7 款不同的 Phaser.js 小游戏（用于展示）

实现方式：
  同时开 7 个终端，每个终端运行一个 Codex CLI 实例
  每个实例负责一款游戏的迭代开发
  开发者同时监控 7 个会话，对各自 approve 或 reject

工程价值：
  7 个 Agent 并行工作 ≈ 串行工作时间的 1/7
  开发者从"写代码"变成"审批 + 方向把控"
```

这也是 Codex CLI 的多 session 设计的核心价值：**开发者带宽的杠杆化**。

---

## 8. spawn_agents_on_csv 的工程模式

这个工具特别适合"批量同构任务"：

```
典型场景：
  1. 为 50 个 API endpoint 各写一份测试
  2. 将 30 个 Python 模块迁移到新框架
  3. 为 20 个数据库表生成 CRUD 代码

工作流程：
  主 Agent：
    1. 枚举所有任务目标（读取文件列表/数据库表/API 清单）
    2. 生成 CSV 格式的任务列表
    3. 调用 spawn_agents_on_csv
    4. 等待所有 worker 完成
    5. 汇总结果，生成报告

每个 Worker Agent：
  - 独立上下文，不共享 token
  - 独立沙箱，不共享文件系统（除非显式配置）
  - 超时保护（default_worker_timeout）
```

---

## 9. Multi-Agent 降低不确定性的机制

| 不确定性场景 | Multi-Agent 的应对 |
|------------|------------------|
| 单个 Agent 上下文不够 | 分解任务，每个 subagent 专注小上下文 |
| 任务相互依赖导致顺序问题 | wait_agent 显式依赖同步 |
| 某个子任务 Agent 出错 | 局部失败隔离，不影响其他 subagent |
| Agent 角色不专业，泛化处理 | Role system 注入专业 guidance |
| 资源失控，Token 爆炸 | max_concurrent_agents + timeout 硬限制 |
| 不知道 subagent 在做什么 | 路径地址系统 + TUI agent 树展示 |

---

## 10. 工程哲学摘要

> **Multi-Agent 的本质是把"人类团队的分工协作"映射到 AI Agent 层面。**
>
> 好的团队有架构师、工程师、Review 者各司其职。
> Codex 的 Role 系统让不同 subagent 扮演不同角色，
> 用结构化分工取代"一个 Agent 包揽一切"的脆弱模式。
>
> 最重要的工程决策：**嵌套深度限制为 1**。
> 简单、可预测、易调试，比理论上的无限灵活更重要。

---

*下一篇：Vol.8 — Config System：分层配置的工程设计*
