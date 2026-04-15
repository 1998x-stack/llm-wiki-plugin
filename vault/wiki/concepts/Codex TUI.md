---
type: concept
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [Codex Terminal UI, Codex 交互终端]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.85
  - target: "[[Codex会话管理器]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# Codex TUI

[[Codex CLI]] 的"驾驶舱"——不是简单的 REPL，而是一个**事件驱动状态机**，承担实时审批、diff 预览、会话导航、多 Agent 状态展示等功能。

## 核心问题

普通命令行 chatbot 是线性对话（输入→输出→循环），而 [[Codex CLI|Codex]] TUI 要解决**并发 Agent 行为的可视化与控制**：Agent 后台多步执行 → 某步需要审批 → 同时人类可能在编辑 prompt → 多个 subagent 并行。

## 架构层次

| 层 | 职责 |
|---|---|
| 渲染层 | Ratatui / 原生终端，全屏 alternate screen mode |
| 事件处理层 | 键盘输入、Agent 消息、Tool 结果、审批请求 |
| 状态管理层 | 会话状态、Draft History、审批队列、Agent 树 |
| Wire Protocol 接口 | 与 `codex-rs/core` 通过 protocol crate 通信 |

## 核心交互设计

### Composer（输入框）

- 支持图片拖入（design spec、截图）
- `@` 引用 Skills、MCP 工具、代码片段
- Draft 历史：`Up/Down` 恢复之前草稿（含图片附件）
- `Ctrl+L` 清屏不清上下文（≠ `/clear` 会开新 session）

### 实时 Diff 预览

Agent 提出文件修改时，TUI 渲染语法高亮的 diff。用户可选 `[A]pprove`、`[R]eject`（并告知原因）、`/copy`（复制输出）。

### Approval Gate UI

关键人机协同节点，展示待执行命令并提供三种审批粒度：

| approval_policy | 含义 |
|----------------|------|
| `untrusted` | 只允许已知安全的只读操作自动执行 |
| `on-request` | 需要时才暂停（推荐日常开发） |
| `never` | 全自动，配合外部沙箱使用 |
| `granular` | 精细到每类动作独立配置 |

### 斜杠命令系统

内置"内部 CLI"：`/model`（切换模型）、`/clear`（新会话）、`/review`（独立 Agent 做 Code Review）、`/status`、`/copy`、`/theme`、`/permissions`（只读规划模式）、`/plugins`、`/title`、`/exit`。

## Alternate Screen 模式

TUI 默认使用终端 alternate screen buffer（类似 vim），全屏不污染 shell history，退出后恢复。可通过 `--no-alternate-screen` 或 `tui.alternate_screen = false` 禁用。

## App Server 模式

```bash
codex app-server  # 启动本地 WebSocket 服务器
```

VS Code Extension、桌面 App、Web 前端均可接入同一个 `core`，支持 bearer-token 鉴权连接远程 WebSocket。

## 设计哲学

> **TUI 的本质是"人类监督带宽的最大化"**——Agent 速度远超人类审阅速度，TUI 在关键决策点精确呈现恰好需要的上下文，让人类在 2 秒内做出正确判断。

三原则：最小化审批摩擦（常见安全操作自动放行）、最大化审批信息（危险操作展示完整 diff）、可逆性优先（所有 session 有 transcript，文件改动可 git 回滚）。

## 来源

- `raw/articles/ai-tools/codex/02_codex_tui_component.md`
