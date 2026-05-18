---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [LLM, 模型, Anthropic, AI工程]
aliases: [Claude 3 Haiku, Haiku]
relates_to:
  - "[[Anthropic]] — part_of"
  - "[[上下文检索]] — uses"
supersedes: null
---

# Claude 3 Haiku

## 概述
[[Claude_Code|Claude]] 3 Haiku 是 [[Anthropic]] 开发的 [[Claude_Code|Claude]] 3 系列大[[Language-Model|语言模型]]中的轻量级版本，以低成本和快速响应为特点，常用于批量文本处理任务如语境生成。

## 关键内容

1. **定位**：[[Claude_Code|Claude]] 3 系列中速度最快、成本最低的模型，适合大规模批量处理任务。

2. **在[[上下文检索]]中的应用**：[[Anthropic]] 使用 [[Claude_Code|Claude]] 3 Haiku 批量生成文本块的语境前缀，配合 [[Prompt Caching]] 特性，每百万文档 token 成本仅 1.02 美元。

3. **成本效益**：由于语境生成是一次性预处理任务，选择 Haiku 而非 Sonnet/Opus 可显著降低索引构建成本。

## 来源
- [[02_contextual_retrieval.md]] — 语境生成 Prompt 章节

## 相关
- [[Anthropic]] — part_of
- [[上下文检索]] — uses
- [[Prompt Caching]] — uses
