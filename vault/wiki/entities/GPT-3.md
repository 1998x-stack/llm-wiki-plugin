---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-model, language-model, openai, AI工程]
aliases: ["GPT-3", "Generative Pre-trained Transformer 3"]
relates_to: 
  - target: "[[Language-Model]]"
    type: part_of
    confidence: 0.9
  - target: "[[OpenAI]]"
    type: created_by
    confidence: 0.9
  - target: "[[Prompt-Engineering]]"
    type: influenced
    confidence: 0.8
entity_type: project
supersedes: null
---

# GPT-3

## 概述
GPT-3（[[GPT 系列|Generative Pre-trained Transformer]] 3）是由 [[OpenAI]] 开发的第三代生成预训练变换模型，于2020年发布。它是首个真正展示"few-shot learning"能力的大规模[[Language-Model|语言模型]]。

## 关键内容

1. **技术里程碑**：
   - GPT-3 首次展示了在不进行梯度更新的情况下，仅通过提供少量示例就能完成各种自然语言任务的能力
   - 证明了 LLM 能够从示例中推断任务意图，为 [[Prompt Engineering]] 的诞生奠定了基础
   - 模型参数规模超过1750亿，展现了参数规模与[[涌现能力]]之间的关系

2. **关键贡献**：
   - 展示了大规模[[Language-Model|语言模型]]的[[零样本学习|零样本]]、[[少样本学习]]能力
   - 证明了 [[In-Context-Learning|In-Context Learning]] 的可行性
   - 为后续 [[ChatGPT]]、[[InstructGPT]] 等模型的发展铺平了道路
   - 激发了 [[Prompt Engineering]] 作为一门专门技术领域的发展

3. **影响**：
   - 开启了 [[Prompt Engineering]] 时代，证明了通过精心设计的自然语言指令可以引导模型产生高质量输出
   - 展现了参数规模超过临界点后出现的[[涌现能力|涌现现象]]，推动了大模型研究的发展

## 来源
- [[ai-engineering--01_prompt_engineering]] — 技术土壤部分提及
- [[In-Context-Learning]] — 相关概念

## 相关
- [[Language-Model]] — part_of
- [[OpenAI]] — created_by
- [[Prompt-Engineering]] — influenced
- [[InstructGPT]] — predecessor