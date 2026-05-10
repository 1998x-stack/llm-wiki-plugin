---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [论文, 自然语言处理, 深度学习, 变压器架构]
aliases: ["Attention Is All You Need", "Transformer Paper", "Vaswani et al. 2017"]
relates_to: []
supersedes: null
entity_type: paper
---

# Attention Is All You Need

## 概述
由 Google Brain 团队于 2017 年发表的开创性论文，提出了完全基于注意力机制的 Transformer 架构，彻底改变了序列建模领域，奠定了现代大语言模型的基础。

## 关键内容

1. **论文背景**：
   - 作者：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin
   - 发表时间：2017 年 NeurIPS 会议
   - 解决问题：RNN/LSTM 的顺序计算瓶颈和 CNN 在捕捉长距离依赖方面的局限

2. **核心创新**：
   - 完全抛弃循环和卷积结构，仅使用注意力机制
   - 提出缩放点积注意力（Scaled Dot-Product Attention）
   - 引入多头注意力（Multi-Head Attention）机制
   - 使用位置编码（Positional Encoding）保留序列信息
   - 实现高度并行化的训练过程

3. **架构特点**：
   - 编码器-解码器结构，各包含 6 层
   - 每层包含多头自注意力和前馈网络
   - 使用残差连接和层归一化
   - 模型基础维度 d_model = 512

## 来源
- [[20-vaswani-transformer.md]] — raw/books/计算机科学/20-vaswani-transformer.md
- [[Transformer]] — 论文核心成果

## 相关
- [[Transformer]] — implements
- [[RNN]] — contrasts
- [[CNN]] — contrasts
- [[Ashish Vaswani]] — authored_by
- [[Self-Attention]] — core_component