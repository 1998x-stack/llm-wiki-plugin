---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, agent-architecture]
aliases: ["Harness Frameworks and Runtimes", "Harness 框架和运行时"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: part_of
    confidence: 0.8
supersedes: null
---

# Harness Frameworks/Runtimes

## 概述
Harness Frameworks/Runtimes 是 AI Agent 架构中的第六层，提供通用执行环境。根据 Harness Is Everything 文章的七层分类框架，这一层位于编码 Agent 之上，具有更高的壁垒和不可替代性。

## 关键内容

1. **层级定位**：
   - 第一层：Human Oversight（人类监督）
   - 第二层：Spec [[Tool System|Tools]]（规格工具）
   - 第三层：Full Lifecycle Platforms（全生命周期平台）
   - 第四层：Task Runners（任务执行器）
   - 第五层：Agent [[Orchestrator Agent|Orchestrator]]s（Agent 编排器）
   - **第六层：Harness Frameworks/Runtimes（Harness 框架和运行时）**
   - 第七层：[[编码 Agent 协议|Coding Agent]]s（编码 Agent）- 商品化层

2. **功能作用**：
   - 提供通用执行环境
   - 比底层的编码 Agent 更难替代
   - 包含系统的架构规范、验证工具和约束机制

3. **竞争优势**：
   - 最底层的 [[编码 Agent 协议|Coding Agent]]（如 [[Claude Code]]、[[Cursor]]、[[Codex CLI|Codex]]）容易被替代
   - 上层的 Harness 框架和运行时构成真正的竞争壁垒
   - 包括如何定义规范、编排任务、进行人类监督等能力

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 知乎文章

## 相关
- [[Harness-Engineering]] — relates_to
- [[Agent-Native-Architecture]] — relates_to
- [[Claude Code]] — relates_to