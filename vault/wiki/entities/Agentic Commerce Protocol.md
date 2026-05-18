---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-commerce, protocol, stripe, openai, AI工程]
aliases: ["ACP", "Agentic Commerce Protocol", "智能代理商务协议"]
relates_to:
  - target: "[[Stripe]]"
    type: developed_with
    confidence: 0.9
  - target: "[[OpenAI]]"
    type: developed_with
    confidence: 0.9
  - target: "[[Shared Payment Tokens]]"
    type: integrates_with
    confidence: 0.85
  - target: "[[Machine Payments Protocol]]"
    type: complements
    confidence: 0.8
supersedes: null
---

# Agentic Commerce Protocol

## 概述
[[Agentic Commerce]] Protocol (ACP) 是由 [[Stripe]] 和 [[OpenAI]] 联合开发的商务协议，用于解决 AI Agent 与商家之间的完整购物流程问题。

## 关键内容

1. **核心定位**：
   - 解决 AI Agent 如何与商家完成完整购物的问题，而非底层支付机制
   - Apache 2.0 开源协议
   - 首个上线的 AI 平台实现是 [[OpenAI]] [[ChatGPT]]

2. **协议流程**：
   - Agent 发送购物意图给商家 ACP 端点
   - 商家返回商品清单和结账[[Configuration|配置]]
   - Agent 提交结账请求并完成支付
   - 商家返回订单确认

3. **端点规范**：
   - GET `/.well-known/acp-configuration` - 发现[[Configuration|配置]]
   - POST `/acp/v1/catalog/search` - 商品搜索
   - POST `/acp/v1/checkout/sessions` - 创建结账会话
   - GET `/acp/v1/checkout/sessions/{id}` - 查询会话状态
   - POST `/acp/v1/checkout/sessions/{id}/complete` - 完成结账

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Stripe]] — developed_with
- [[OpenAI]] — developed_with
- [[Shared Payment Tokens]] — integrates_with
- [[Machine Payments Protocol]] — complements
- [[Agentic Commerce Suite]] — extends