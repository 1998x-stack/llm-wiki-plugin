---
type: entity
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [blockchain, payment, crypto, tempo, AI工程]
aliases: ["Tempo", "Tempo L1 Blockchain"]
relates_to:
  - target: "[[Paradigm]]"
    type: incubated_by
    confidence: 0.9
  - target: "[[Stripe]]"
    type: partnered_with
    confidence: 0.85
  - target: "[[Machine Payments Protocol]]"
    type: settlement_layer_for
    confidence: 0.9
  - target: "[[USDC.e]]"
    type: native_currency
    confidence: 0.9
supersedes: null
---

# Tempo

## 概述
[[Tempo]] 是由 [[Paradigm]] 和 [[Stripe]] 孵化的专用支付 L1 区块链，2026 年 3 月主网上线，专门为稳定币支付而设计。

## 关键内容

1. **核心技术参数**：
   - 出块时间：~0.6 秒，确定性最终确认，无重组风险
   - Gas Token：USD 稳定币，无需持有波动资产
   - 主要资产：USDC.e（bridged USDC）
   - 手续费：极低（设计目标：亚美分级别）

2. **支付专项设计**：
   - 专用支付通道：协议层保障 blockspace，高峰期费用不飙升
   - 稳定币 Gas：用 USDC.e 付手续费，而非原生代币
   - 内置 DEX：稳定币间低滑点兑换
   - 支付元数据：结构化备注字段（发票号/订单号）
   - 确定性结算：0.6s 最终性，无分叉风险
   - 智能账户：批量交易、计划支付、Passkey 签名

3. **在 MPP 生态中的角色**：
   - MPP 的首选区块链结算层
   - MPP 官网 Demo 的默认支付方式

## 来源
- [[agentic-commerce-deep-dive.md]] — 全文分析

## 相关
- [[Paradigm]] — incubated_by
- [[Stripe]] — partnered_with
- [[Machine Payments Protocol]] — settlement_layer_for
- [[USDC.e]] — native_currency
- [[Stablecoin]] — related_concept