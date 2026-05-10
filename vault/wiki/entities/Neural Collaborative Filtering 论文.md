---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 深度学习, 协同过滤]
aliases: ["Neural Collaborative Filtering", "NCF 论文", "NCF Paper", "WWW 2017 NCF"]
entity_type: paper
relates_to:
  - target: "[[Xiangnan He]]"
    type: authored
    confidence: 0.9
  - target: "[[National University of Singapore]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[WWW 2017]]"
    type: published_at
    confidence: 0.9
  - target: "[[NeuMF]]"
    type: introduces
    confidence: 0.9
  - target: "[[GMF]]"
    type: introduces
    confidence: 0.9
  - target: "[[MLP (NCF)]]"
    type: introduces
    confidence: 0.9
  - target: "[[矩阵分解]]"
    type: extends
    confidence: 0.8
supersedes: null
---

# Neural Collaborative Filtering 论文

## 概述
2017年WWW会议发表的重要论文，提出用神经网络替代矩阵分解中的内积操作，构建通用的神经协同过滤框架(NCF)，使模型能够从数据中自动学习任意复杂的用户-物品交互函数。

## 关键内容
1. **核心贡献**：提出神经协同过滤(NCF)框架，用可学习的神经网络替代固定内积，理论上能逼近任意交互函数，表达能力优于传统矩阵分解。

2. **具体方法**：
   - **GMF(广义矩阵分解)**：用加权逐元素乘积替代标准内积，允许不同潜在维度有不同重要性
   - **MLP(多层感知机)**：通过拼接用户/物品嵌入向量并经多层变换，学习复杂交叉模式
   - **NeuMF(神经矩阵分解)**：融合GMF的线性建模和MLP的非线性建模能力

3. **实验验证**：在MovieLens和Pinterest数据集上验证NeuMF的优越性，证明了非线性建模的有效性，但后续研究对其优势提出了质疑。

## 来源
- [[10-ncf.md]] — raw/books/推荐系统/10-ncf.md
- [[推荐系统]] — 推荐系统领域综述

## 相关
- [[Xiangnan He]] — 论文作者
- [[矩阵分解]] — 继承并扩展的方法
- [[NeuMF]] — 提出的关键模型
- [[GMF]] — 提出的关键模型
- [[MLP (NCF)]] — 提出的关键模型
- [[二元交叉熵]] — 采用的损失函数
- [[负采样]] — 采用的技术手段
- [[隐式反馈]] — 针对的应用场景