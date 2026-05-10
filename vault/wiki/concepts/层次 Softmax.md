---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [NLP, 优化技术, 机器学习]
aliases: ["Hierarchical Softmax", "层次 Softmax"]
relates_to:
  - target: "[[Word2Vec]]"
    type: used_by
    confidence: 0.8
  - target: "[[Skip-gram 模型]]"
    type: used_by
    confidence: 0.75
  - target: "[[CBOW]]"
    type: used_by
    confidence: 0.75
  - target: "[[负采样技术]]"
    type: alternative_to
    confidence: 0.75
supersedes: null
---

# 层次 Softmax

## 概述
[[层次 Softmax（Hierarchical Softmax）]]是 [[Word2Vec]] 中的另一项关键技术优化，通过构建[[大卫·哈夫曼|哈夫曼]]树来降低[[计算]]复杂度，提高训练效率。

## 关键内容

1. **解决问题**：
   - 传统的 [[Softmax]] 需要[[计算]]整个词表的概率分母，[[计算]]复杂度为 O(V)
   - 层次 [[Softmax]] 通过[[大卫·哈夫曼|哈夫曼]]树将复杂度降至 O(log V)

2. **工作原理**：
   - 将词表构建成一棵[[大卫·哈夫曼|哈夫曼]]树
   - 预测时只需从根节点走到对应的叶节点
   - 每次预测只需要约 log₂(V) 次[[计算]]，而不是 V 次

3. **优化效果**：
   - 大幅降低[[计算]]复杂度
   - 特别适用于大词表的情况
   - 在某些场景下被[[负采样技术]]替代

## 来源
- [[paper_09_word2vec]] — Word2Vec 论文介绍

## 相关
- [[Word2Vec]] — 所属技术
- [[Skip-gram 模型]] — 应用模型
- [[CBOW]] — 应用模型
- [[负采样技术]] — 对比技术
- [[NLP]] — 应用领域
- [[哈夫曼树]] — 依赖数据结构