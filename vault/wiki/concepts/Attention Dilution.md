---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [transformer, attention-mechanism, llm-limitations, context-engineering]
aliases: ["Attention Dilution", "注意力稀释", "Attention稀释", "注意力分散"]
relates_to:
  - target: "[[Transformer架构]]"
    type: based_on
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: motivation_for
    confidence: 0.9
  - target: "[[上下文窗口]]"
    type: constraint_on
    confidence: 0.95
  - target: "[[上下文腐烂]]"
    type: contributes_to
    confidence: 0.9
  - target: "[[信噪比]]"
    type: affects
    confidence: 0.9
supersedes: null
---

# Attention Dilution

## 概述
Attention Dilution（注意力稀释）是指随着 [[Transformer]] 模型[[上下文窗口]]长度增加，每个 token 的平均注意力权重下降的现象。这是 LLM [[Context Management|上下文管理]]的核心限制之一，也是 [[Context Engineering]] 存在的重要动机。

## 关键内容

1. **技术机理**：
   - [[Transformer]] 的 [[Softmax]] Attention 机制：attention(Q,K,V) = softmax(QK^T / √d) · V
   - 当上下文长度 N 增大时，[[Softmax]] 分母增大 → 每个 token 平均注意力权重下降
   - 关键信息被"稀释"在大量噪声中
   - 模型有效"关注"范围存在软上限

2. **对模型性能的影响**：
   - 信息冗余 → 注意力稀释（Lost in the Middle 问题）
   - 模型可能忽略重要的上下文信息
   - 随着上下文增长，召回准确信息的能力下降

3. **工程对策**：
   - 最大化[[信噪比]]（[[信噪比|Signal-to-Noise Ratio]]）
   - 使用位置效应策略：关键信息放在头部或尾部
   - [[上下文压缩]]与选择性保留
   - 滑动窗口和[[分层记忆架构]]

4. **与 [[Context Engineering]] 的关系**：
   - Attention Dilution 是 [[Context Engineering]] 存在的根本原因之一
   - [[Context Engineering]] 的核心任务之一就是对抗注意力稀释的影响
   - 通过信息架构设计最大化有效注意力利用率

## 来源
- [[AI-Agent--02_context_engineering]] — 技术机理描述
- [[]] — 

## 相关
- [[Transformer架构]] — 基础机制
- [[Context-Engineering]] — 对策应用
- [[上下文腐烂]] — 相关现象
- [[上下文窗口]] — 受影响对象
- [[信噪比]] — 优化目标