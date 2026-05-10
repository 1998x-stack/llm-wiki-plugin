---
type: paper
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [transformer, attention, nlp, google-brain, seq2seq]
aliases: ["Attention Is All You Need", "Transformer Paper", "Vaswani et al. 2017"]
relates_to:
  - target: "[[Transformer]]"
    type: introduces
    confidence: 0.9
  - target: "[[Self-Attention]]"
    type: introduces
    confidence: 0.9
  - target: "[[Multi-Head Attention]]"
    type: introduces
    confidence: 0.9
  - target: "[[Positional Encoding]]"
    type: introduces
    confidence: 0.9
  - target: "[[Feed Forward Network]]"
    type: introduces
    confidence: 0.8
  - target: "[[BERT]]"
    type: influences
    confidence: 0.9
  - target: "[[GPT]]"
    type: influences
    confidence: 0.9
  - target: "[[RNN]]"
    type: supersedes
    confidence: 0.8
supersedes: null
---

# Attention Is All You Need

## 概述
2017年Google Brain团队发表的开创性论文，提出完全基于注意力机制的Transformer架构，抛弃了传统的RNN/CNN，彻底改变了NLP和其他AI领域的发展方向。

## 关键内容

### 研究背景
在2017年之前，序列到序列（Seq2Seq）任务主要依赖RNN/LSTM模型，存在三个关键问题：
1. **串行计算**：无法充分利用GPU并行性，训练效率低下
2. **长距离依赖**：梯度随距离指数衰减，难以捕捉远距离关系
3. **信息瓶颈**：整个序列压缩为固定长度向量，信息损失严重

### 核心创新
论文提出了一种全新的架构，完全抛弃循环结构，仅依靠自注意力机制（Self-Attention）实现序列建模。这一创新解决了传统RNN的固有问题，并实现了完全并行化计算。

### Transformer架构组成
- **自注意力机制**：允许模型关注序列中的任意位置
- **多头注意力**：从不同子空间同时关注不同类型的关系
- **位置编码**：为模型提供序列位置信息
- **前馈网络**：逐位置特征变换
- **残差连接与层归一化**：提升训练稳定性

### 实验成果
论文在WMT 2014英德翻译任务中达到28.4 BLEU分数，超越所有RNN模型，同时训练时间大幅缩短。在英法翻译任务中也取得41.8 BLEU的优异成绩。

### 影响力
该论文的影响远远超出了NLP领域，成为了后续几乎所有重要AI模型的基石，包括BERT、GPT、ViT、CLIP、AlphaFold2等。

## 来源
- [[paper_06_transformer.md]] — 论文精读笔记
- [[raw/articles/ai-papers/foundations/paper_06_transformer.md]] — 原始资料

## 相关
- [[Transformer]] — introduces
- [[Self-Attention]] — introduces
- [[Multi-Head Attention]] — introduces
- [[Positional Encoding]] — introduces
- [[Feed Forward Network]] — introduces
- [[Google Brain]] — published_by
- [[Ashish Vaswani]] — authored_by
- [[诺姆·沙泽尔]] — authored_by
- [[BERT]] — influences
- [[GPT]] — influences
- [[RNN]] — supersedes