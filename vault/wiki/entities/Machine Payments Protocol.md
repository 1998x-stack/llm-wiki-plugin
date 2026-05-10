---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-commerce, protocol, tempo-labs, stripe]
aliases: ["MPP", "Machine Payments Protocol"]
relates_to:
  - target: "[[Tempo Labs]]"
    type: developed_with
    confidence: 0.9
  - target: "[[Stripe]]"
    type: developed_with
    confidence: 0.9
  - target: "[[HTTP 402]]"
    type: builds_upon
    confidence: 0.85
  - target: "[[Agentic Commerce Protocol]]"
    type: complements
    confidence: 0.8
supersedes: null
---

# Machine Payments Protocol

## 概述
[[Machine Payments]] Protocol (MPP) 由 [[Tempo Labs]] 和 [[Stripe]] 联合设计，基于 [[x402 Protocol|HTTP 402]] 状态码的支付协议，已提交 IETF 规范草案。

## 关键内容

1. **核心定位**：
   - 解决任何 API 如何向任何客户端（Agent/App/人类）收取费用，无需注册、API Key
   - 被称为"按请求付费"的互联网原语，是对 API Key 的革命性替代

2. **协议流程**：
   - 客户端发起请求
   - [[服务]]端返回 [[x402 Protocol|HTTP 402]] Payment Required 及支付选项
   - 客户端完成支付（签名/转账/扣款）
   - 客户端再次发起请求，携带支付凭证
   - [[服务]]端验证后返回资源和支付收据

3. **支持的支付方式**：
   - [[Tempo]] (USDC.e)：微支付、Agent 间支付，~0.6s 最终确认
   - [[Stripe]] (Card)：传统法币支付，T+1 结算
   - Lightning (BTC)：极小额、即时，链下通道毫秒级
   - Solana：高频微支付，低手续费

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Tempo Labs]] — developed_with
- [[Stripe]] — developed_with
- [[HTTP 402]] — builds_upon
- [[Agentic Commerce Protocol]] — complements
- [[IETF]] — standard_body