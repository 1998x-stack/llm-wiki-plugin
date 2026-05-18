---
type: concept
status: active
confidence: 0.95
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: [词向量, 分布式表示, NLP, 稠密向量, LLM能力]
aliases: [Word Embedding, 词嵌入, 分布式表示]
relates_to: [Word2Vec, 词向量（Word Embedding）, CBOW（连续词袋模型）, Skip-gram, 分布式假说（Distributional Hypothesis）, BERT]
supersedes: null
---

# 词向量（Word Embedding）

## 概述
将离散词汇映射为稠密低维连续向量空间中的表示，捕捉语义和语法相似性。

## 关键内容

1. **从稀疏到稠密**：相比 one-hot 编码（维度等于词汇量，词之间正交），[[词向量]]将每个词映射为 50-300 维的稠密实值向量。语义相似的词在向量空间中距离更近，支持相似度[[计算]]和语义推理。
2. **语义组合性**：Mikolov 等人发现[[词向量]]具有线性平移特性，如 king - man + woman ≈ queen，表明[[词向量]]能够捕捉语义关系（如性别、时态、国籍等）并进行向量运算。
3. **演进路线**：从静态[[词向量]]（[[Word2Vec]]、GloVe、FastText）到[[上下文感知]][[词向量]]（BERT、ELMo），[[词向量]]技术经历了从"一词一表示"到"一词多表示"的演进，显著提升了 NLP 任务的性能。

[[词向量]]是现代 NLP 的基础组件，几乎所有下游 NLP 任务都依赖高质量的[[词嵌入（Word Embedding）|词表示]]。

## 来源
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — Word2Vec 词向量
- [[BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (2019 论文)]] — 上下文词向量

## 相关
- [[Word2Vec]] — produces
- [[CBOW（连续词袋模型）]] — produces
- [[Skip-gram]] — produces
- [[分布式假说（Distributional Hypothesis）]] — based_on
- [[BERT]] — extends
- [[负采样（Negative Sampling）]] — uses
