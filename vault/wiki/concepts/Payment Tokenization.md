---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [payments, security, tokens]
aliases: ["Payment Tokenization", "Secure Payment Tokens"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Payment Tokenization

## 概述
Payment [[文本预处理|Tokenization]]是一种支付安全技术，用唯一的[[符号化]]令牌替换敏感的支付数据，以保护实际的支付信息。

## 关键内容
1. **安全机制**：将敏感的支付信息（如信用卡号）替换为非敏感的令牌，确保真实支付信息不在多方之间传递。

2. **SPT实现**：在[[Agentic Commerce]]中，SPT（[[Shared Payment Tokens|共享支付令牌]]）是支付令牌化的典型应用，使AI Agent能够在不知晓真实卡号的情况下完成支付。

3. **多维约束**：令牌可[[Settings|设置]]金额上限、时间窗口、商家绑定等多种约束条件，增强安全性。

## 来源
- [[agentic-commerce-deep-dive.md]] — 描述了支付令牌化在SPT中的应用
- [[]] — 

## 相关
- [[Shared Payment Tokens]] — implementation
- [[Agentic Commerce]] — secures
- [[Security]] — relates_to