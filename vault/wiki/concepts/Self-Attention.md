---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [注意力机制, 深度学习, 序列建模, 机器学习]
aliases: ["Self Attention", "Self-Attention Mechanism"]
relates_to: []
supersedes: null
---

# Self-Attention

## 概述
一种[[注意力机制]]，允许序列中的每个位置关注序列中的所有位置，从而建立序列内部的全局依赖关系，是 [[Transformer 架构]]的核心组件。

## 关键内容

1. **工作机制**：
   - 查询（Q）、键（K）、值（V）的[[计算]]
   - [[注意力机制|注意力]]分数的[[计算]]：通过 QK^T 得到[[注意力机制|注意力]]分数[[矩阵]]
   - 使用 softmax 函数将分数转化为概率分布
   - 对值向量进行加权求和

2. **技术特点**：
   - 在序列中任意两个位置之间建立常数级别的路径长度
   - 使模型能够动态决定应该关注哪些位置的信息
   - 支持并行[[计算]]，提高了训练效率

3. **应用价值**：
   - 解决了 RNN 在处理长距离依赖时的[[梯度消失]]问题
   - 提供了捕捉长距离依赖关系的有效手段
   - 是 [[Transformer]] 模型能够高效处理序列数据的关键

## 来源
- [[Transformer]] — 核心组件
- [[20-vaswani-transformer.md]] — raw/books/计算机科学/20-vaswani-transformer.md

## 相关
- [[Transformer]] — core_component
- [[Attention Is All You Need]] — introduced_in
- [[Multi-Head Attention]] — related
- [[Scaled Dot-Product Attention]] — variant