---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, loop-mechanism, runtime, AI工程]
aliases: ["TAOR Loop", "Think-Act-Observe-Repeat"]
relates_to: []
supersedes: null
---

# TAOR 循环

## 概述
TAOR 循环是一种 AI Agent 执行模型，包含四个阶段：思考（Think）、行动（Act）、观察（Observe）、重复（Repeat）。

## 关键内容
1. **Think（推理）**：
   - [[Claude_Code|Claude]] 分析当前状态，决定下一步行动
   - 调用 [[Claude_Code|Claude]] API 进行推理

2. **Act（工具调用）**：
   - 调用 Bash / Edit / View / Task 等工具
   - 顺序执行所有工具调用

3. **Observe（观察结果）**：
   - 工具执行结果追加到消息历史
   - 执行 PreToolUse 和 PostToolUse 钩子

4. **Repeat（继续或终止）**：
   - 检查是否还有工具调用，继续循环
   - 纯文本响应时自然终止，返回用户

## 来源
- [[02 · nO 主循环（TAOR Loop）]] — 完整描述

## 相关
- [[nO 主循环]] — 核心执行引擎
- [[Claude Code]] — 所属系统
- [[h2A 实时转向队列]] — 实时转向机制