---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, NLP, GPT, AI工程]
aliases: [Radford et al. 2018, GPT-1 论文]
relates_to:
  - target: Alec Radford
    relation: authored_by
  - target: GPT 系列
    relation: introduced
  - target: 预训练-微调范式
    relation: introduced
supersedes: null
---

# Improving Language Understanding by Generative Pre-Training (2018 论文)

## 概述
[[GPT 系列]]开山之作，提出使用生成式预训练学习通用语言表示，再微调下游任务的[[规范化理论|范式]]。

## 关键内容

1. **[[预训练-微调范式]]**：先在大规模无[[标注]]文本上进行生成式预训练，再在特定任务上微调，显著减少[[标注]]数据需求。
2. **[[Transformer]] 解码器**：使用 [[Transformer]] 的解码器部分（带 [[因果掩码]]），[[AR 模型（自回归模型）|自回归]]生成下一个 token。
3. **与 BERT 对比**：GPT 是单向[[Language-Model|语言模型]]，适合生成任务；[[BERT]] 是双向的，适合理解任务。两者互补。

## 来源
- [[ai_papers_timeline.md]] — 2018 年时间线条目

## 相关
- [[Alec Radford]] — authored_by
- [[GPT 系列]] — introduced
- [[预训练-微调范式]] — introduced
- [[BERT]] — compares_to
