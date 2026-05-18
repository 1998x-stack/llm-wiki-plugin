---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [payments, token, security, AI工程]
aliases: ["Shared Payment Tokens"]
relates_to: []
supersedes: null
entity_type: project
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# SPT

## 概述
SPT（[[Shared Payment Tokens]]）是[[Stripe]]开发的[[Shared Payment Tokens|共享支付令牌]]，用于在AI Agent购物场景中安全地处理支付凭证。

## 关键内容
1. **安全问题**：SPT解决了AI Agent代为购物时的根本性安全矛盾，避免真实支付凭证暴露给Agent。

2. **约束维度**：SPT可指定多维度限制，包括金额上限、货币限制、时间窗口、商家绑定、单次使用等。

3. **生命周期**：SPT有完整的生命周期管理，通过Webhook事件通知各方使用和失效情况。

## 来源
- [[agentic-commerce-deep-dive.md]] — 详细描述了SPT的各个方面
- [[]] — 
- [[]] — 

## 相关
- [[Stripe]] — develops
- [[Agentic Commerce]] — enables_secure_payments
- [[Agentic Commerce Protocol]] — payment_mechanism