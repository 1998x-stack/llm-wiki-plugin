---
type: entity
entity_type: person
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags:
- 机器学习
- 深度学习
- NLP
- 人物
aliases:
- Tomas Mikolov
- 托马斯·米科洛夫
relates_to:
- target: "[[Efficient Estimation of Word Representations in Vector Space (2013 论文)]]"
  type: caused
  confidence: 0.99
  note: 第一作者
- target: "[[Word2Vec]]"
  type: caused
  confidence: 0.99
  note: 发明者
- target: "[[Jeffrey Dean]]"
  type: compares_to
  confidence: 0.7
  note: Word2Vec 论文合著者
supersedes: null
---

# Tomas Mikolov

## 概述

Tomas Mikolov 是捷克计算机科学家，[[Word2Vec]] [[Word2Vec|词向量模型]]的发明者，2013年发表《[[Efficient Estimation of Word Representations in Vector Space (2013 论文)|Efficient Estimation of Word Representations in Vector Space]]》开创了[[词嵌入（Word Embedding）|词嵌入]]时代。

## 关键内容

### 学术贡献

- **[[Word2Vec]] 发明者**：提出 [[Skip-gram]] 和 CBOW 两种高效[[词嵌入（Word Embedding）|词向量]]学习架构
- **[[负采样（Negative Sampling）]]**：设计了一种替代全量 Softmax 的高效训练方法，使训练速度提升 1000 倍以上
- **语义向量算术发现**：首次展示[[词嵌入（Word Embedding）|词向量]]空间中的线性语义关系（如 king - man + woman ≈ queen）

### 职业背景

- 曾在 [[Google]] 工作期间发表 [[Efficient Estimation of Word Representations in Vector Space (2013 论文)|Word2Vec 论文]]（2013）
- 合著者包括 Kai Chen、Greg Corrado、[[Jeffrey Dean]]
- 论文发表于 ICLR Workshop，成为 NLP 领域引用量最高的论文之一

### 历史影响

- [[Word2Vec]] 开创了 [[词嵌入（Word Embedding）]] 时代
- 为后续 ELMo、BERT 等预训练语言模型奠定基础
- 其[[词嵌入（Word Embedding）|词向量]]算术发现震惊学界，展示了神经网络学习语义的能力

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 第一作者
- [[Word2Vec]] — 发明
- [[Jeffrey Dean]] — 合著者
