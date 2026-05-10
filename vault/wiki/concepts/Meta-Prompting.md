---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [prompt-engineering, advanced-technique, ai-engineering]
aliases: ["元提示", "Meta-Prompting", "Meta Prompting"]
relates_to: 
  - target: "[[Prompt-Engineering]]"
    type: part_of
    confidence: 0.8
  - target: "[[Language-Model]]"
    type: applies_to
    confidence: 0.7
  - target: "[[Self-Consistency]]"
    type: relates_to
    confidence: 0.6
entity_type: concept
supersedes: null
---

# Meta-Prompting

## 概述
Meta-Prompting 是一种高级的[[Prompt Engineering|提示工程]]技术，指使用一个提示词来生成另一个用于解决问题的最佳提示词，然后再使用这个生成的提示词来回答原始问题的技术。

## 关键内容

1. **工作原理**：
   - 首先生成针对特定问题的最佳提示词
   - 然后使用这个生成的提示词来解决问题
   - 本质上是"提示词的提示词"，让模型自我优化其响应策略

2. **应用场景**：
   - 复杂问题分解
   - 任务自适应提示设计
   - 针对特定领域的问题优化
   - 提升模型在复杂推理任务上的表现

3. **技术优势**：
   - 允许模型根据问题特点动态调整解决方案
   - 提高了模型应对多样化任务的灵活性
   - 可以自动生成针对特定问题的优化提示词
   - 在某些复杂推理任务上表现优于传统[[Prompt Engineering|提示工程]]

## 来源
- [[ai-engineering--01_prompt_engineering]] — 核心技术模式部分的元提示介绍

## 相关
- [[Prompt-Engineering]] — part_of
- [[Language-Model]] — applies_to
- [[Self-Consistency]] — relates_to
- [[CO-STAR-Framework]] — relates_to