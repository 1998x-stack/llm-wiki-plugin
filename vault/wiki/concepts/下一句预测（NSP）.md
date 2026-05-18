---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [深度学习, NLP, 预训练, BERT, 句子理解, 机器学习]
aliases: ["Next Sentence Prediction", "NSP", "下一句预测", "句子对预测"]
relates_to:
  - target: "[[BERT]]"
    type: part_of
    confidence: 0.95
  - target: "[[掩码语言模型（MLM）]]"
    type: compares_to
    confidence: 0.8
  - target: "[[编码器-解码器架构（Seq2Seq）]]"
    type: relates_to
    confidence: 0.7
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: depends_on
    confidence: 0.85
supersedes: null
---

# 下一句预测（NSP）

## 概述

下一句预测（Next Sentence Prediction, NSP）是 BERT 的第二个预训练任务，通过判断两个句子是否为连续文本，使模型学习句子间关系，对问答、自然语言推理（NLI）等任务有帮助。后续研究发现其贡献有限，RoBERTa 等[[模型选择]]去掉 NSP。

## 关键内容

### 任务设计

NSP 是一个二分类任务：

```
输入格式：[CLS] 句子A [SEP] 句子B [SEP]

50% 情况：B 是 A 的真实下一句 → 标签 IsNext
50% 情况：B 是随机抽取的句子  → 标签 NotNext

目标：[CLS] 位置的输出向量预测 IsNext / NotNext
```

### 输入格式详解

- **[CLS]**：分类 token，其最终隐藏状态聚合了整个输入序列的信息
- **[SEP]**：分隔 token，标记句子边界
- **Segment Embedding**：区分句子 A（全 0）和句子 B（全 1）

模型取 [CLS] 位置的输出向量，经过一个线性分类层预测 IsNext/NotNext。

### 设计动机

NSP 的设计目的是让模型理解**句子间关系**，这对以下任务至关重要：

- **问答（QA）**：判断问题与文档片段的相关性
- **自然语言推理（NLI）**：判断前提与假设之间的蕴含/矛盾/中立关系
- **文本蕴含**：判断两个句子是否表达相同含义

### 与 MLM 的互补性

| 维度 | [[掩码语言模型（MLM）]] | NSP |
|------|------------------------|-----|
| 粒度 | 词级别 | 句子级别 |
| 目标 | 预测被掩盖的词 | 判断句子连续性 |
| 能力 | 双向词义理解 | 句子间关系理解 |
| 输入 | 单句（含掩码） | 句对 |

### 后续争议：NSP 是否必要？

RoBERTa（2019，Facebook）的系统性研究发现：

- **去掉 NSP** 对下游任务性能无显著负面影响
- **原因推测**：MLM 任务本身已隐式学习了句子间关系；NSP 任务过于简单（随机负样本容易被识别）
- **替代方案**：使用连续文本训练（Document-level training），让模型自然接触句子间关系

这一发现影响了后续模型设计：RoBERTa、ALBert、DeBERTa 等均不再使用 NSP。

### 在 BERT 架构中的实现

在 [[BERT]] 的预训练头中，NSP 头（BertNSPHead）是一个简单线性层：

```
[CLS] 输出 → Linear(H, 2) → IsNext/NotNext logits
```

与 MLM 头（预测整个词表）相比，NSP 头极其轻量，仅 2×H+2 个参数。

## 来源

- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — 首次提出 NSP 任务
- [[raw/articles/ai-papers/machine-learning/15_bert_2018.md]] — NSP 机制详解与 RoBERTa 的后续发现

## 相关

- [[BERT]] — part_of（NSP 是 BERT 的第二个预训练任务）
- [[掩码语言模型（MLM）]] — compares_to（BERT 的第一个预训练任务，词级别 vs 句子级别）
- [[编码器-解码器架构（Seq2Seq）]] — relates_to（都涉及句子间关系的建模）
- [[注意力机制（Attention Mechanism）]] — depends_on（NSP 依赖自注意力编码句对表示）
