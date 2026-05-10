---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Word2Vec, 训练优化, Softmax, 计算效率]
aliases: [Hierarchical Softmax, 层次化 Softmax, Huffman Softmax]
relates_to: [Word2Vec, 负采样（Negative Sampling）, CBOW（连续词袋模型）, Skip-gram, 交叉熵]
supersedes: null
---

# 层次 Softmax（Hierarchical Softmax）

## 概述
[[Word2Vec]] 中使用的训练优化技术，利用霍夫曼树将 [[Softmax]] [[计算]]复杂度从 O(V) 降至 O(log V)。

## 关键内容

1. **霍夫曼树结构**：将词汇表 V 组织为一棵二叉霍夫曼树，频繁词靠近根节点，稀有词靠近叶节点。每个内部节点关联一个 sigmoid 分类器，决定走向左子树还是右子树。
2. **对数复杂度**：预测一个词的概率只需[[计算]]从根到该词叶节点路径上的 sigmoid 值，路径长度为 O(log V)。相比标准 [[Softmax]] 需要[[计算]]所有 V 个词的概率，层次 [[Softmax]] 大幅降低了[[计算]]量。
3. **与[[负采样]]的对比**：层次 [[Softmax]] 和[[负采样（Negative Sampling）]]是 [[Word2Vec]] 的两种训练优化方法。[[负采样]]实现更简单且在大型语料上通常表现更好，层次 [[Softmax]] 在低频[[词嵌入（Word Embedding）|词表示]]上略有优势。

层次 [[Softmax]] 是早期[[词向量]]训练的关键优化技术，使得在大规模语料上训练[[词向量]]变得可行。

## 来源
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 原始提出

## 相关
- [[Word2Vec]] — used_by
- [[负采样（Negative Sampling）]] — compares_to
- [[CBOW（连续词袋模型）]] — used_by
- [[Skip-gram]] — used_by
- [[交叉熵]] — optimizes
