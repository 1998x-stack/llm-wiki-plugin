---
type: entity
status: active
confidence: 0.9
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [技术, 工具]
aliases: [Codex, OpenAI Codex CLI]
relates_to:
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.9
  - target: "[[Codex沙箱系统]]"
    type: uses
    confidence: 0.9
  - target: "[[Codex会话管理器]]"
    type: uses
    confidence: 0.85
  - target: "[[MCP协议层]]"
    type: uses
    confidence: 0.85
  - target: "[[Codex多Agent调度]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Codex CLI

OpenAI 以 Rust 重写并开源的**本地编码 Agent**。不是聊天机器人，而是一套把 LLM 决策与 OS 级执行边界融合的系统工程——运行在本地终端，读仓库、改文件、跑命令。

## 一句话定义

**LLM 推理引擎 + OS 级沙箱执行器 + 人机协同审批协议 + MCP 协议总线**

## 整体分层架构

| 层 | 组件 | 职责 |
|---|---|---|
| 用户接入层 | TUI / codex exec / App Server | 用户交互入口 |
| 会话管理层 | Session Store / Transcript / Resume / Subagent Pool | 会话持久化 |
| Agent Core | codex-rs/core | 业务逻辑、Model I/O、Tool Dispatch |
| 策略层 | [[ExecPolicy]] | [[ExecPolicy|策略即代码]]的命令审批引擎 |
| 协议层 | [[MCP协议层]] | 双向 MCP：客户端连工具，服务端暴露自身 |
| 沙箱层 | [[Codex沙箱系统]] | macOS Seatbelt / Linux Landlock+seccomp |

## 核心组件（C1–C9）

| 编号 | 组件 | 主要文件/crate |
|------|------|---------------|
| C1 | TUI | `codex-rs/tui/` |
| C2 | Exec Engine | `core/exec.rs`, `core/spawn.rs` |
| C3 | [[Codex沙箱系统]] | `linux-sandbox/`, macOS seatbelt |
| C4 | [[ExecPolicy]] | `codex-rs/execpolicy/` |
| C5 | [[Codex会话管理器]] | `core/session*.rs` |
| C6 | [[MCP协议层]] | protocol, mcp-server |
| C7 | [[Codex多Agent调度]] | `core/subagent*.rs` |
| C8 | [[Codex配置系统]] | `config.toml` |
| C9 | Model Layer | `core/model*.rs` |

## 关键架构决策

### Rust 重写

原版为 TypeScript，2025 年迁移 Rust 的核心理由：
- **原生沙箱绑定**：Landlock/seccomp 必须在系统调用层做，应用层做不到
- 零依赖静态二进制，消除 Node.js runtime 依赖
- 确定性内存，无 GC 抖动
- 真并发（Tokio async/await）

> 工程智慧：选 Rust 不只是"性能更好"，更是为了**在内核层做安全隔离**。

### Policy-First 设计

先声明策略，再执行——而非"先执行再道歉"：

```
[用户配置] approval_policy + sandbox_mode
         ↓
[ExecPolicy] 每条命令过策略引擎
         ↓
[Sandbox]  OS 内核强制执行
```

策略层（意图）与沙箱层（执行边界）独立但协同，沙箱兜底。

### Wire Protocol 解耦

核心业务逻辑通过 Wire Protocol（`codex-rs/protocol`）与 UI 层解耦：
- TUI、App Server、IDE Extension 共用同一个 `core` crate
- 支持 Python/TypeScript 客户端通过协议接入
- Codex 自身可作为 MCP Server 被其他 Agent 调用

## 三道防线（不确定性 → 确定性）

LLM 输出是随机的，系统执行必须是可控的，用三道防线解决：

1. **[[ExecPolicy]]（意图过滤）** — allow / prompt / forbidden 三态决策
2. **Approval Gate（人机协同）** — 不确定命令暂停等待人类批准
3. **OS Sandbox（执行隔离）** — 内核级强制，LLM 无法绕过

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]]
