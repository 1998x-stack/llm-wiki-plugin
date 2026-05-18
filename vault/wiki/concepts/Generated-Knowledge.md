---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, prompt-engineering, knowledge, AI工程]
aliases: ["生成知识", "Generated Knowledge"]
relates_to: []
supersedes: null
---

# Generated Knowledge

## 概述
Generated Knowledge 是一种先生成背景知识再回答问题的技术，特别适用于知识密集型任务。

## 关键内容

1. **基本原理**：
   - 首先生成相关的背景知识或事实
   - 然后利用这些生成的知识来回答原始问题
   - 通过分两步处理提高了知识密集型任务的准确性

2. **技术特点**：
   - 两阶段处理：知识生成 + 问题回答
   - 适用于需要背景知识的任务
   - 提高模型在知识密集型任务上的表现
   - 特别适合模型可能缺乏直接相关信息的场景

3. **应用场景**：
   - 知识密集型问答任务
   - 需要背景信息补充的问题
   - 事实核查和推理任务

## 来源
- [[AI-Agent--01_prompt_engineering]] — 高级技术部分中的 Generated Knowledge

## 相关
- [[Prompt-Engineering]] — relates_to
- [[In-Context-Learning]] — extends
- [[Knowledge-Augmentation]] — extends