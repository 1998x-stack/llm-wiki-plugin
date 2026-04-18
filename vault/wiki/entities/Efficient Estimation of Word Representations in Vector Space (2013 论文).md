---
type: entity
entity_type: paper
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
- 词嵌入
aliases:
- Efficient Estimation of Word Representations in Vector Space
- Word2Vec 论文
- Mikolov 2013 论文
relates_to:
- target: "[[Tomas Mikolov]]"
  type: caused_by
  confidence: 0.99
  note: 第一作者
- target: "[[Word2Vec]]"
  type: caused
  confidence: 0.99
  note: 提出 Word2Vec 模型
- target: "[[Skip-gram]]"
  type: caused
  confidence: 0.99
  note: 提出 Skip-gram 架构
- target: "[[CBOW（连续词袋模型）]]"
  type: caused
  confidence: 0.99
  note: 提出 CBOW 架构
- target: "[[负采样（Negative Sampling）]]"
  type: caused
  confidence: 0.99
  note: 提出负采样训练方法
- target: "[[词嵌入（Word Embedding）]]"
  type: implements
  confidence: 0.99
  note: 实现高效词向量学习
supersedes: null
---

# Efficient Estimation of Word Representations in Vector Space (2013 论文)

## 概述

Mikolov 等人于2013年发表的《Efficient Estimation of Word Representations in Vector Space》，提出了 [[Word2Vec]] 模型，开创了[[词嵌入（Word Embedding）|词嵌入]]时代，将语义推理转化为向量算术。

## 关键内容

### 论文信息

| 条目 | 内容 |
|------|------|
| **标题** | Efficient Estimation of Word Representations in Vector Space |
| **作者** | [[Tomas Mikolov]], Kai Chen, Greg Corrado, [[Jeffrey Dean]] |
| **发表时间** | 2013年 |
| **会议** | ICLR Workshop |
| **机构** | [[Google]] |

### 核心创新

- **[[Skip-gram]] 架构**：用中心词预测[[上下文窗口]]内的词，对低频词效果尤佳
- **[[CBOW（连续词袋模型）]] 架构**：用上下文词的平均向量预测中心词，训练更快
- **[[负采样（Negative Sampling）]]**：用 K 个随机负样本代替全量 Softmax，速度提升 1000 倍以上
- **高频词下采样**：丢弃概率 P(wᵢ) = 1 - √(t / freq(wᵢ))，减少无信息高频词影响

### 语义发现

训练后的 300 维向量空间展现出惊人的线性语义关系：
- king - man + woman ≈ queen（性别类比）
- Paris - France + Italy ≈ Rome（国家-首都关系）
- walked - walk + swim ≈ swam（动词时态变化）

### 工程效率

- [[负采样]]策略：按词频的 3/4 次方采样 P(w) ∝ freq(w)^(3/4)
- 亿级语料可在几小时内训练完毕
- 使用 Sparse[[Adam（自适应矩估计）|Adam 优化器]]，学习率线性衰减

### 历史影响

- 开创了 [[词嵌入（Word Embedding）]] 时代
- 成为 NLP [[预训练-微调范式]]的先驱
- 直接启发了 [[GloVe]]（2014）、[[FastText]]（2016）、[[ELMo]]（2018）、[[BERT]]（2018）等后续模型

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Tomas Mikolov]] — 第一作者
- [[Word2Vec]] — 提出的模型
- [[Skip-gram]] — 提出的架构
- [[CBOW（连续词袋模型）]] — 提出的架构
- [[负采样（Negative Sampling）]] — 提出的训练方法
- [[词嵌入（Word Embedding）]] — 实现的技术
