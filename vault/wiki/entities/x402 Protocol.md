---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [protocol, http, coinbase, cloudflare]
aliases: ["x402", "HTTP 402", "HTTP 402 Protocol"]
relates_to:
  - target: "[[Coinbase]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Cloudflare]]"
    type: supports_through
    confidence: 0.85
  - target: "[[Machine Payments Protocol]]"
    type: subset_of
    confidence: 0.8
supersedes: null
---

# x402

## 概述
x402 是 [[Coinbase]] 推动的 HTTP 402 状态码复兴计划，将沉睡 30 年的状态码"Payment Required"正式定义为互联网支付标准。

## 关键内容

1. **历史背景**：
   - HTTP 402 状态码自 1991 年 HTTP/1.0 规范起存在，但从未正式定义或广泛使用
   - [[Coinbase]] 决定激活这个状态码用于支付场景

2. **x402 与 MPP 的关系**：
   - x402 专注于链上支付和稳定币
   - MPP 是更完整的生产实现，支持多种支付方式（包括 x402）
   - 两者可视为：x402 是子集，MPP 是超集

3. **核心交互流程**：
   - 客户端请求受保护资源
   - [[服务]]端返回 402 Payment Required，包含支付要求
   - 客户端完成链上支付
   - 客户端重新请求并携带支付凭证
   - [[服务]]端验证后返回资源

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Coinbase]] — developed_by
- [[Cloudflare]] — supports_through
- [[Machine Payments Protocol]] — subset_of
- [[HTTP]] — protocol_basis
- [[x402 Foundation]] — promotes_standard