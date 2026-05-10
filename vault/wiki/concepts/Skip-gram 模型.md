---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [NLP, 词向量, 模型架构]
aliases: ["Skip-gram", "跳字模型"]
relates_to:
  - target: "[[Word2Vec]]"
    type: component_of
    confidence: 0.9
  - target: "[[CBOW]]"
    type: alternative_to
    confidence: 0.85
supersedes: null
---

# Skip-gram

## 概述
[[Skip-gram]] 是 [[Word2Vec]] 提出的两种[[词向量]]训练模型之一，特点是使用中心词预测周围词，通常在实践中比 CBOW 效果更好。

## 关键内容

1. **工作原理**：
   - 输入：中心词的向量表示
   - 输出：预测的上下文词
   - 用单个中心词来预测其窗口范围内的多个上下文词

2. **模型特点**：
   - 在小数据集上效果更好
   - 对罕见词的处理能力更强
   - 产生的[[词向量]]质量通常高于 CBOW

3. **与 CBOW 对比**：
   - [[Skip-gram]] 用中心词预测上下文词
   - CBOW 用上下文词预测中心词
   - [[Skip-gram]] 训练相对较慢，但对低频词表现更好

## 来源
- [[paper_09_word2vec]] — Word2Vec 论文介绍

## 相关
- [[Word2Vec]] — 所属模型
- [[CBOW]] — 对比模型
- [[词向量]] — 目标技术
- [[NLP]] — 应用领域