---
type: entity
entity_type: person
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["技术", "研究", "NLP", "AI研究者"]
aliases: ["Jacob Devlin", "Devlin"]
relates_to:
  - target: "[[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]]"
    type: caused
    confidence: 0.99
    note: 第一作者
  - target: "[[BERT]]"
    type: caused
    confidence: 0.99
    note: BERT 模型第一作者
  - target: "[[Ming-Wei Chang]]"
    type: relates_to
    confidence: 0.9
    note: BERT 论文合作者
  - target: "[[Kenton Lee]]"
    type: relates_to
    confidence: 0.9
    note: BERT 论文合作者
  - target: "[[Kristina Toutanova]]"
    type: relates_to
    confidence: 0.9
    note: BERT 论文合作者
supersedes: null
---

# Jacob Devlin

## 概述

Jacob Devlin 是 [[Google]] AI Language 的研究科学家，[[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)|BERT 论文]]的第一作者，对双向预训练语言模型的发展做出了开创性贡献。

## 关键内容

### BERT 论文

2018-2019 年，Jacob Devlin 作为第一作者与 [[Ming-Wei Chang]]、[[Kenton Lee]]、[[Kristina Toutanova]] 共同发表了《[[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)|BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding]]》（NAACL 2019）。该论文提出了：

1. **[[掩码语言模型（MLM）]]**：通过随机掩盖输入词并预测，实现真正双向语言理解
2. **[[下一句预测（NSP）]]**：句子对分类任务，使模型理解句子间关系
3. **[[预训练-微调范式]]**：确立了 NLP 的标准开发模式

### 研究影响

[[BERT]] 模型一次性刷新 11 项 NLP 基准，包括 GLUE（+7.7）、SQuAD 2.0（+10.0），成为 NLP 历史上最具影响力的工作之一。BERT 的"预训练+微调"[[规范化理论|范式]]至今仍是 NLP 领域的基础方法论。

### 所属机构

[[Google]] AI Language — [[Google]] 的自然语言处理研究团队。

## 来源

- [[raw/articles/ai-papers/machine-learning/15_bert_2018.md]] — BERT 论文作者信息
- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — 原始论文

## 相关

- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — 第一作者
- [[BERT]] — BERT 模型第一作者
- [[Ming-Wei Chang]] — BERT 论文合作者
- [[Kenton Lee]] — BERT 论文合作者
- [[Kristina Toutanova]] — BERT 论文合作者
