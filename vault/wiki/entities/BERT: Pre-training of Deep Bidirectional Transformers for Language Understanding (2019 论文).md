---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["技术", "研究", "NLP", "深度学习", "历史"]
aliases: ["BERT 论文", "Devlin 2019 论文", "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding"]
relates_to:
  - target: "[[Jacob Devlin]]"
    type: caused_by
    confidence: 0.99
    note: 第一作者
  - target: "[[Ming-Wei Chang]]"
    type: caused_by
    confidence: 0.95
    note: 第二作者
  - target: "[[Kenton Lee]]"
    type: caused_by
    confidence: 0.95
    note: 第三作者
  - target: "[[Kristina Toutanova]]"
    type: caused_by
    confidence: 0.95
    note: 第四作者
  - target: "[[BERT]]"
    type: caused
    confidence: 0.99
    note: 首次提出 BERT 模型
  - target: "[[掩码语言模型（MLM）]]"
    type: caused
    confidence: 0.99
    note: 首次提出 MLM 预训练任务
  - target: "[[下一句预测（NSP）]]"
    type: caused
    confidence: 0.95
    note: 首次提出 NSP 预训练任务
  - target: "[[预训练-微调范式]]"
    type: caused
    confidence: 0.95
    note: 确立 NLP 标准范式
  - target: "[[Transformer 论文]]"
    type: extends
    confidence: 0.9
    note: 基于 Transformer Encoder 构建
  - target: "[[Word2Vec]]"
    type: supersedes
    confidence: 0.85
    note: 上下文词向量取代静态词向量
supersedes: null
---

# BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)

## 概述

[[Jacob Devlin|Devlin]] 等人于 2019 年 NAACL 发表的 BERT 论文，提出了双向 [[Transformer 架构|Transformer]] 预训练模型，通过[[掩码语言模型（MLM）|掩码语言模型]]和[[下一句预测（NSP）|下一句预测]]任务学习深层双向语言表示，一次性刷新 11 项 NLP 基准，确立了"预训练+微调"的 NLP 标准[[规范化理论|范式]]。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | BERT: Pre-training of Deep Bidirectional [[Transformer 架构|Transformer]]s for Language Understanding |
| **作者** | [[Jacob Devlin]], [[Ming-Wei Chang]], [[Kenton Lee]], [[Kristina Toutanova]]（[[Google]] AI Language） |
| **发表时间** | 2019 年（arXiv 提交于 2018 年 10 月） |
| **会议** | NAACL 2019 |
| **机构** | [[Google]] AI Language |

### 核心创新

1. **双向预训练**：突破单向语言模型限制，通过 [[掩码语言模型（MLM）]] 实现真正双向上下文理解
2. **多任务预训练**：MLM（词级别）+ [[下一句预测（NSP）]]（句子级别）[[联合训练]]
3. **微调[[规范化理论|范式]]**：预训练权重作为参数初始化，下游任务只需添加简单输出层并微调几个 epoch
4. **架构简洁**：纯 [[Transformer架构]] Encoder 堆叠，无 Decoder，无复杂任务特定架构

### 模型配置

| 配置 | 层数 L | 隐藏维度 H | 注意力头数 A | 参数量 |
|------|--------|-----------|------------|--------|
| BERT-Base | 12 | 768 | 12 | 110M |
| BERT-Large | 24 | 1024 | 16 | 340M |

### 实验结果

一次性刷新 11 项 NLP 基准：

| 任务 | 之前 SOTA | BERT | 提升 |
|------|---------|------|------|
| GLUE | 72.8 | 80.5 | +7.7 |
| SQuAD 1.1 F1 | 91.7 | 93.2 | +1.5（超人类） |
| SQuAD 2.0 F1 | 76.3 | 86.3 | +10.0 |
| MultiNLI | 86.7 | 86.7（Large:90.9）| — |
| CoNLL NER F1 | 91.9 | 92.8 | +0.9 |

### 训练细节

- **语料**：Wikipedia（25 亿词）+ BooksCorpus（8 亿词）
- **优化器**：[[AdamW]]，β₁=0.9，β₂=0.999
- **学习率**：Warmup 10000 步 → 线性衰减
- **Batch Size**：256 sequences（最大长度 512）
- **训练步数**：1,000,000 步
- **硬件**：64 块 TPU v2，训练 4 天（BERT-Large）

### 历史影响

- 确立了"预训练+微调"作为 NLP 的标准[[规范化理论|范式]]
- 催生了 RoBERTa、DistilBERT、ALBert、DeBERTa 等一系列后继模型
- 与 GPT 系列共同开启了大语言模型时代
- HuggingFace transformers 库使 BERT 成为开箱即用的工业标准工具

## 来源

- [[raw/articles/ai-papers/machine-learning/15_bert_2018.md]] — 论文详细解读与代码实现

## 相关

- [[Jacob Devlin]] — 第一作者
- [[Ming-Wei Chang]] — 第二作者
- [[Kenton Lee]] — 第三作者
- [[Kristina Toutanova]] — 第四作者
- [[BERT]] — 首次提出
- [[掩码语言模型（MLM）]] — 核心创新之一
- [[下一句预测（NSP）]] — 核心创新之一
- [[预训练-微调范式]] — 确立 NLP 标准范式
- [[Transformer 论文]] — 架构基础
- [[Word2Vec]] — 被 BERT 的上下文词向量取代
