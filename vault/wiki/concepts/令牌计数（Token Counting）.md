---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [AI工程, 工具, LLM能力]
aliases: ["Token Counting", "令牌估算"]
relates_to:
  - target: "[[上下文窗口（Context Windows）]]"
    type: uses
    confidence: 0.9
  - target: "[[提示词缓存]]"
    type: relates_to
    confidence: 0.8
  - target: "[[上下文压缩（Compaction）]]"
    type: relates_to
    confidence: 0.75
supersedes: null
---

# 令牌计数（Token Counting）

## 概述
Anthropic API 的 `/v1/messages/count_tokens` 端点，用于在发送消息给 Claude 前估算输入令牌数量，帮助主动管理速率限制、成本和模型路由决策。

## 关键内容

1. **工作原理**：令牌计数端点接受与创建消息相同的结构化输入（包括系统提示、工具、图片、PDF），返回 `input_tokens` 总数。该数值为估算值，实际使用时可能有少量偏差。

2. **计费说明**：Token 计数可能包含 Anthropic 为系统优化自动添加的令牌，但系统添加的令牌不会计费，计费仅针对用户内容。

3. **支持模型**：所有活跃模型均支持令牌计数功能。

4. **与[[Context Management|上下文管理]]结合**：支持传入 `context_management` 参数，可预览应用[[上下文编辑]]（如[[上下文编辑|工具结果清除]]、思维块清除）后的令牌使用量。响应返回 `input_tokens`（编辑后）和 `context_management.original_input_tokens`（编辑前）。

5. **与压缩结合**：可检查应用先前压缩操作后的有效令牌计数，帮助判断是否需要触发新的压缩。

6. **使用场景**：
   - 主动管理速率限制和成本
   - 做出智能模型路由决策（如判断是否可以使用更便宜的模型）
   - 将提示词优化为特定长度
   - 调试[[上下文窗口]]溢出问题

## 来源
- [[Token counting]] — Anthropic 官方文档

## 相关
- [[上下文窗口（Context Windows）]] — uses
- [[提示词缓存]] — relates_to
- [[上下文压缩（Compaction）]] — relates_to
