---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [nlp, architecture, attention, google, deep-learning, 机器学习]
aliases: ["Transformer Architecture", "Transformer Model"]
relates_to:
  - target: "[[Attention Is All You Need]]"
    type: introduced_by
    confidence: 0.9
  - target: "[[Self-Attention]]"
    type: core_component
    confidence: 0.9
  - target: "[[Multi-Head Attention]]"
    type: core_component
    confidence: 0.9
  - target: "[[Positional Encoding]]"
    type: core_component
    confidence: 0.9
  - target: "[[Feed Forward Network]]"
    type: core_component
    confidence: 0.8
  - target: "[[BERT]]"
    type: parent_architecture
    confidence: 0.9
  - target: "[[GPT]]"
    type: parent_architecture
    confidence: 0.9
  - target: "[[Vision Transformer]]"
    type: extended_to
    confidence: 0.9
  - target: "[[RNN]]"
    type: alternative_to
    confidence: 0.8
supersedes: null
---

# Transformer

## 概述
一种完全基于[[注意力机制（Attention Mechanism）|注意力机制]]的深度学习架构，由[[Google Brain]]团队在2017年的论文《[[Transformer 论文|Attention Is All You Need]]》中首次提出。该架构抛弃了传统的循环和卷积结构，实现了完全并行化的序列处理。

## 关键内容

### 核心组件
1. **[[自注意力机制]]**：使模型能够关注输入序列中的任意位置，捕获长距离依赖关系
2. **[[多头注意力]]**：允许模型从不同的表示子空间同时关注不同类型的信息
3. **[[位置编码]]**：为模型提供序列位置信息，因为[[注意力机制（Attention Mechanism）|注意力机制]]本身是位置无关的
4. **前馈网络**：独立地对每个位置应用相同的线性变换
5. **[[残差连接]]与[[Layer Normalization|层归一化]]**：提升深层网络的训练稳定性

### 架构设计
Transformer包含编码器（Encoder）和解码器（Decoder）两个部分，每个部分都由多个相同的层堆叠而成。编码器由6个相同的层组成，每层有两个子层：[[多头注意力|多头自注意力]]机制和位置全连接前馈网络。解码器同样由6个层组成，但在两个子层之间增加了第三个子层，用于处理编码器的输出。

### 优势
- **完全并行化**：相比RNN的串行[[计算]]，Transformer可以并行处理序列中的所有位置，大大提高了训练效率
- **长距离依赖**：通过[[自注意力机制]]直接连接任意两个位置，更好地捕获长距离依赖关系
- **可解释性**：[[注意力机制|注意力]]权重提供了模型决策过程的可视化

### 影响
[[Transformer架构]]奠定了现代大[[Language-Model|语言模型]]的基础，BERT、GPT等模型均基于此架构或其变体。此外，该架构还成功扩展到了[[计算]]机视觉等领域，产生了[[Vision Transformer（ViT）|Vision Transformer]]等重要模型。

## 来源
- [[Attention Is All You Need]] — 原始论文

## 相关
- [[Attention Is All You Need]] — 提出论文
- [[Self-Attention]] — 核心技术
- [[BERT]] — 基于此架构
- [[GPT]] — 基于此架构
- [[Vision Transformer]] — 扩展应用
- [[RNN]] — 替代的技术