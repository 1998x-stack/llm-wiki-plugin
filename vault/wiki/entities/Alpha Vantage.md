---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["Alpha Vantage", "NASDAQ 数据 API", "AV API"]
relates_to:
  - target: "[[AKShare]]"
    type: compares_to
    confidence: 0.75
  - target: "[[yfinance]]"
    type: compares_to
    confidence: 0.8
  - target: "[[MCP协议层]]"
    type: uses
    confidence: 0.85
supersedes: null
entity_type: tool
---

# Alpha Vantage

## 概述
Alpha Vantage 是 NASDAQ 官方授权的全球市场数据 API 服务，由 Y Combinator 孵化，提供 100+ API 端点覆盖美股、全球 20+ 交易所、外汇、加密货币、大宗商品、宏观经济，内置 50+ 技术指标，支持 MCP 原生集成。

## 关键内容

1. **定价体系**：2025 年免费配额从 500/天大幅降至 25 次/天，对原型开发影响显著。付费套餐从 $49.99/月（30 次/min）到 $249.99+/月（600+ 次/min）。

2. **核心 API**：股票时间序列（日内/日线/周线/月线的原始和复权版本）、技术指标（50+ 预计算指标如 SMA/EMA/RSI/MACD/BB）、基本面数据、外汇、加密货币、大宗商品、宏观经济。

3. **MCP 支持**：官方 MCP Server，在 AI Agent 生态中处于领先地位。

4. **实时数据**：实时美股数据（非延迟）需额外通过 Alpha X Terminal 完成数据授权流程（FINRA 合规要求）。

## 来源
- [[alpha_vantage]] — Alpha Vantage 深度分析报告

## 相关
- [[AKShare]] — compares_to
- [[yfinance]] — compares_to
- [[MCP协议层]] — uses
