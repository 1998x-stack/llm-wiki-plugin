# Codex CLI 深度解析 Vol.1：架构总览

> **系列前言**  
> Codex CLI 是 OpenAI 以 Rust 重写、开源发布的本地编码 Agent。它不是一个"会写代码的聊天机器人"，而是一套**把 LLM 决策与 OS 级执行边界融合**的系统工程。本系列从 9 个维度逐层拆解其技术内核与工程智慧。

---

## 1. 一句话定义

Codex CLI = **LLM 推理引擎** + **OS 级沙箱执行器** + **人机协同审批协议** + **MCP 协议总线**，运行在你的本地终端，读你的仓库、改你的文件、跑你的命令。

---

## 2. 整体分层架构

```
┌──────────────────────────────────────────────────────────────┐
│                     用户接入层 (Entry Layer)                  │
│   TUI (交互式终端)  │  codex exec (非交互)  │  App Server    │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                     会话管理层 (Session Layer)                 │
│   Session Store   │  Transcript  │  Resume  │  Subagent Pool  │
└──────────────────────────────┬───────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────┐
│                     Agent Core (业务逻辑层)                    │
│   codex-rs/core   ─── Model I/O ─── Tool Dispatch            │
└──────────┬───────────────────┬──────────────┬────────────────┘
           │                   │              │
┌──────────▼──────┐  ┌─────────▼──────┐  ┌───▼───────────────┐
│  ExecPolicy     │  │  MCP 协议层     │  │  Config 系统       │
│  (策略引擎)      │  │  (Client+Server)│  │  (config.toml)    │
└──────────┬──────┘  └────────────────┘  └───────────────────┘
           │
┌──────────▼──────────────────────────────────────────────────┐
│                   沙箱执行层 (Sandbox Layer)                   │
│  macOS Seatbelt  │  Linux Landlock+seccomp  │  Windows       │
│                  exec.rs / spawn.rs                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 核心组件清单

| 编号 | 组件 | 主要文件/crate | 职责摘要 |
|------|------|---------------|---------|
| C1 | **TUI** | `codex-rs/tui/` | 全屏交互终端，diff 预览，实时审批 |
| C2 | **Exec Engine** | `core/exec.rs`, `core/spawn.rs` | 所有工具调用的统一执行入口 |
| C3 | **Sandbox System** | `linux-sandbox/`, macOS seatbelt | OS 级隔离，Landlock/seccomp/Seatbelt |
| C4 | **ExecPolicy** | `codex-rs/execpolicy/` | 策略即代码的命令审批引擎 |
| C5 | **Session Manager** | `core/session*.rs` | 会话持久化、Resume、Transcript |
| C6 | **MCP Layer** | protocol, mcp-server | 双向 MCP：客户端连工具，服务端暴露自身 |
| C7 | **Multi-Agent** | `core/subagent*.rs` | 并行 subagent 调度与路由 |
| C8 | **Config System** | `docs/config.md`, `config.toml` | 分层配置：Global → Team → Project → Profile |
| C9 | **Model Layer** | `core/model*.rs` | 模型抽象、provider 切换、推理级别控制 |

---

## 4. 关键架构决策

### 4.1 Rust 重写：为什么不用 TypeScript？

原版 Codex CLI 用 TypeScript 实现。2025 年 OpenAI 宣布迁移 Rust，理由明确：

| 维度 | TypeScript | Rust |
|------|-----------|------|
| 启动速度 | V8 冷启动开销 | 原生二进制，零依赖 |
| 内存 | GC 抖动 | 确定性内存布局 |
| 安全绑定 | Node native addon 繁琐 | 直接调用 Landlock/seccomp syscall |
| 分发 | Node runtime 依赖 | 单一静态二进制 |
| 并发 | 事件循环单线程 | 真并发 async/await + Tokio |

> **工程智慧**：选择 Rust 不只是"性能更好"，更是为了**原生沙箱绑定** ——  
> 安全隔离必须在系统调用层做，而非应用层做。

### 4.2 Policy-First 设计

Codex 不是"先执行再道歉"，而是**先声明策略，再执行**：

```
[用户配置] approval_policy + sandbox_mode
         ↓
[ExecPolicy] 每条命令过策略引擎
         ↓
[Sandbox]  OS 内核强制执行
```

两层独立但协同：策略层是"意图"，沙箱层是"执行边界"。即使策略层有漏洞，沙箱层兜底。

### 4.3 Wire Protocol 解耦

核心业务逻辑通过 **Wire Protocol**（基于 `codex-rs/protocol`）与 UI 层解耦：

- TUI、App Server、IDE Extension 共用同一个 `core` crate
- 不同语言客户端（Python、TypeScript）可通过协议接入
- Codex 自身也可作为 MCP Server 被其他 Agent 调用

---

## 5. 不确定性 → 确定性的系统设计

Codex CLI 面对的根本问题：**LLM 输出是随机的，但系统执行必须是可控的**。

它用三道防线解决这个矛盾：

```
第一道：ExecPolicy（意图过滤）
   → 命令在执行前先过策略规则集
   → allow / prompt / forbidden 三态决策

第二道：Approval Gate（人机协同）
   → 不确定的命令暂停，等人类批准
   → approval_policy 精细控制暂停粒度

第三道：OS Sandbox（执行隔离）
   → 即使策略放行了，OS 也限制文件系统和网络边界
   → 内核级强制，LLM 无法绕过
```

---

## 6. 组件依赖关系图

```
config.toml ──────────────────────────────────────┐
                                                   ▼
AGENTS.md ──► core (业务逻辑) ──► ExecPolicy ──► Sandbox
                │                      │
                ├──► Session Manager   └──► Approval Gate ──► TUI
                │
                ├──► MCP Client ──► 外部工具服务器
                │
                └──► Subagent Pool ──► 并行 core 实例
```

---

## 7. 小结

Codex CLI 的架构哲学可以用一句话概括：

> **"把 AI 的不确定性关进操作系统的笼子里，用策略而非硬编码来定义笼子的大小。"**

接下来的 8 篇将逐一解剖每个组件的实现细节与工程智慧。

---

*下一篇：Vol.2 — TUI：全屏交互终端的设计哲学*
