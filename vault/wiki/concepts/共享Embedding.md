---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 深度学习, 特征工程]
aliases: [Shared Embedding, 共享嵌入, 共享嵌入层]
relates_to: []
supersedes: null
---

# 共享Embedding

## 概述
共享[[Embedding]]是指在机器学习模型中多个组件或子网络共享同一套[[Embedding|嵌入向量]]参数的技术。这种设计常见于推荐系统中的CTR预估模型，如[[DeepFM]]，其中FM组件和DNN组件共享同一套特征[[Embedding]]。

## 关键内容

1. **技术定义**：
   - 共享[[Embedding]]是指在多任务或多组件模型中，不同子网络使用相同的[[嵌入表示|嵌入层]]参数
   - 对于每个输入特征，其[[Embedding]]向量同时[[服务]]于模型的不同部分
   - 这种设计避免了为不同组件分别学习相同特征的[[Embedding|嵌入向量]]

2. **核心优势**：
   - **参数效率**：[[嵌入表示|嵌入层]]通常占据模型参数量的绝大部分（因类别特征维度极高），共享可显著减少总参数量
   - **[[联合训练|联合优化]]**：不同组件的梯度信号可以共同优化[[Embedding]]，使嵌入同时适配多种任务需求
   - **消除预训练**：无需像FNN等模型那样需要预训练步骤，可以端到端训练

3. **在[[DeepFM]]中的应用**：
   - [[DeepFM]]的FM组件和Deep组件使用完全相同的[[Embedding]]层参数
   - 对于每个特征i，其[[Embedding]]向量Vi同时用于FM的二阶交互[[计算]]⟨Vi, Vj⟩和Deep组件的拼接输入
   - 这使得FM的二阶交互信号和DNN的高阶交互信号可以共同优化[[Embedding]]

4. **与其他技术的比较**：
   - 相比独立[[Embedding]]：减少了参数冗余，提高训练效率
   - 相比[[多任务学习]]：共享低层表示但保持高层任务特异性
   - 相比参数绑定：更灵活，允许不同组件使用相同的嵌入进行不同类型的[[计算]]

5. **应用场景**：
   - 推荐系统中的Wide&Deep、[[DeepFM]]等模型
   - 多模态学习中的特征对齐
   - 预训练模型中的参数共享策略

## 来源
- [[09-deepfm.md]] — 共享Embedding在DeepFM中的详细介绍
- [DeepFM: A Factorization-Machine based Neural Network for CTR Prediction] — 原始论文

## 相关
- [[嵌入表示]] — 共享Embedding的基础技术
- [[DeepFM]] — 共享Embedding的典型应用
- [[CTR 预估]] — 主要应用领域
- [[特征交叉]] — 通过共享Embedding实现的功能
- [[联合训练]] — 共享Embedding支持的训练方式