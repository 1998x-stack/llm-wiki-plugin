---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [api, llm-api, anthropic, ai-platform, AI工程]
aliases: ["Anthropic Messages API", "Anthropic API"]
relates_to:
  - target: "[[Anthropic]]"
    type: provided_by
  - target: "[[Claude Code]]"
    type: used_by
  - target: "[[Claude (Model)]]"
    type: accesses
  - target: "[[Messages API]]"
    type: part_of
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Anthropic Messages API

## 概述
[[Anthropic]] Messages API 是 [[Anthropic]] 提供的 API 接口，允许开发者直接访问 [[Claude_Code|Claude]] 模型的能力，支持[[消息传递]]模式的交互。

## 关键内容
1. **功能特性**：Messages API 允许开发者以消息交换的方式与 [[Claude_Code|Claude]] 模型进行交互，支持多轮对话、工具调用等功能。

2. **设计理念**：[[Claude Code]] 选择使用 [[Anthropic]] Messages API 是因为它可以直接暴露模型能力，符合 [[Claude Code]] "The product is the model" 的哲学，让模型直接与系统交互。

3. **技术规格**：
   - 支持多种 [[Claude_Code|Claude]] 模型（如 Sonnet、Opus 等）
   - 提供流式响应支持
   - 支持工具调用和函数调用
   - 支持[[Context Management|上下文管理]]和长对话保持

4. **在 [[Claude Code]] 中的应用**：作为 [[Claude Code]] 与 [[Anthropic]] 模型通信的主要接口，使 [[Claude Code]] 能够直接利用模型的推理和生成能力。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[Anthropic]] — provided_by
- [[Claude Code]] — used_by
- [[Claude (Model)]] — accesses
- [[Messages API]] — part_of

## 指令