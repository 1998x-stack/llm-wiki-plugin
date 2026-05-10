---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, llm, learning]
aliases: ["上下文学习", "In-Context Learning"]
relates_to: []
supersedes: null
---

# In-Context Learning

## 概述
In-Context Learning 是指 LLM 在不更新参数的情况下，仅通过输入上下文中的示例就能学会执行任务的能力。

## 关键内容

1. **基本原理**：
   - P(y | x, examples) >> P(y | x) - 示例在上下文中充当隐式的"软微调"
   - 模型无需更新参数，仅通过[[注意力机制（Attention Mechanism）|注意力机制]]在推理时完成任务适配
   - [[Transformer]] 的[[注意力机制（Attention Mechanism）|注意力机制]]使得每个 token 的生成都受所有上文 token 的影响

2. **发展历程**：
   - 从 [[GPT-3]] 开始显著展现
   - 通过 few-shot、many-shot 示例展示任务意图
   - [[涌现能力]]随着模型规模增大而显现

3. **关键技术**：
   - Zero-shot: 无示例直接任务执行
   - Few-shot: 少量示例指导任务执行
   - Many-shot: 更多样例指导任务执行

## 来源
- [[AI-Agent--01_prompt_engineering]] — 核心技术机理部分中的 In-Context Learning

## 相关
- [[Prompt-Engineering]] — implements
- [[Language-Model]] — extends
- [[Chain-of-Thought]] — relates_to