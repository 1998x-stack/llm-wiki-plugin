---
type: concept
status: active
confidence: 0.85
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [架构模式, 协议设计, Agent系统]
aliases: [Codex Wire Protocol, Wire Protocol 解耦]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[MCP协议层]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Codex TUI]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Codex Wire Protocol解耦

[[Codex CLI]] 的核心架构决策：通过 **Wire Protocol**（基于 `codex-rs/protocol` crate）将业务逻辑与 UI 层彻底解耦，实现"一个 core，多端接入"。

## 关键内容

1. **核心与 UI 分离**：`codex-rs/core` 包含所有业务逻辑（模型调用、工具分发、会话管理），TUI、App Server、IDE Extension 均作为独立前端通过 Wire Protocol 接入同一个 core crate。

2. **多语言客户端支持**：协议层抽象了通信细节，[[Python]]、[[TypeScript]] 等语言编写的客户端均可接入，无需重写核心逻辑。

3. **双向角色**：[[Codex CLI|Codex]] 既可通过 MCP Client 连接外部工具[[服务]]器，也可作为 [[MCP Prompts|MCP Server]] 暴露自身能力被其他 Agent 调用——形成 Agent 间的可组合性。

4. **组件依赖关系**：
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

## 工程价值

- **单一事实源**：所有 UI 端共享同一 core，行为一致性得到保证
- **可扩展性**：新增 UI 端只需实现协议适配层，无需触碰业务逻辑
- **[[Agent可组合性|Agent 可组合性]]**：[[Codex CLI|Codex]] 作为 [[MCP Prompts|MCP Server]] 可被其他 Agent（如 [[Claude Code]]）调用，形成工具链

## 来源

- [[raw/articles/ai-tools/codex/01_codex_architecture_overview.md]] — 第 4.3 节 Wire Protocol 解耦 + 第 6 节组件依赖关系图

## 相关

- [[Codex CLI]] — 采用 Wire Protocol 解耦架构的编码 Agent
- [[MCP协议层]] — 与 Wire Protocol 协同的双向协议层
- [[Codex TUI]] — 通过 Wire Protocol 接入 core 的终端 UI
