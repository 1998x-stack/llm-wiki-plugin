---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, NLP, GPT, LLM, AI工程]
aliases: [Brown et al. 2020, GPT-3 论文]
relates_to:
  - target: Tom Brown
    relation: authored_by
  - target: GPT 系列
    relation: extends
  - target: 少样本学习
    relation: demonstrated
  - target: 涌现能力
    relation: demonstrated
supersedes: null
---

# Language Models are Few-Shot Learners (2020 论文)

## 概述
[[GPT-3]] 论文，展示 1750 亿参数[[Language-Model|语言模型]]的[[涌现能力]]和[[少样本学习]][[规范化理论|范式]]。

## 关键内容

1. **规模扩展**：[[GPT-3]] 将参数扩展到 1750 亿，展示了模型规模与能力之间的幂律关系。
2. **[[涌现能力]]**：当模型达到临界规模时，涌现出训练时未明确教授的能力，如推理、[[代码生成]]、数学[[计算]]等。
3. **[[少样本学习|少样本]]提示**：通过少量示例（few-shot prompting）即可引导模型完成新任务，改变了人机交互[[规范化理论|范式]]。

## 来源
- [[ai_papers_timeline.md]] — 2020 年时间线条目

## 相关
- [[Tom Brown]] — authored_by
- [[GPT 系列]] — extends
- [[少样本学习]] — demonstrated
- [[涌现能力]] — demonstrated
