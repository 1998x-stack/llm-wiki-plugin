---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [skills, agent, claude-code, AI工程]
aliases: ["Agent Skills"]
relates_to: []
supersedes: null
---

# Agent Skills

## 概述
为AI代理设计的可重用功能模块，用于扩展代理的能力和行为。

## 关键内容
1. **功能扩展**：[[Agent Skills]]允许为AI代理添加特定领域或任务的功能，使其能够执行更复杂的操作。
2. **实现形式**：在[[Claude Code]]中，[[Skills]]以文件夹形式存在，可包含脚本、资产、数据等，而不仅仅是文本文件。
3. **动态执行**：[[Skills]]可以包含脚本和其他可执行组件，使代理能够在运行时发现、探索和操作这些资源。
4. **灵活[[Configuration|配置]]**：[[Skills]]支持各种[[Configuration|配置]]选项，包括动态钩子注册，可根据不同场景定制行为。

## 来源
- [[Lessons from Building Claude Code_ How We Use Skills]] — 全文

## 相关
- [[Skills]] — relates_to
- [[Claude-Code]] — relates_to
- [[Context-Engineering]] — relates_to