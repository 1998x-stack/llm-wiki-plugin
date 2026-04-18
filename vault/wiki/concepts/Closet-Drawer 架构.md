---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [ai-memory, architecture, mempalace, progressive-loading]
aliases: [Closet-Drawer Pattern, Closet Drawer Architecture]
relates_to:
  - AAAK 方言
  - MemPalace
  - 渐进式加载
  - 分层记忆系统
  - 冻结快照设计
supersedes: null
---

# Closet-Drawer 架构

## 概述
Closet-Drawer 架构是 [[MemPalace]] 中的两级存储模式：Closet 存放压缩摘要用于快速导航，Drawer 存放原文保证零信息损耗，实现检索效率与完整性的平衡。

## 关键内容
- **两级结构**：
  - **Closet（壁橱）**：存放压缩摘要，用最少的 token 传递最多的导航信息，AI 每次启动时先读 Closet 判断各 Room 里有什么
  - **Drawer（抽屉）**：存放原始内容原文，保证零信息损耗，需要详情时通过 MCP 工具读取
- **工作流程**：
  1. 挖掘阶段（mine）：原始内容切块后，Drawer 存原文，同时生成 AAAK 摘要存入 Closet
  2. 检索阶段（Agent 启动）：读所有 Closet 注入 System Prompt（极小 token）→ AI 理解导航地图 → 需要详情时调用 MCP 工具读 Drawer
- **设计哲学**：AAAK 是"导航地图"而非"存储格式"，导航层追求极致压缩，存储层追求零损耗
- **与[[渐进式加载]]的关系**：Closet-Drawer 是[[渐进式加载]]系统的物理基础，先加载轻量 Closet 判断方向，再[[渐进式披露（Progressive Disclosure）|按需加载]] Drawer 原文
- **与 [[MemPalace 宫殿架构]]的关系**：每个 Room 有一个 Closet 和多个 Drawer，是六层架构中 Drawer 层的内部组织模式

## 来源
- [mempalace_03_aaak.md](/raw/articles/ai-tools/mempalace/mempalace_03_aaak.md) — MemPalace 深度解析第三篇：AAAK 方言

## 相关
- [[AAAK 方言]] — uses
- [[MemPalace]] — part_of
- [[渐进式加载]] — implements
- [[分层记忆系统]] — compares_to
- [[冻结快照设计]] — compares_to
