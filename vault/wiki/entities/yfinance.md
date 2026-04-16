---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["工具与框架"]
aliases: ["yfinance", "Yahoo Finance Python", "yf"]
relates_to:
  - target: "[[AKShare]]"
    type: compares_to
    confidence: 0.75
  - target: "[[Alpha Vantage]]"
    type: compares_to
    confidence: 0.8
  - target: "[[Baostock]]"
    type: compares_to
    confidence: 0.75
supersedes: null
entity_type: tool
---

# yfinance

## 概述
yfinance 是 Yahoo Finance 非官方 Python 封装库，提供全球市场数据（美股、港股、A 股、E[[TensorFlow|TF]]、加密货币、外汇、期货、指数），完全免费无需 API Key，是研究和原型开发的首选工具，但不建议用于生产交易系统。

## 关键内容

1. **项目概览**：版本 1.2.1（2026-04-07），Python ≥ 3.8，Apache 2.0 License，作者 Ran Aroussi，GitHub Stars 15,000+。

2. **核心风险**：使用 Yahoo Finance 非授权接口，Yahoo 可随时改变接口结构导致功能异常。仅限研究/教育目的，不建议用于生产交易系统。

3. **版本里程碑**：2025-12-22 发布 1.0 重大版本，API 全面重构，新增 Sector/Industry 类；2026-04-07 发布 1.2.1 最新稳定版。

4. **核心 API**：Ticker 对象（行情数据/财务报表/公司信息）、Sector/Industry 类、Options 数据、Holdings 数据、下载批量数据。

5. **优势**：完全免费、无需注册、全球市场覆盖、API 简洁易用。劣势：非官方接口、稳定性无保障、不适合生产环境。

## 来源
- [[yfinance]] — yfinance 深度分析报告

## 相关
- [[AKShare]] — compares_to
- [[Alpha Vantage]] — compares_to
- [[Baostock]] — compares_to
