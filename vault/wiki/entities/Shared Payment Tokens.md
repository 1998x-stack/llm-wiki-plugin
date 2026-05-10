---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-commerce, payment, stripe]
aliases: ["SPT", "Shared Payment Tokens", "共享支付令牌"]
relates_to:
  - target: "[[Stripe]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Agentic Commerce Protocol]]"
    type: integrated_with
    confidence: 0.9
  - target: "[[Machine Payments Protocol]]"
    type: complementary
    confidence: 0.8
supersedes: null
---

# Shared Payment Tokens

## 概述
Shared Payment Tokens (SPT) 是 [[Stripe]] 开发的安全支付令牌系统，允许 AI Agent 代表买家进行购物而不暴露真实的支付凭证。

## 关键内容

1. **安全机制**：
   - 解决了 AI Agent 代购场景中的安全矛盾
   - 买家创建 SPT 后，AI Agent 只持有受限令牌，不接触真实支付信息
   - 商家只收到受限令牌，不会获得完整卡号信息

2. **约束维度**：
   - 金额上限：令牌只能用于指定金额以内的交易
   - 货币限制：仅限特定货币结算
   - 时间窗口：超时自动失效
   - 商家绑定：可限制只能被特定商家使用
   - 单次使用：使用后自动注销防止重复扣款

3. **生命周期**：
   - 买家在 AI 平台授权创建 SPT
   - AI 平台发放 SPT 给 Agent
   - Agent 持有 SPT 并传递给商家
   - 商家使用 SPT 创建 PaymentIntent 完成支付
   - 通过 Webhook 通知各方使用状态

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Stripe]] — developed_by
- [[Agentic Commerce Protocol]] — integrated_with
- [[Machine Payments Protocol]] — complementary
- [[PaymentIntent]] — related_concept