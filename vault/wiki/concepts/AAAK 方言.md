---
type: concept
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["compression", "summarization", "token-efficiency", "aaak-dialect", "semantic-compression", "AI工程"]
aliases: [AAAK Compression, AAAK Dialect, AAAK 压缩语言]
relates_to:
  - MemPalace 宫殿架构
  - 上下文压缩
  - 轨迹压缩
  - Token 经济学
  - Closet-Drawer 架构
  - 语义压缩
  - 实体缩写
  - AI 可读格式
supersedes: null
---

# AAAK 方言

## 概述
[[MemPalace]] 专为 AI 设计的压缩语言，通过保留语义可理解性的同时激进删除冗余，实现大规模实体场景下 30:1 的 token 压缩比，用于 Closet 层快速导航。

## 关键内容
- **用途**：存放在每个 Room 的 Closet 中，作为该 Room 内容的压缩摘要
- **压缩比**：单条约 4:1，大规模重复实体场景下可达 30:1；但官方承认在短文本、低实体重复场景下可能不省 token 甚至更多
- **导航功能**：AI 先读取 Closet 的 AAAK 摘要（极小 token 消耗），判断 Room 里大致有什么，再决定是否深入 Drawer 取原文
- **[[渐进式加载]]核心**：构成"先地图，再导航，再详情"[[渐进式加载|四级渐进式加载]]系统的第一级
- **零信息损耗**：Drawer 永远存原文保证零信息损耗，AAAK 是"导航地图"而非"存储格式"
- **四大设计原则**：
  1. 去掉所有助词、冠词、系动词（"The user is using" → `usr>use`）
  2. 用符号替代高频短语（`>` 使用/决定，`[reason]` 原因，`@` 上下文，`~` 相关，`+` 以及，`!` 警告，`?` 待确认）
  3. [[实体缩写]]机制：首次建立映射（`alice=A, postgresql=PG`），后续全部使用缩写，一次性开销后持续低代价
  4. 保持 AI 可理解性：本质是"被激进压缩的英语"，LLM 无需特殊解码器即可理解
- **实际示例**：180 tokens 的对话记录压缩至约 30 tokens，保留决策者、决策原因、执行者、截止时间等关键信息
- **注入机制**：每次 AI Agent 启动时，在 System Prompt 里注入 AAAK 字典说明，Agent 几秒内掌握当前会话的缩写体系
- **未来计划**：v3.0.0 中 Closet 摘要尚未全量 AAAK 化，下一版本将实现完整 AAAK Closet

## 来源
- [mempalace_02_palace_architecture.md](/raw/articles/ai-tools/mempalace/mempalace_02_palace_architecture.md) — MemPalace 深度解析第二篇
- [mempalace_03_aaak.md](/raw/articles/ai-tools/mempalace/mempalace_03_aaak.md) — MemPalace 深度解析第三篇：AAAK 方言

## 相关
- [[MemPalace 宫殿架构]] — part_of
- [[上下文压缩]] — compares_to
- [[轨迹压缩]] — compares_to
- [[渐进式加载]] — implements
- [[Token 经济学]] — implements
- [[Closet-Drawer 架构]] — part_of
- [[语义压缩]] — implements
- [[实体缩写]] — uses
- [[AI 可读格式]] — implements
