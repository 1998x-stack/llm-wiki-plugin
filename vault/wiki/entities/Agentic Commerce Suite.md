---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-commerce, suite, stripe]
aliases: ["ACS", "Agentic Commerce Suite"]
relates_to:
  - target: "[[Stripe]]"
    type: developed_by
    confidence: 0.9
  - target: "[[Agentic Commerce Protocol]]"
    type: implements
    confidence: 0.9
  - target: "[[ChatGPT]]"
    type: supports_platform
    confidence: 0.85
supersedes: null
---

# Agentic Commerce Suite

## 概述
[[Agentic Commerce]] Suite (ACS) 是 [[Stripe]] 于 2025 年 12 月发布的 SaaS 解决方案，将 ACP 集成的工程工作量从数月压缩到几分钟的单击[[Configuration|配置]]。

## 关键内容

1. **产品定位**：
   - ACP 协议的托管实现，[[Stripe]] 托管 ACP 端点、商品目录同步及 AI Agent 对接
   - 解决方案包括商品发现、结账简化和支付风控三大模块

2. **核心模块**：
   - 商品发现：托管 ACP 端点、商品目录上传、实时库存同步
   - 结账简化：Checkout Sessions API、[[Stripe]] Tax、动态运费[[计算]]
   - 支付风控：SPT 处理、[[Stripe]] Radar、欺诈信号监控

3. **集成渠道**：
   - 直接在 [[Stripe]] Dashboard 一键上线
   - 电商平台插件：Wix、WooCommerce、BigCommerce 等
   - 全渠道商务平台：Akeneo、Cymbio、Mirakl 等

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Stripe]] — developed_by
- [[Agentic Commerce Protocol]] — implements
- [[ChatGPT]] — supports_platform
- [[Shared Payment Tokens]] — utilizes