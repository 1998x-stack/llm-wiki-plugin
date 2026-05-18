---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, reasoning, AI工程]
aliases: ["自洽性", "Self-Consistency"]
relates_to: []
supersedes: null
---

# Self-Consistency

## 概述
Self-Consistency 是一种通过多次采样取多数答案来提高推理准确率的技术。

## 关键内容

1. **基本原理**：
   - 多次运行相同的 Prompt 生成多个候选答案
   - 通过投票或其他聚合方法选择最一致的答案
   - 显著提升数学推理和逻辑推理的准确率

2. **技术特点**：
   - 多次采样策略：生成多个独立的回答
   - 投票机制：选择最频繁或最一致的答案
   - 特别适用于数学/逻辑推理任务
   - 通过多样性减少单次生成的随机性影响

3. **应用场景**：
   - 数学推理问题
   - 逻辑推理任务
   - 需要高准确率的任务

## 来源
- [[AI-Agent--01_prompt_engineering]] — 高级技术部分中的 Self-Consistency

## 相关
- [[Chain-of-Thought]] — extends
- [[Prompt-Engineering]] — relates_to
- [[In-Context-Learning]] — relates_to