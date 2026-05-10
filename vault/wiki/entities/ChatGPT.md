---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-model, language-model, openai, chatbot]
aliases: ["ChatGPT", "Chat Generative Pre-trained Transformer"]
relates_to: 
  - target: "[[Language-Model]]"
    type: part_of
    confidence: 0.9
  - target: "[[OpenAI]]"
    type: created_by
    confidence: 0.9
  - target: "[[GPT-3]]"
    type: extends
    confidence: 0.8
  - target: "[[Prompt-Engineering]]"
    type: popularized
    confidence: 0.9
entity_type: project
supersedes: null
---

# ChatGPT

## 概述
ChatGPT 是 [[OpenAI]] 于2022年11月发布的对话式[[Language-Model|语言模型]]，基于 [[GPT-3]].5 架构并通过人类反馈[[强化学习]](RLHF)进行对齐训练。

## 关键内容

1. **技术特点**：
   - 基于 [[GPT-3]].5 架构，采用 RLHF([[RLHF|Reinforcement Learning from Human Feedback]]) 技术进行对齐训练
   - 专注于对话式交互，能够理解和回应复杂的多轮对话
   - 具备指令跟随能力，能够根据用户要求执行各种任务

2. **社会影响**：
   - 2022年11月发布后迅速普及，让数百万人首次体验到如何通过提问技巧影响AI回答质量
   - 证明了"怎么问"比"怎么答"更重要，推动了 [[Prompt Engineering]] 的广泛应用
   - 引发了人工智能领域的广泛关注和投资热潮

3. **重要贡献**：
   - 使 [[Prompt Engineering]] 从学术研究走向大众应用
   - 展示了对齐训练对于实用AI系统的重要性
   - 推动了整个AI行业对于人机交互界面设计的重视

## 来源
- [[ai-engineering--01_prompt_engineering]] — 技术土壤部分提及
- [[GPT-3]] — 技术演进关系

## 相关
- [[GPT-3]] — extends
- [[InstructGPT]] — successor
- [[Prompt-Engineering]] — popularized
- [[OpenAI]] — created_by