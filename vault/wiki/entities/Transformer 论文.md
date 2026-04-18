---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
  - 技术
  - 研究
  - 历史
  - 计算理论
  - 深度学习
aliases:
- Attention Is All You Need
- Transformer 论文
- Vaswani 2017 论文
relates_to:
- target: "[[Ashish Vaswani]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Transformer 架构]]"
  type: caused
  confidence: 0.99
  note: 首次提出 Transformer 架构
- target: "[[自注意力机制]]"
  type: caused
  confidence: 0.99
  note: 核心创新
- target: "[[函数式编程]]"
  type: compares_to
  confidence: 0.6
  note: 两者都关注计算的组合性
- target: "[[MapReduce]]"
  type: compares_to
  confidence: 0.6
  note: 两者都通过并行化实现大规模计算
supersedes: null
---

# Transformer 论文

## 概述

Vaswani 等人于2017年发表的《Attention Is All You Need》，提出了完全基于[[注意力机制（Attention Mechanism）|注意力机制]]的 [[Transformer 架构]]，开启了大语言模型与通用人工智能的新纪元。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | Attention Is All You Need |
| **作者** | [[Ashish Vaswani]], [[Noam Shazeer]], Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin |
| **发表时间** | 2017年 |
| **会议** | NeurIPS 2017 |
| **引用量** | 超过13万次 |

### 核心创新

- **完全抛弃循环和卷积**：仅用[[注意力机制（Attention Mechanism）|注意力机制]]完成序列建模
- **[[自注意力机制]]**：O(1) 路径长度，任意位置直接连接
- **[[多头注意力]]**：8个头同时学习不同的关注模式
- **[[位置编码]]**：用正弦/余弦函数补偿位置信息

### 实验结果

- WMT 2014 英德翻译：28.4 BLEU（超越此前所有模型2+ BLEU）
- WMT 2014 英法翻译：41.0 BLEU（单模型新纪录）
- 训练时间：8块 P100 GPU 仅需3.5天

### 历史影响

- 八位作者中多人创办了 Cohere、Adept AI、Character.AI 等明星公司
- 开启了 BERT、GPT、ViT 等后续革命
- 成为当代人工智能的"[[操作系统]]"

## 来源

- [[raw/books/计算机科学/20-vaswani-transformer.md]]
- [[raw/articles/ai-papers/machine-learning/14_transformer_2017.md]] — 完整代码实现 + RNN并行化困境分析 + 架构演变图

## 相关

- [[Ashish Vaswani]] — 第一作者
- [[Transformer 架构]] — 首次提出
- [[自注意力机制]] — 核心创新
- [[函数式编程]] — 计算的组合性
- [[MapReduce]] — 并行化计算
