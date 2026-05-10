---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [语言学, 分布式表示, 词向量, 语义]
aliases: [Distributional Hypothesis, 分布假说]
relates_to: [Word2Vec, 词向量（Word Embedding）, CBOW（连续词袋模型）, Skip-gram, Tomas Mikolov]
supersedes: null
---

# 分布式假说（Distributional Hypothesis）

## 概述
语言学基本假说：语义相似的词倾向于出现在相似的上下文中，即"一个词由其邻居定义"。

## 关键内容

1. **核心思想**：Firth（1957）提出"You shall know a word by the company it keeps"。该假说认为词的语义可以通过其在语料中的上下文分布来推断，上下文相似的词具有相似的语义。
2. **数学形式化**：[[Word2Vec]] 等[[Word2Vec|词向量模型]]将[[分布式假说]]转化为优化问题——学习稠密向量表示，使得上下文相似的词在向量空间中距离更近。
3. **对 NLP 的影响**：[[分布式假说]]是从 one-hot 编码走向[[词向量（Word Embedding）|分布式表示]]的理论基础。它支撑了 [[Word2Vec]]、GloVe、FastText 等[[词向量]]方法，以及后续 BERT 等[[上下文感知]]表示学习。

[[分布式假说]]是现代自然语言处理的理论基石之一，为词的[[词向量（Word Embedding）|分布式表示]]提供了语言学依据。

## 来源
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 实践验证

## 相关
- [[Word2Vec]] — implements
- [[词向量（Word Embedding）]] — enables
- [[CBOW（连续词袋模型）]] — based_on
- [[Skip-gram]] — based_on
- [[Tomas Mikolov]] — relates_to
