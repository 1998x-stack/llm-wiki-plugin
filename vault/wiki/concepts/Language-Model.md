---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, llm, architecture]
aliases: ["语言模型", "Large Language Model", "LLM"]
relates_to: []
supersedes: null
---

# Language Model

## 概述
语言模型是用于预测文本序列概率分布的人工智能模型，现代大规模语言模型（LLM）能够理解和生成自然语言。

## 关键内容

1. **基本原理**：
   - 语言模型的目标是学习 P(output | input) 的条件概率分布
   - 通过在大规模文本语料上训练，学习语言的统计规律
   - [[Transformer 架构]]中的[[注意力机制（Attention Mechanism）|注意力机制]]使得模型能够捕捉长距离依赖关系

2. **模型规模与能力**：
   - < 1B 参数：Prompt 效果不稳定，few-shot 几乎无效
   - 1B-10B：基础指令跟随能力
   - 10B-100B：CoT 开始稳定工作
   - > 100B：复杂推理、元认知、指令跟随达到实用级别

3. **[[涌现能力]]**：
   - 随着参数规模超过某个阈值，模型展现出[[零样本学习|零样本]]推理、指令跟随等[[涌现能力]]
   - 这些能力在小规模模型中不存在或很弱

## 来源
- [[AI-Agent--01_prompt_engineering]] — 技术土壤和核心技术机理部分

## 相关
- [[In-Context-Learning]] — implements
- [[Prompt-Engineering]] — extends
- [[Transformer]] — implements