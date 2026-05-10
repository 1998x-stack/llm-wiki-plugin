---
type: concept
status: active
confidence: 0.75
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [技术, Agent系统, 人机协同, 安全]
aliases: [Approval Gate, 审批门, 审批界面]
relates_to:
  - target: "[[Codex TUI]]"
    type: implements
    confidence: 0.95
  - target: "[[ExecPolicy]]"
    type: uses
    confidence: 0.9
  - target: "[[Codex CLI]]"
    type: part_of
    confidence: 0.9
supersedes: null
---

# Approval Gate UI

人机协同审批界面模式——在 Agent 执行危险操作前**暂停并展示完整上下文**，让人类在 2 秒内做出批准或拒绝的决策。

## 概述

Approval Gate UI 是 Agent 系统中关键的人机协同节点，将 [[ExecPolicy]] 的策略决策可视化为可操作的界面，展示待执行命令、影响范围（diff 预览）、以及多级审批选项。

## 审批粒度（approval_policy）

| 模式 | 含义 | 适用场景 |
|------|------|---------|
| `untrusted` | 只允许已知安全的只[[Read|读操作]]自动执行 | 新[[仓库]]/高风险环境 |
| `on-request` | Agent 遇到需要时才暂停询问（推荐交互模式）| 日常开发 |
| `never` | 全自动，不暂停（配合外部沙箱使用）| CI/自动化脚本 |
| `granular` | 精细到每类动作独立[[Configuration|配置]] | 高级定制 |

## 界面设计要素

1. **命令意图展示**：不仅显示命令本身，还展示 Agent 为什么要执行这条命令
2. **Diff 预览**：语法高亮的文件修改预览，审批前可见
3. **三态操作**：`[A]llow once`（单次允许）、`[S]ession allow`（会话允许）、`[D]eny`（拒绝并反馈原因）
4. **最小化摩擦**：常见安全操作自动放行，只在关键决策点暂停

## 在 Codex 三道防线中的位置

Approval Gate 是第二道防线，位于 [[ExecPolicy]]（意图过滤）和 OS Sandbox（执行隔离）之间：
1. [[ExecPolicy]] → allow/prompt/forbidden 三态决策
2. **Approval Gate** → prompt 态命令暂停等待人类批准
3. OS Sandbox → 内核级强制执行，LLM 无法绕过

## 来源

- [[raw/articles/ai-tools/codex/02_codex_tui_component.md]] — Codex CLI 深度解析 Vol.2：TUI 交互式终端的设计哲学

## 相关

- [[Codex TUI]] — implements
- [[ExecPolicy]] — uses
- [[Codex CLI]] — part_of
