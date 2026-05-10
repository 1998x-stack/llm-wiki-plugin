---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [payments, commerce, protocol]
aliases: ["Agentic Commerce Protocol"]
relates_to: []
supersedes: null
entity_type: project
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# ACP

## 概述
ACP（[[Agentic Commerce Protocol]]）是由[[Stripe]]与[[OpenAI]]联合开发的商务协议，解决AI Agent如何与商家完成完整购物的问题。

## 关键内容
1. **协议定位**：ACP是商务协议层，而非底层支付机制，处理"Agent如何与商家完成一次完整购物"的问题。

2. **核心流程**：包含四个主要步骤：发送购物意图→返回商品清单+结账[[Configuration|配置]]→提交结账请求→返回订单确认。

3. **商家集成**：商家需实现特定端点（REST或MCP均可），包括[[Configuration|配置]]发现、商品搜索、结账会话等接口。

## 来源
- [[agentic-commerce-deep-dive.md]] — 详细描述了ACP协议的各个方面
- [[]] — 
- [[]] — 

## 相关
- [[Stripe]] — co-develops
- [[OpenAI]] — co-develops
- [[Agentic Commerce]] — core_protocol