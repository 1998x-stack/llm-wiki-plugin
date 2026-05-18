---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [person, developer, ai-tools, AI工程]
aliases: ["赵凡", "Fried_rice", "@Fried_rice", "Chaofan Shou"]
relates_to: 
  - target: "[[Claude Code]]"
    type: discovered
    confidence: 0.9
  - target: "[[Anthropic]]"
    type: researcher
    confidence: 0.8
supersedes: null
entity_type: person
---

# Chaofan Shou

## 概述
Chaofan Shou（网名 @Fried_rice）是一名开发者实习生，在 2026 年 3 月 31 日发现了 [[Claude-Code|Anthropic Claude Code]] 的源码泄露事件。

## 关键内容

1. **发现者身份**：
   - 2026 年 3 月 31 日凌晨 4 点（UTC），[[Solayer Labs]] 实习生 Chaofan Shou 在 X（原 Twitter）上发布了 [[Claude Code]] 源码泄露的消息
   - 他是首位公开披露此事件的人

2. **技术发现**：
   - 发现了通过 npm registry 里的 `.map` 文件泄露的 [[Claude Code]] 源码
   - 提供了直接下载链接，该链接托管在 [[Anthropic]] 自家的 [[Cloudflare]] R2 存储桶上

3. **影响**：
   - 他的发现引发了整个开发者社区对此次源码泄露事件的关注
   - 直接导致了 [[Claude Code]] v2.1.88 版本源码的公开传播

## 来源
- [[01_overview_architecture]] — 事件始末详细描述

## 相关
- [[Claude Code]] — discovered
- [[Source Map 泄露事件]] — relates_to
- [[Anthropic]] — relates_to