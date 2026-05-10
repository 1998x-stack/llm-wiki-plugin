---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [NLP, 词向量, 模型架构]
aliases: ["Continuous Bag of Words", "CBOW"]
relates_to:
  - target: "[[Word2Vec]]"
    type: component_of
    confidence: 0.9
  - target: "[[Skip-gram 模型]]"
    type: alternative_to
    confidence: 0.85
supersedes: null
---

# CBOW

## 概述
CBOW（Continuous Bag of Words）是 [[Word2Vec]] 提出的两种[[词向量]]训练模型之一，特点是使用周围词预测中心词。

## 关键内容

1. **工作原理**：
   - 输入：目标词的上下文词（如在窗口内的前后词）
   - 输出：预测的目标中心词
   - 将上下文词的向量平均作为输入，通过神经网络预测中心词

2. **模型特点**：
   - [[计算]]效率相对较高
   - 在较小的数据集上表现较好
   - 对高频词的向量表示效果更佳

3. **与 [[Skip-gram]] 对比**：
   - CBOW 用上下文预测中心词
   - [[Skip-gram]] 用中心词预测上下文
   - CBOW 训练速度更快，但 [[Skip-gram]] 对罕见词的表现更好

## 来源
- [[paper_09_word2vec]] — Word2Vec 论文介绍

## 相关
- [[Word2Vec]] — 所属模型
- [[Skip-gram]] — 对比模型
- [[词向量]] — 目标技术
- [[NLP]] — 应用领域