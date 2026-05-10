---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [AI工具, 性能优化, 成本控制, 缓存机制, ai-agent, claude-code]
aliases: ["Prompt Cache", "Prompt Cache Optimization", "Cache Break Detection", "Prompt缓存"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[autoCompact]]"
    type: complements
  - target: "[[Token Cost]]"
    type: optimizes
  - target: "[[Anthropic Messages API]]"
    type: uses
  - target: "[[上下文窗口经济学]]"
    type: relates_to
  - target: "[[DANGEROUS_uncachedSystemPromptSection()]]"
    type: implements
  - target: "[[Cache Break 向量]]"
    type: uses
  - target: "[[成本驱动架构]]"
    type: exemplifies
  - target: "[[Context Management]]"
    type: relates_to
supersedes: null
---

# Prompt Cache

## 概述
Prompt Cache是[[Claude Code]]中的[[提示词缓存]]机制，用于优化token使用成本和提高响应速度，通过追踪可能导致缓存失效的因素来维持高命中率。该机制是[[Anthropic]]作为API提供者和消费者的[[成本驱动架构]]理念的重要体现，将Token成本视为AI Agent的"CPU时间"。

## 关键内容
1. **成本驱动设计**：当每个token都需要付费时，Prompt Cache命中率不仅是性能问题，更是账务问题，因此系统高度重视缓存效率。

2. **失效因素追踪**：promptCacheBreakDetection.ts追踪14个可能导致prompt cache失效的因素，包括模式切换、[[Permissions|权限]]状态变化、工具列表动态变化、系统提示词动态段变化等。

3. **风险警告机制**：代码中有一个标记为DANGEROUS_uncachedSystemPromptSection()的函数，警告开发者在系统提示词中添加任何动态内容都会破坏缓存，成本极高。

4. **粘性锁存器机制**：多个"粘性锁存器"（sticky latches）机制确保一旦某种模式被激活，就不会因为中间状态变化而频繁重置cache，从而提高缓存稳定性。

5. **架构设计原则**：为Prompt Cache设计架构，不只是"避免cache break"，而是在架构层面就设计哪些部分是稳定的（可缓存），哪些是动态的（不可缓存）。

6. **成本优化哲学**：Token成本是AI Agent的"CPU时间"——架构设计必须把它作为一等约束，而不是事后优化。这体现了[[Anthropic]]作为API提供者和消费者的双重成本感受对架构决策的直接塑造作用。

## 来源
- [[Claude Code 源码泄露深度解析（二）：核心 Agent 引擎与 40+ 工具系统]] — 全文
- [[Claude Code 源码泄露深度解析（八）：工程总结——从 512,000 行代码中提炼的 AI Agent 设计哲学]] — 43-49行

## 相关
- [[Claude Code]] — part_of
- [[autoCompact]] — complements
- [[Token Cost]] — optimizes
- [[Context Management]] — relates_to