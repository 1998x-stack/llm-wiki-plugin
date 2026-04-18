---
type: concept
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
- 词嵌入
aliases:
- CBOW
- Continuous Bag-of-Words
- 连续词袋模型
- CBOW 模型
relates_to:
- target: "[[Word2Vec]]"
  type: part_of
  confidence: 0.99
  note: Word2Vec 的核心架构之一
- target: "[[Skip-gram]]"
  type: compares_to
  confidence: 0.9
  note: Word2Vec 的另一种架构
- target: "[[Efficient Estimation of Word Representations in Vector Space (2013 论文)]]"
  type: caused_by
  confidence: 0.99
  note: 论文提出
supersedes: null
---

# CBOW（连续词袋模型）

## 概述

CBOW（Continuous Bag-of-Words）是 [[Word2Vec]] 的核心架构之一，通过上下文词的平均向量预测中心词，训练速度较快但对低频词效果较差。

## 关键内容

### 工作原理

```
句子：我 爱 [?] 天安门

输入：{我, 爱, 天安门} 的词向量平均
目标：预测 "北京"
```

与 [[Skip-gram]] 相反，CBOW 用上下文预测中心词：
1. 获取[[上下文窗口]]内所有词的[[词嵌入（Word Embedding）|词向量]]
2. 计算这些[[词嵌入（Word Embedding）|词向量]]的平均值
3. 用平均向量预测中心词

### 与 Skip-gram 的对比

| 特性 | CBOW | [[Skip-gram]] |
|------|------|-----------|
| 预测方向 | 上下文 → 中心词 | 中心词 → 上下文 |
| 训练速度 | 较快 | 较慢 |
| 低频词效果 | 较差 | 更好 |
| 适用场景 | 通用语料 | 生僻词、罕见词 |

### 特点

- **训练更快**：由于使用上下文平均向量，计算效率更高
- **对低频词效果较差**：平均操作会稀释低频词的信息
- **适合大规模语料**：在数据充足的情况下表现良好

### 在 Word2Vec 中的地位

CBOW 和 [[Skip-gram]] 共同构成了 [[Word2Vec]] 的两种核心架构。《[[Efficient Estimation of Word Representations in Vector Space (2013 论文)|Efficient Estimation of Word Representations in Vector Space]]》论文中，[[Skip-gram]] 被作为重点推荐模型，但 CBOW 在训练速度上有优势。

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Word2Vec]] — 所属模型
- [[Skip-gram]] — 对比架构
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 提出论文
