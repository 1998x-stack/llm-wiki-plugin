---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["AI工程", "Agent系统"]
aliases: ["Advisor Tool", "顾问工具", "多模型协作"]
relates_to:
  - target: "[[扩展思维]]"
    type: uses
    confidence: 0.85
  - target: "[[工具与框架]]"
    type: part_of
    confidence: 0.8
  - target: "[[零数据保留]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# Advisor Tool（顾问工具）

## 概述
[[Anthropic]] [[Claude_Code|Claude]] API 的 Advisor 模式是一种[[服务]]端多模型协作机制，允许在单次 HTTP 请求内部由廉价模型（Sonnet/Haiku）执行主任务，在关键时刻调用昂贵模型（Opus）进行策略审阅，实现接近 Opus 质量、接近 Sonnet 成本的效果。

## 关键内容

1. **核心设计哲学**：打破多模型协作必须多次 HTTP 往返的惯例。传统框架（LangGraph、AutoGen）需要 N 次网络往返，而 Advisor 模式在单次 `/v1/messages` 请求内部完成 Executor→Advisor→Executor 的完整协作流程。

2. **触发流程**：
   - Executor 生成文本时触发 `server_tool_use(name="advisor")`
   - [[服务]]端将完整 transcript（system+tools+history）发给 Advisor（Opus）
   - Advisor 使用[[扩展思维]]独立推理，流式暂停但发送 keepalive pings
   - Advisor 返回 `advisor_tool_result`（仅最终建议文本，不含 thinking blocks）
   - Executor 接收建议后继续流式生成

3. **关键设计决策**：
   - **`input: {}` 永远为空**：Advisor 自动获得完整上下文，不允许 Executor"选择性隐瞒"，防止 prompt injection 链路
   - **Thinking blocks 被丢弃**：仅返回 400-700 tokens 的建议文本，防止 Executor 被推理过程干扰，保持自主性
   - **信息对称设计**：Advisor 比 Executor 信息更全，但 Executor 看不到 Advisor 的推理链

4. **`advisor_redacted_result` 加密变体**：返回 `encrypted_content` 字段，客户端无法读取但必须原样传回，[[服务]]端解密后注入 Executor 上下文。用于企业 ZDR 场景和敏感建议隔离。

5. **三层设计意图**：
   - 协议层：一次请求内部完成多模型协作，无网络往返延迟
   - 认知层：Advisor 是"策略审阅器"而非"另一个执行者"，只给高层建议
   - 经济层：昂贵模型只做关键决策，廉价模型完成 bulk generation

6. **正确使用模式**：需正确处理两种变体（`advisor_result` 可读 vs `advisor_redacted_result` 不可读），并在后续请求中原样传回加密内容。

## 来源
- [[advisor_deep_analysis]] — Anthropic Advisor Tool 底层逻辑深度分析

## 相关
- [[扩展思维]] — uses
- [[工具与框架]] — part_of
- [[零数据保留]] — relates_to
