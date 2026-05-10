---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [技术, AI, 工具, AI工程]
aliases:
- KV Cache Hit Rate
- KV 缓存命中率
- KV-Cache
- 前缀缓存
relates_to:
- target: "[[提示词缓存]]"
  type: implements
  confidence: 0.95
- target: "[[Context-Engineering]]"
  type: part_of
  confidence: 0.9
- target: "[[注意力预算]]"
  type: related_to
  confidence: 0.85
supersedes: null
---

# KV 缓存命中率

## 概述

KV 缓存命中率是生产阶段 AI Agent 的关键性能指标，衡量推理请求中多少输入 token 可以利用已缓存的 Key-Value 对，直接影响延迟（TTFT）和成本——缓存命中与未命中的成本差异可达 10 倍。

## 关键内容

### 为什么对 Agent 特别重要

典型 Agent 的运行模式导致**输入/输出 token 比例高度倾斜**：
- Agent 通过工具使用链完成任务，每步的动作和观察结果追加到上下文
- 输出通常是结构化的函数调用，保持相对简短
- 以 [[Manus]] 为例：平均输入与输出 token 比例约 **100:1**
- 这使得 Agent 相比聊天机器人更依赖预填充阶段的优化

### 成本影响

以 [[Claude_Code|Claude]] Sonnet 为例：
- 缓存输入 token：**$0.30/百万 token**
- 未缓存输入 token：**$3.00/百万 token**
- **相差 10 倍**

### 提高 KV 缓存命中率的三大实践

#### 1. 保持提示前缀稳定

由于 LLM 的**[[AR 模型（自回归模型）|自回归]]**特性，即使是单个 token 的差异也会使该标记之后的缓存失效。

**常见错误**：在系统提示开头包含时间戳（尤其是精确到秒的）——虽然让模型知道当前时间，但会降低缓存命中率。

#### 2. 使上下文只追加

- 避免修改之前的动作或观察
- 确保序列化是确定性的
- **注意**：许多编程语言和库在序列化 JSON 对象时不保证键顺序的稳定性，会悄无声息地破坏缓存

#### 3. 明确标记缓存断点

- 某些模型提供商或推理框架不支持自动增量前缀缓存
- 需要在上下文中手动插入缓存断点
- 分配断点时要考虑潜在的缓存过期问题
- 至少确保断点包含系统提示的结尾

### 自托管模型的额外优化

如果使用 vLLM 等框架自托管模型：
- 确保启用了**前缀/[[提示词缓存|提示缓存]]**
- 使用会话 ID 等技术在分布式工作节点之间一致地路由请求

### 与工具动态变化的冲突

在 Agent 系统中，工具定义通常位于上下文前部（系统提示之前或之后）。**任何工具定义的更改都会使后续所有动作和观察的 KV 缓存失效**。

这是 [[Manus]] 选择"遮蔽而非移除"工具策略的重要原因之一——通过 logits 掩码约束动作选择，而非动态增删工具定义，从而保持缓存稳定。

### 与提示词缓存的关系

[[提示词缓存]]（[[提示词缓存|Prompt Caching]]）是 [[Anthropic]] API 层面的缓存机制，通过 `cache_control` 断点实现。KV 缓存是更底层的推理引擎优化。两者协同工作：
- KV 缓存优化相同前缀的复用
- [[提示词缓存]]标记哪些部分应该被缓存
- 在系统提示末尾添加 `cache_control` 断点，将系统提示与对话内容分开缓存

## 来源

- [[raw/articles/ai-engineering/claude-blog/AI代理的上下文工程：构建Manus的经验教训.md]] — Manus 上下文工程实践

## 相关

- [[提示词缓存]] — implements（KV 缓存是提示词缓存的底层机制）
- [[Context-Engineering]] — part_of（KV 缓存优化是上下文工程的核心技术手段）
- [[注意力预算]] — related_to（缓存优化间接扩展了有效注意力预算）
