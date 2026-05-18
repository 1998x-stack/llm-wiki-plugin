---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [context-engineering, information-architecture, 信息论]
aliases: ["Progressive Disclosure"]
relates_to: []
supersedes: null
---

# Progressive Disclosure

## 概述
一种信息架构策略，通过逐步向用户展示复杂信息来管理认知负荷，首先显示最重要的信息，然后按需提供更多细节。

## 关键内容
1. **[[Context Engineering|上下文工程]]**：在[[Skills]]设计中，整个文件系统被视为[[Context Engineering|上下文工程]]和渐进式披露的一种形式。
2. **文件系统利用**：告诉[[Claude_Code|Claude]][[Skills|技能]]中有哪些文件，它会在适当的时候阅读它们。
3. **信息分层**：最简单的渐进式披露形式是指向其他Markdown文件供[[Claude_Code|Claude]]使用，例如可能将详细的函数签名和使用示例拆分到references/api.md中。
4. **灵活访问**：可以有参考、脚本、示例等文件夹，帮助[[Claude_Code|Claude]]更有效地工作。

## 来源
- [[Lessons from Building Claude Code_ How We Use Skills]] — 全文

## 相关
- [[Context-Engineering]] — relates_to
- [[Skills]] — relates_to
- [[Information-Architecture]] — relates_to