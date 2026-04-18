---
type: concept
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: [技术, 工具, Agent系统]
aliases: [Codex Session Manager, Codex Session]
relates_to:
  - target: "[[Codex CLI]]"
    type: implements
    confidence: 0.95
  - target: "[[Codex TUI]]"
    type: uses
    confidence: 0.8
  - target: "[[Codex沙箱系统]]"
    type: uses
    confidence: 0.75
  - target: "[[JSONL格式]]"
    type: uses
    confidence: 0.9
  - target: "[[LLM-Statelessness]]"
    type: extends
    confidence: 0.85
  - target: "[[会话分支（Branching）]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# Codex会话管理器

[[Codex CLI]] 的上下文持久化层，解决 LLM 天然无状态与工程任务有状态之间的矛盾。通过 Session 持久化、Transcript 存储和 Resume 机制，将 Agent 变成"有记忆的协作者"。

## 核心问题

LLM 每次 API 调用独立，没有内置记忆，[[上下文窗口]]有限。但工程任务可能持续数小时甚至数天，需要中断恢复，多步骤依赖前置结果。Session Manager 在无状态 LLM 之上构建**有状态的任务上下文**。

## Session 数据结构

每个 Session 存储于 `~/.codex/sessions/<session_id>/`：

| 文件 | 内容 |
|------|------|
| `transcript.jsonl` | 完整对话记录（[[JSONL格式|JSONL]] 格式，流式追加） |
| `metadata.json` | Session ID、模型、workspace、sandbox 配置、approval_policy、title、**parent_session_id**（Fork 来源）、**git_commit**（启动时 HEAD） |
| `plan.json` | Agent 任务计划快照 |
| `approvals.log` | 人类审批记录 |

**[[JSONL格式|JSONL]] 格式选择原因**：流式追加、崩溃安全（中断只丢当前行）、可用 `jq` 直接分析。

## Resume 机制

```bash
codex resume          # 交互选择最近会话列表
codex resume --last   # 直接跳最近会话
codex resume <id>     # 指定 Session ID
```

Resume 时不简单地把 transcript 全塞进上下文，而是：
1. 加载环境配置（metadata.json）
2. 读取 transcript，**智能压缩**超出 context window 的早期轮次（保留所有审批记录和关键 tool 结果）
3. 注入 continuation prompt
4. 恢复 approval_policy 和 sandbox_mode 设置

**不变量**：原有 transcript 只读，新对话追加；原有审批在 resume 后依然有效。

## Fork 机制

```bash
codex resume --fork <session_id>
```

从历史节点创建分支，尝试不同解决方案（类比 Git 分支，但在 Agent 对话层面操作）。原 Session 不变，Fork Session 可以走不同路径。

## Memories 系统（跨 Session 长期记忆）

`~/.codex/memories/` — 跨 Session 的长期记忆层（workspace_prefs.md、global_knowledge.md）。在 `workspace-write` sandbox 模式下自动添加到可写路径。Agent 通过工具调用写入，下次启动时自动注入初始上下文。

## exec 模式

```bash
codex exec "生成单元测试"           # 非交互，结果流式输出到 stdout
codex exec --output jsonl "重构"    # JSONL 输出（适合脚本处理）
codex exec --ephemeral "快速问答"   # 不持久化（CI/CD 环境使用）
```

## Session 生命周期

CREATE → ACTIVE → 中断/完成/超时 → Resume → ACTIVE → Fork → 新 ACTIVE

## 减少不确定性的方式

| 不确定性场景 | Session Manager 的应对 |
|------------|----------------------|
| 任务中途崩溃，进度丢失 | [[JSONL格式]] 流式写入，崩溃安全 |
| [[上下文窗口]]超出限制 | 自动压缩，保留关键决策节点 |
| 不同方案需要并行探索 | Fork 机制创建分支 session |
| 重复告知 Agent 项目背景 | Resume 恢复完整上下文 |
| Agent "忘了"上次审批的决定 | approvals.log 持久化，resume 后有效 |
| 不知道 Agent 上次做了什么 | transcript 完整记录，可审计 |

## 工程哲学

> **Transcript 只追加，不修改**——这是系统可信任的基础。任何时刻中断，任何时刻恢复，上下文完整。让 AI Agent 拥有与人类工程师相同的"可中断工作记忆"能力。

## 来源

- [[raw/articles/ai-tools/codex/05_codex_session_manager.md]]
- [[raw/articles/ai-tools/codex/05_codex_session_manager.md]] — Codex CLI 深度解析 Vol.5：Session Manager（详细版）
