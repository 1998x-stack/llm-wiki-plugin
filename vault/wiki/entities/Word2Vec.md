---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [NLP, 词向量, 神经网络, 表示学习, 机器学习]
aliases: ["Word2Vec", "Efficient Estimation of Word Representations in Vector Space"]
relates_to:
  - target: "[[Tomas Mikolov]]"
    type: authored_by
    confidence: 0.9
  - target: "[[Google]]"
    type: developed_at
    confidence: 0.9
  - target: "[[词向量]]"
    type: implements
    confidence: 0.9
  - target: "[[One-Hot 编码]]"
    type: supersedes
    confidence: 0.85
  - target: "[[分布式假说]]"
    type: implements_theory
    confidence: 0.85
  - target: "[[CBOW]]"
    type: includes
    confidence: 0.9
  - target: "[[Skip-gram 模型]]"
    type: includes
    confidence: 0.9
  - target: "[[负采样技术]]"
    type: uses
    confidence: 0.85
  - target: "[[层次 Softmax]]"
    type: uses
    confidence: 0.8
  - target: "[[GloVe]]"
    type: predecessor_to
    confidence: 0.8
  - target: "[[FastText]]"
    type: predecessor_to
    confidence: 0.8
supersedes: null
---

# Word2Vec

## 概述
Word2Vec 是由 [[Google]] 在 2013 年提出的神经网络模型，用于高效地将词汇映射到稠密向量空间中，使语言中的语义关系可以通过几何关系来捕获，是现代 NLP 的[[词向量]]基础。

## 关键内容

1. **核心贡献**：
   - 提出了两种训练模型：CBOW（连续词袋）和 [[Skip-gram]]（[[Skip-gram|跳字模型]]）
   - 解决了传统 [[One-Hot 编码]]的维度灾难和语义盲区问题
   - 证明了语言中的语义关系可以被几何关系捕获（如"国王 - 男人 + 女人 ≈ 女王"）

2. **两种模型架构**：
   - CBOW（[[CBOW|Continuous Bag of Words]]）：用周围词预测中心词
   - [[Skip-gram]]（[[Skip-gram|跳字模型]]）：用中心词预测周围词（更常用，在小数据集上效果更好）

3. **关键技术优化**：
   - [[层次 Softmax（Hierarchical Softmax）]]：将词表构建成[[大卫·哈夫曼|哈夫曼]]树，减少[[计算]]复杂度
   - [[负采样（Negative Sampling）]]：每次只随机抽取少量"负样本"，将多分类转为二分类问题，极大提升训练速度

## 来源
- [[paper_09_word2vec]] — 论文精读
- [[Google]] — 作者单位

## 相关
- [[Tomas Mikolov]] — 作者
- [[GloVe]] — 继承发展
- [[FastText]] — 继承发展
- [[BERT]] — 受其影响
- [[GPT]] — 受其影响
- [[One-Hot 编码]] — 比较对象
- [[词向量]] — 核心概念
- [[分布式假说]] — 理论基础
- [[CBOW]] — 模型组件
- [[Skip-gram]] — 模型组件
- [[负采样]] — 关键技术
- [[层次 Softmax]] — 关键技术