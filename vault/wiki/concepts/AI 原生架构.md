---
type: concept
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程", "产品设计"]
aliases: ["AI-Native Architecture", "Agent-First Design", "AI 优先架构"]
relates_to:
  - target: "[[TapTap Maker]]"
    type: implements
    confidence: 0.9
  - target: "[[Agent 计算机接口]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# AI 原生架构

## 概述
一种优先为 AI Agent 而非人类用户设计的软件架构理念，主张 GUI 不适合 AI（图形界面是给人用的，AI 更适合直接调接口），产品应面向「Agent + 人」双端设计。

## 关键内容

1. **核心主张**：GUI 不适合 AI，图形界面是给人用的，AI 更适合直接调接口。产品面向「Agent + 人」双端，优先 AI 原生架构。

2. **技能优于知识**：给 AI 灌技能而非灌知识。技能 = 特定领域开发流程的抽象理解，靠组件/API/垂直知识库实现，不堆 Demo。

3. **人机共创模式**：AI 给方案，人做决定。不自动判断可玩性/正确性，只执行创作者指令，保持人在回路中的决策权。

4. **隐藏代码设计**：普通用户编程不如 AI，不用看代码，专注创意层面；代码层由 AI 处理，未来可能开放给高级用户。

5. **竞争意义**：AI 原生架构相比传统工具（如 Unity）无历史包袱，可专为 AI 优化设计；相比通用 AI 编程工具（如 [[Cursor]]）有垂直领域深度和全闭环优势。

## 来源
- [[黎叔的硅星人 Pro 的采访]] — 硅星人 Pro 采访笔记

## 相关
- [[TapTap Maker]] — implements
- [[Agent 计算机接口]] — relates_to
