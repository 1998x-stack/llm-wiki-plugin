---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-behavior", "prompt-engineering", "memory-query", "constraint-protocol", "Agent系统"]
aliases: [Know Before Speaking, KBS Protocol]
relates_to:
  - MemPalace
  - 渐进式加载
  - Agent循环
  - 上下文工程
  - 检索增强生成
supersedes: null
---

# Know Before Speaking 协议

## 概述
[[MemPalace]] 在 `mempalace_status` 响应中注入的软约束指令，强制 AI 在回答关于人、项目或历史事件的问题前先查询记忆系统，防止凭训练数据幻觉回答。

## 关键内容
- **协议内容**：`mempalace_status` 工具每次响应注入 "BEFORE RESPONDING about any person, project, or past event: call [[MemPalace|mempalace]]_kg_query or [[MemPalace|mempalace]]_search FIRST"
- **软约束性质**：依赖 LLM 遵循 System Prompt 中的指令，而非硬性代码拦截。实践中大模型对此类强制协议遵从度很高
- **设计目的**：确保[[渐进式加载]]不是"有了就用"的可选功能，而是 Agent 工作流中的强制步骤
- **防止幻觉**：避免 AI 仅凭预训练记忆回答问题，确保回答基于用户真实的对话历史和决策记录
- **与[[渐进式加载]]的关系**：作为[[渐进式加载]]的行为层保障——即使系统提供了四级加载能力，如果 AI 不主动调用查询工具，能力也无法发挥作用
- **工具链**：协议引导 AI 调用 `mempalace_kg_query`（知识图谱查询）或 `mempalace_search`（语义搜索），两者都触发[[渐进式加载]]流程

## 来源
- [mempalace_04_progressive_loading.md](/raw/articles/ai-tools/mempalace/mempalace_04_progressive_loading.md) — MemPalace 深度解析第四篇：4 级渐进式加载系统

## 相关
- [[MemPalace]] — implements
- [[渐进式加载]] — part_of
- [[Agent循环]] — extends
- [[Context Engineering]] — part_of
- [[检索增强生成]] — compares_to
