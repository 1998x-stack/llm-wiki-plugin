---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags:
- 机器学习
- 深度学习
- NLP
- 词嵌入
aliases:
- Word2Vec
- 词向量模型
- 词嵌入模型
relates_to:
- target: "[[Efficient Estimation of Word Representations in Vector Space (2013 论文)]]"
  type: caused_by
  confidence: 0.99
  note: 论文提出
- target: "[[Tomas Mikolov]]"
  type: caused_by
  confidence: 0.99
  note: 发明者
- target: "[[Skip-gram]]"
  type: implements
  confidence: 0.99
  note: 核心架构之一
- target: "[[CBOW（连续词袋模型）]]"
  type: implements
  confidence: 0.99
  note: 核心架构之一
- target: "[[负采样（Negative Sampling）]]"
  type: implements
  confidence: 0.99
  note: 训练优化方法
- target: "[[词嵌入（Word Embedding）]]"
  type: part_of
  confidence: 0.99
  note: 词嵌入技术的代表
- target: "[[GloVe]]"
  type: compares_to
  confidence: 0.8
  note: 后续词向量模型
- target: "[[FastText]]"
  type: compares_to
  confidence: 0.8
  note: 后续词向量模型
- target: "[[BERT]]"
  type: supersedes
  confidence: 0.85
  note: BERT 的上下文词向量取代了 Word2Vec 的静态词向量
- target: "[[掩码语言模型（MLM）]]"
  type: extends
  confidence: 0.8
  note: MLM 可视为 CBOW 的深度化扩展
supersedes:
- One-hot 编码
---

# Word2Vec

## 概述

Word2Vec 是 [[Google]] 于2013年提出的[[词嵌入（Word Embedding）|词向量]]模型，通过上下文预测任务将词语映射为稠密低维向量，实现语义推理的向量化。

## 关键内容

### 核心思想

基于 Firth（1957）的语言学直觉："A word is characterized by the company it keeps."（词的意义由其上下文决定）。Word2Vec 将这一语言学直觉转化为可学习的神经网络。

### 两种架构

1. **[[Skip-gram]]**：用中心词预测[[上下文窗口]]内的词。对低频词和生僻词效果更好，是论文重点推荐的模型
2. **[[CBOW（连续词袋模型）]]**：用上下文词的平均向量预测中心词。训练速度更快，但对低频词效果较差

### 训练优化

- **[[负采样（Negative Sampling）]]**：每次只更新正样本 + K 个随机负样本（K=5~20），替代全量 [[Softmax]]，速度提升 1000 倍以上
- **[[负采样]]策略**：按词频的 3/4 次方采样 P(w) ∝ freq(w)^(3/4)
- **高频词下采样**：丢弃概率 P(wᵢ) = 1 - √(t / freq(wᵢ))，t=1e-5，减少 "the"、"a" 等无信息词的影响

### 语义向量算术

训练后的 300 维向量空间展现惊人的线性语义关系：
- king - man + woman ≈ queen（性别类比）
- Paris - France + Italy ≈ Rome（国家-首都关系）
- walked - walk + swim ≈ swam（动词时态变化）
- China - Chinese + Japanese ≈ Japan（语言-国家关系）

**几何解释**：向量空间中存在**语义方向（Semantic Direction）**，某个维度方向编码"皇室"、"国家→首都"、"动词时态"等语义概念。

### 工程实现

- 使用 [[PyTorch]] 实现时，中心词和上下文词各有独立的嵌入[[矩阵]]
- 推荐使用 Sparse[[Adam（自适应矩估计）|Adam 优化器]]，学习率线性衰减
- 典型[[Configuration|配置]]：embed_dim=300, window_size=5, n_negatives=5

### 演化谱系

Word2Vec（2013）→ [[GloVe]]（2014，[[斯坦福大学|Stanford]]）→ [[FastText]]（2016，[[Meta|Facebook]]）→ [[ELMo]]（2018，AllenNLP）→ [[BERT]]（2018，[[Google]]）→ 当今大模型内置词[[嵌入表示|嵌入层]]

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]
- [[raw/articles/ai-papers/foundations/paper_09_word2vec.md]] — 全文精读

## 相关

- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 提出论文
- [[Tomas Mikolov]] — 发明者
- [[Skip-gram]] — 核心架构
- [[CBOW（连续词袋模型）]] — 核心架构
- [[负采样（Negative Sampling）]] — 训练优化方法
- [[词嵌入（Word Embedding）]] — 所属技术领域
