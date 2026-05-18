---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, steering, real-time, AI工程]
aliases: ["h2A Real-time Steering Queue", "实时转向队列"]
relates_to: []
supersedes: null
---

# h2A 实时转向队列

## 概述
h2A 实时转向队列是 [[Claude Code]] 中的异步双缓冲队列，允许用户在 Agent 执行中途注入新指令而无需重启会话。

## 关键内容
1. **问题解决**：
   - 传统 Agent 一旦开始执行很难中途纠偏
   - 避免了等待执行完成或完全重启导致的上下文丢失

2. **工作原理**：
   - 用户在 Agent 执行中途输入新指令
   - h2A 异步双缓冲队列非阻塞写入
   - [[游戏主循环模式|主循环]]在每次工具调用完毕后检查队列
   - 发现转向消息后追加到历史，下次推理时生效

3. **应用场景**：
   - 用户发现方向不对时可注入新指令
   - 保持完整上下文的同时调整执行方向
   - 无需重启会话即可改变 Agent 行为

4. **技术特点**：
   - 异步双缓冲队列
   - 非阻塞写入
   - 保留完整上下文

## 来源
- [[02 · nO 主循环（TAOR Loop）]] — 完整描述

## 相关
- [[nO 主循环]] — 应用场景
- [[TAOR 循环]] — 循环模型
- [[Claude Code]] — 所属系统