---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, tools, protocol, ai-framework, AI工程]
aliases: ["Tool Use", "工具使用协议", "tool_use 协议", "Anthropic Tool Use", "OpenAI Tool Use"]
relates_to: 
  - target: "[[Tool System]]"
    type: extends
  - target: "[[Write-Tools]]"
    type: base_for
  - target: "[[Claude Code]]"
    type: implemented_by
  - target: "[[OpenAI]]"
    type: protocol_by
  - target: "[[Anthropic]]"
    type: protocol_by
supersedes: null
---

# Tool-Use

## 概述
Tool-Use 是 [[Anthropic]] 和 [[OpenAI]] 等 LLM [[服务]]商提供的标准化工具调用协议，允许 LLM 以结构化方式调用外部工具。[[Write-Tools]] 正是基于此协议的具体实现。

## 关键内容
1. **协议标准**：所有主流框架均遵循 [[Anthropic]] / [[OpenAI]] `tool_use` 协议，为工具调用提供了统一的[[接口规范]]，使 LLM 能够请求执行特定功能并接收返回结果。

2. **调用流程**：LLM 生成工具调用请求，包含工具名称和参数，然后由工具执行器解析并实际执行，最后将结果返回给 LLM 以继续推理过程。

3. **结构化输出**：`tool_use` 协议使得 LLM 能够产生结构化的工具调用，而非非结构化文本，这极大地提高了工具调用的可靠性和安全性。

4. **生态兼容性**：基于统一协议，不同厂商的模型可以使用相同的工具接口，促进了 AI 工具生态的互操作性。

## 来源
- [[write-tools.md]] — 二、工具 Schema 与多粒度设计

## 相关
- [[Write-Tools]] — relates_to
- [[Tool System]] — relates_to
- [[Claude Code]] — relates_to
- [[Anthropic]] — relates_to
- [[OpenAI]] — relates_to