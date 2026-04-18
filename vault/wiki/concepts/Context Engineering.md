---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["llm", "context-window", "system-design", "gsd", "LLM能力"]
aliases: ["Context Engineering", "上下文工程"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[Context Rot]]"
    type: relates_to
---

# Context Engineering

## 概述
多步骤系统中信息流的全局架构设计方法论，与提示词工程（单次调用措辞优化）本质不同，关注如何为每个[[Subagents-in-Claude-Code|子智能体]]提供干净、充足、精准的上下文。

## 关键内容

1. **与提示词工程的区别**：
   - **提示词工程**：关注单次调用的措辞优化
   - **上下文工程**：关注多步骤系统中信息流的全局架构设计

2. **GSD 的关键实现**：
   > 每个命令只加载它真正需要的文件

3. **计划阶段加载内容**：
   - ✅ PROJECT.md（项目愿景，≤3 页）
   - ✅ REQUIREMENTS.md（版本化需求边界）
   - ✅ CONTEXT.md（当前阶段实现偏好）
   - ✅ RESEARCH.md（本阶段领域研究结论）

4. **执行阶段加载内容**：
   - ✅ [[XML Plan|PLAN.md]]（单个原子任务，XML 格式）
   - ✅ PROJECT.md（最小化项目上下文）

5. **永远不加载的内容**：
   - ✗ 历史对话记录
   - ✗ 其他阶段的代码
   - ✗ 旧的设计讨论
   - ✗ 已完成阶段的研究报告

6. **效果**：
   - 每个[[Subagents-in-Claude-Code|子智能体]]拿到的是干净的全量 200k token
   - 而非被历史垃圾污染的上下文
   - 主会话上下文保持在 30-40%

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程

## 相关
- [[GSD]] — part_of
- [[Context Rot]] — caused
- [[Prompt Engineering]] — compares_to
