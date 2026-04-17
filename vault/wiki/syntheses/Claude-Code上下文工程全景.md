---
type: synthesis
title: "Claude Code 上下文工程全景"
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 6
tags: [AI, 方法论, 技术, AI工程]
synthesizes:
  - "[[Context-Engineering]]"
  - "[[分层记忆架构]]"
  - "[[渐进式披露-Progressive-Disclosure]]"
  - "[[LLM-Statelessness]]"
  - "[[Claude-Code-Hook-System]]"
  - "[[Claude-Code]]"
relates_to:
  - target: "[[Context-Engineering]]"
    type: synthesizes
    confidence: 0.95
  - target: "[[分层记忆架构]]"
    type: synthesizes
    confidence: 0.95
  - target: "[[渐进式披露-Progressive-Disclosure]]"
    type: synthesizes
    confidence: 0.9
  - target: "[[Claude-Code-Hook-System]]"
    type: synthesizes
    confidence: 0.9
  - target: "[[LLM-Statelessness]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# Claude Code 上下文工程全景

## 综合洞见

Claude Code 的[[Context-Engineering|上下文工程]]本质是：**在 [[LLM-Statelessness|LLM 无状态性]]约束下，把有限的 token 窗口从"聊天历史容器"重构为"可计算状态机"。** 这需要三件事同时发生：结构化记忆分层（L0–L4）、渐进式检索（三层按需展开）、和生命周期钩子（Hook 系统捕获与压缩）。

## 问题层：LLM 无状态性

LLM 的每次调用都从零状态开始。Claude Code 中这表现为：跨会话失去项目记忆、重复解释架构决策、无法追踪历史 bug 决策。

根本问题：**"说过一次的话"和"已确认的约束"在系统里拥有相同地位**——都在下一次会话后消失。

## 架构层：L0–L4 五层记忆

| 层 | Claude Code 中的内容 | 对应 Hook |
|----|---------------------|----------|
| L0 Cached Prefix | CLAUDE.md、工具 schema | — (静态) |
| L1 Working Memory | 当前任务、约束、打开的文件 | Context Hook 注入 |
| L2 Episodic Memory | 决策+结论+pending items | Summary Hook 压缩 |
| L3 Semantic Memory | 项目知识、架构惯例 | Cleanup Hook 晋升 |
| L4 Raw Archive | 原始 transcript、工具输出 | Save Hook 捕获 |

Hook 采用即发即忘模式（Fire-and-Forget）避免阻塞主进程。

## 检索层：渐进式披露（三层展开）

不一次性灌入所有检索结果，而是：
1. **索引层** — 只注入元数据，让模型先筛选
2. **上下文层** — 注入局部关联（前后事件），提供叙事性
3. **详情层** — 仅对高置信度目标展开完整内容

实测约 10 倍 Token 节省。

## 编排层：Prompt 位置效应

关键信息不能埋在中段（Lost in the Middle 效应）：

```
[L0] CLAUDE.md / schema  ← 最前，吃 prefix cache
[L1] 当前任务
[检索] 最关键证据         ← 靠前
[L2] 历史 checkpoints
[反证] counter-evidence  ← 关键约束靠尾
[用户问题] + [输出要求]
```

对不能丢的约束：允许重复一次 > 埋在中间。

## 预算层：Token 分配（Coding Agent）

| 槽 | 比例 |
|---|---|
| L0 Cached Prefix | 10% |
| L1 Working Memory + Tool Delta | 35% |
| Recent Turns | 15% |
| Retrieved Evidence | 25% |
| L2 Episodic Summaries | 15% |

选片段用 knapsack（按 token budget 最优化），而非 top-k 截断。

## 压缩层：产出可复用状态

触发时机：任务阶段切换 / 关键决策 / 工具超长输出 / 预算逼近阈值。

产出四类对象（而非自由文本摘要）：
- **durable facts** — 项目约定
- **decisions** — 选择+理由
- **open loops** — 未完成事项
- **source anchors** — 行号锚点

⚠️ 禁止压缩数字/合同/代码逻辑。

## 关键结论

> **不要让 Claude Code 会话变成"一次性消耗品"。** 通过 Hook + 分层记忆 + 渐进检索，可以让每次会话的产出（决策、约定、洞见）晋升为下一次会话的 L3 背景知识，实现知识的滚雪球式积累。

## 来源

- [[Context-Engineering]]
- [[分层记忆架构]]
- [[渐进式披露-Progressive-Disclosure]]
- [[Claude-Code-Hook-System]]
- [[LLM-Statelessness]]
- [[Claude-Code]]

## 相关

- [[Claude-Mem]]
- [[DeepAgents评估设计哲学]]
