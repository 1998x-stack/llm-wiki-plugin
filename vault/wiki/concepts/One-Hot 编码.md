---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [NLP, 表示学习, 机器学习]
aliases: ["One-Hot Encoding", "独热编码", "独热向量"]
relates_to:
  - target: "[[Word2Vec]]"
    type: superseded_by
    confidence: 0.85
  - target: "[[词向量]]"
    type: improved_by
    confidence: 0.85
supersedes: null
---

# One-Hot 编码

## 概述
One-Hot 编码是一种传统的[[词嵌入（Word Embedding）|词表示]]方法，将词汇表中的每个[[词嵌入（Word Embedding）|词表示]]为一个高维稀疏向量，其中只有一个元素为1，其余均为0。

## 关键内容

1. **表示方式**：
   - 词表大小为 V，则每个[[词嵌入（Word Embedding）|词表示]]为 V 维向量
   - 向量中只有一个位置为 1（对应词的位置），其余位置为 0
   - 如"猫"=[0,0,0,1,0,...,0]，"狗"=[0,0,0,0,1,0,...,0]

2. **主要缺陷**：
   - 维度灾难：词表很大时，向量维度极高，造成存储和[[计算]]压力
   - 语义盲区：任意两个不同词的余弦相似度为0，无法表达语义关系
   - 泛化能力弱：无法捕获词之间的相似性

3. **与[[词向量]]对比**：
   - One-Hot 是稀疏、高维、无语义关系的表示
   - [[词向量]]是稠密、低维、能表达语义关系的表示
   - [[Word2Vec]] 等模型正是为了解决 One-Hot 的缺陷而提出

## 来源
- [[paper_09_word2vec]] — 作为对比方法提及

## 相关
- [[词向量]] — 对比方法
- [[Word2Vec]] — 解决其缺陷
- [[分布式假说]] — 理论替代方法
- [[NLP]] — 应用领域