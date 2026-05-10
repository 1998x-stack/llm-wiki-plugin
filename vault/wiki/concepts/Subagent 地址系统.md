---
type: concept
status: active
confidence: 0.8
created: 2026-04-19
updated: 2026-04-19
last_accessed: 2026-04-19
source_count: 1
tags: [AI, Agent系统, Codex, 架构]
aliases: [Subagent Addressing System, 子智能体地址系统, Agent 路径地址]
relates_to:
  - target: "[[Codex多Agent调度]]"
    type: part_of
    confidence: 0.95
  - target: "[[Codex TUI]]"
    type: uses
    confidence: 0.8
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: implements
    confidence: 0.85
supersedes: null
---

# Subagent 地址系统

## 概述
[[Codex多Agent调度|Codex Multi-Agent]] 系统中基于路径的可读地址方案（2026 年引入），用层级路径替代 UUID 标识 subagent，支持结构化消息传递和 TUI 树形展示。

## 关键内容

1. **路径结构**：地址采用类文件系统的层级路径格式。`/root` 指向主 Agent，`/root/agent_a` 指向主 Agent 派遣的第一个 subagent，`/root/agent_a/sub_1` 指向 agent_a 派遣的嵌套 subagent，`/root/agent_b` 指向第二个 subagent。
2. **人类可读性**：相比 UUID，路径地址直观展示 agent 的层级关系和派遣来源，开发者一眼就能看出哪个 agent 派生了哪个 subagent。
3. **结构化消息传递**：路径天然支持层级路由——消息可以沿路径树精确投递到目标 agent，也可以向子树广播。
4. **TUI 树形展示**：路径地址与 [[Codex TUI]] 的 agent 树结构完美映射，便于在终端界面中可视化整个 agent 团队的层级关系和运行状态。
5. **嵌套深度关联**：地址路径的深度直接受 `max_nesting_depth` [[Configuration|配置]]限制（默认 1），防止路径无限增长导致的路由复杂化。

## 地址示例

```
/root                 → 主 Agent（Orchestrator）
/root/agent_a         → 主 Agent 派遣的第一个 subagent
/root/agent_a/sub_1   → agent_a 派遣的 subagent（嵌套，受深度限制）
/root/agent_b         → 主 Agent 派遣的第二个 subagent
```

## 来源
- [[raw/articles/ai-tools/codex/07_codex_multi_agent.md]] — Codex CLI 深度解析 Vol.7：Multi-Agent 并行编码的调度与协同

## 相关
- [[Codex多Agent调度]] — 地址系统是多 Agent 调度的基础设施 (part_of)
- [[Codex TUI]] — TUI 利用地址系统展示 agent 树结构 (uses)
- [[Orchestrator-Subagent-Pattern]] — 地址系统实现了协调器-子智能体模式的标识机制 (implements)
