---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags:
- 机器学习
- 深度学习
- NLP
- 表示学习
aliases:
- Word Embedding
- 词嵌入
- 词向量
- 词表示
relates_to:
- target: "[[Word2Vec]]"
  type: implements
  confidence: 0.99
  note: 代表性实现
- target: "[[Skip-gram]]"
  type: implements
  confidence: 0.95
  note: 实现方法之一
- target: "[[CBOW（连续词袋模型）]]"
  type: implements
  confidence: 0.95
  note: 实现方法之一
- target: "[[负采样（Negative Sampling）]]"
  type: implements
  confidence: 0.9
  note: 训练优化方法
- target: "[[GloVe]]"
  type: implements
  confidence: 0.9
  note: 后续实现方法
- target: "[[FastText]]"
  type: implements
  confidence: 0.9
  note: 后续实现方法
- target: "[[ELMo]]"
  type: extends
  confidence: 0.9
  note: 上下文相关的词向量
- target: "[[BERT]]"
  type: extends
  confidence: 0.9
  note: 完全上下文化的表示
supersedes:
- One-hot 编码
---

# 词嵌入（Word Embedding）

## 概述

[[词向量（Word Embedding）|词嵌入]]是将词语映射为稠密低维实数向量的技术，使语义相似的词在向量空间中距离相近，是现代 NLP 的基础表示方法。

## 关键内容

### 传统方法的局限

在[[词向量（Word Embedding）|词嵌入]]出现之前，NLP 中通常使用 **One-hot 编码**：
```
词汇表：[猫, 狗, 汽车, 苹果]（共 4 个词）

"猫" → [1, 0, 0, 0]
"狗" → [0, 1, 0, 0]

问题一：维度爆炸（10 万个词 → 10 万维稀疏向量）
问题二：无法表达语义关系
  cosine("猫", "狗") = 0
  cosine("猫", "汽车") = 0    ← 完全相同！
```

### 语言学基础

Firth（1957）的名言：**"A word is characterized by the company it keeps."**（词的意义由其上下文决定）

[[词向量（Word Embedding）|词嵌入]]将这个语言学直觉转化为可学习的神经网络——用上下文预测词或用词预测上下文，训练出稠密、低维、语义丰富的[[词向量]]。

### 代表性实现

1. **[[Word2Vec]]**（2013，[[Google]]）：[[Skip-gram]] + [[CBOW（连续词袋模型）]] + [[负采样（Negative Sampling）]]
2. **[[GloVe]]**（2014，[[斯坦福大学|Stanford]]）：全局词共现[[矩阵分解]] + 局部[[上下文窗口]]
3. **[[FastText]]**（2016，[[Meta|Facebook]]）：子[[词向量（Word Embedding）|词嵌入]]（character n-gram）→ 处理未登录词
4. **[[ELMo]]**（2018，AllenNLP）：深层双向 LSTM → 上下文相关的[[词向量]]
5. **[[BERT]]**（2018，[[Google]]）：[[Transformer 架构|Transformer]] + 预训练 → 完全上下文化的表示

### 语义向量算术

[[Word2Vec]] 训练后的[[词向量]]空间展现惊人的线性语义关系：
- king - man + woman ≈ queen（性别类比）
- Paris - France + Italy ≈ Rome（国家-首都关系）
- walked - walk + swim ≈ swam（动词时态变化）

**几何解释**：向量空间中存在**语义方向（Semantic Direction）**，不同维度方向编码不同的语义概念。

### 历史地位

[[词向量（Word Embedding）|词嵌入]]技术开创了 NLP [[预训练-微调范式]]的先河，是当代大[[Language-Model|语言模型]]内置词[[嵌入表示|嵌入层]]的直系祖先。

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Word2Vec]] — 代表性实现
- [[Skip-gram]] — 实现方法
- [[CBOW（连续词袋模型）]] — 实现方法
- [[负采样（Negative Sampling）]] — 训练优化方法
- [[GloVe]] — 后续实现
- [[FastText]] — 后续实现
- [[ELMo]] — 上下文相关扩展
- [[BERT]] — 完全上下文化扩展
