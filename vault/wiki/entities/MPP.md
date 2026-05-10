---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [payments, api, protocol]
aliases: ["Machine Payments Protocol"]
relates_to: []
supersedes: null
entity_type: project
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# MPP

## 概述
MPP（[[Machine Payments Protocol]]）由[[Tempo Labs]]与[[Stripe]]联合设计，基于[[x402 Protocol|HTTP 402]]状态码，已提交IETF规范草案。

## 关键内容
1. **核心定位**：MPP解决任何API向任何客户端（Agent/App/人类）收取费用的问题，无需注册、无需API Key，是"按请求付费"的互联网原语。

2. **协议流程**：采用5步握手流程：GET请求→[[x402 Protocol|HTTP 402]]响应→客户端完成支付→重试请求→获得资源。

3. **支付方式**：设计为支付方式无关（payment-method-agnostic），支持[[Tempo]]（USDC.e）、[[Stripe]]（Card）、Lightning（BTC）、Solana等多种方式。

## 来源
- [[agentic-commerce-deep-dive.md]] — 详细描述了MPP协议的各个方面
- [[]] — 
- [[]] — 

## 相关
- [[Tempo Labs]] — co-develops
- [[Stripe]] — co-develops
- [[Tempo]] — settlement_layer