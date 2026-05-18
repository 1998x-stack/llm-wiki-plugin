---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, execution-engine, runtime, AI工程]
aliases: ["nO Master Loop", "主循环"]
relates_to: []
supersedes: null
---

# nO 主循环

## 概述
nO [[游戏主循环模式|主循环]]是 [[Claude Code]] 的核心执行引擎，设计原则是 Runtime 是"哑循环"，所有智能在模型里。

## 关键内容
1. **设计原则**：
   - Runtime 是哑循环，智能在模型里
   - 从"代码控制模型"到"模型控制循环"的根本[[规范化理论|范式]]转变

2. **消息历史管理**：
   - 单一扁平消息历史（非树状/多线程）
   - 包含用户输入、工具调用、工具结果等

3. **循环机制**：
   - Think 阶段：调用 [[Claude_Code|Claude]] API 推理
   - Act 阶段：执行工具调用
   - Observe 阶段：处理工具结果
   - Repeat 阶段：继续或终止循环

4. **[[终止机制]]**：
   - 自然终止条件：无工具调用时返回纯文本响应
   - 不使用固定迭代上限，避免过早终止

## 来源
- [[02 · nO 主循环（TAOR Loop）]] — 完整描述

## 相关
- [[TAOR 循环]] — 循环模型基础
- [[Claude Code]] — 所属系统
- [[h2A 实时转向队列]] — 实时转向机制