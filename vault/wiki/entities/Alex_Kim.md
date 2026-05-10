---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [person, researcher, security]
aliases: ["Alex Kim"]
relates_to: []
supersedes: null
---

# Alex Kim

## 概述
Alex Kim 是一位安全研究员，分析了 [[Claude Code]] 的安全机制并指出了其中的绕过方式。

## 关键内容
1. **[[安全分析]]贡献**：
   - 分析了 [[Claude Code]] 的[[客户端证明]]机制
   - 指出三种绕过 anti_distillation 机制的方式，每种约需 1 小时工作量
   - 对[[反蒸馏系统]]的有效性提出质疑

2. **发现的绕过方法**：
   - MITM 代理剥离 `anti_distillation` 字段
   - [[Settings|设置]] `CLAUDE_CODE_ATTRIBUTION_HEADER=false` 禁用 header 注入
   - 在 stock Bun 上运行 JS bundle（Zig 层不存在，placeholder 原样发送）

## 来源
- [[06_security_antidistillation.md]] — Alex Kim 安全分析
- [[Claude Code 源码泄露深度解析（六）：安全机制与反蒸馏——从客户端证明到 Undercover Mode]] — 全文

## 相关
- [[Claude Code]] — analyzes
- [[Anti-Distillation System]] — analyzes