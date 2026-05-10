---
type: concept
status: active
confidence: 0.5
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["ai-design", "data-format", "llm", "context-engineering", "AI工程"]
aliases: [AI-Readable Format, Machine-Readable for AI]
relates_to:
  - AAAK 方言
  - 语义压缩
  - Token 经济学
  - 上下文工程
  - System Prompt 设计
supersedes: null
---

# AI 可读格式

## 概述
AI 可读格式指专为大[[Language-Model|语言模型]] attention 机制设计的数据格式，不遵循人类可读性标准，而是保留语义、删除冗余，利用 LLM 对自然语言缩写的强泛化能力。

## 关键内容
- **核心理念**：为 AI 设计的数据格式，不必遵循为人类设计的可读性标准
- **格式对比**：
  - JSON 的括号、引号是给解析器看的
  - Markdown 的 `**bold**` 是给渲染器看的
  - AI 可读格式的目标受众是大[[Language-Model|语言模型]]的 attention 机制
- **设计原则**：
  1. 保留语义可理解性（AI 天然理解英语语义）
  2. 删除冗余成分（助词、冠词、系动词）
  3. 利用 LLM 对速记、代码注释、学术缩写的强泛化能力
  4. 无需特殊解码器（AI 直接理解压缩后的内容）
- **与人类可读格式的区别**：人类格式追求易读、美观、结构化；AI 格式追求 token 效率、语义密度、attention 友好
- **AI 读的是 token 不是字节**：优化目标是 token 数量而非字节数量，利用 AI 的语义理解能力做无损压缩
- **应用场景**：System Prompt 优化、RAG 上下文装载、长期记忆存储、Agent 间通信协议
- **AAAK 作为范例**：AAAK 是"被激进压缩的英语"，是 AI 可读格式的一个具体实现

## 来源
- [mempalace_03_aaak.md](/raw/articles/ai-tools/mempalace/mempalace_03_aaak.md) — MemPalace 深度解析第三篇：AAAK 方言

## 相关
- [[AAAK 方言]] — implements
- [[语义压缩]] — implements
- [[Token 经济学]] — implements
- [[Context Engineering]] — part_of
- [[上下文窗口]] — depends_on
