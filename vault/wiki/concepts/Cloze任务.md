---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [NLP, 预训练, 语言模型, 推荐系统]
aliases: [Cloze任务, Cloze Task, 完形填空任务]
relates_to:
  - {target: BERT, type: uses}
  - {target: BERT4Rec, type: uses}
  - {target: 预训练模型, type: part_of}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# Cloze任务

## 概述
完形填空任务，一种在序列中随机掩盖部分元素并预测被掩盖元素的训练方法，最早应用于NLP领域的BERT模型预训练，后扩展至推荐系统中的序列建模。

## 关键内容

1. **基本定义**：Cloze任务源于心理学中的完形填空测试，指在一段文本中遮盖某些词汇，要求模型根据上下文信息恢复被遮盖的内容。在机器学习中，Cloze任务通常指随机掩盖序列中的某些位置，训练模型基于剩余信息预测被掩盖的元素。

2. **NLP中的应用**：BERT（Bidirectional Encoder Representations from Transformers）首次将Cloze任务系统性应用于语言模型预训练。通过随机掩盖输入序列中的部分token（通常是15%），训练模型恢复原始文本，使得模型能够学习双向上下文信息。

3. **推荐系统中的应用**：在推荐系统中，特别是序列推荐领域，Cloze任务被用于建模用户行为序列。例如，BERT4Rec将用户的历史行为序列中的某些物品进行掩盖，训练模型预测被掩盖的物品，从而学习用户的长期兴趣和行为模式。

4. **技术实现**：
   - **掩盖策略**：通常随机掩盖序列中一定比例的元素（如15%）
   - **双向建模**：允许模型同时利用掩盖位置的前后上下文信息
   - **训练目标**：使用softmax交叉熵损失预测被掩盖的元素

5. **与自回归任务的区别**：Cloze任务是双向的，模型可以同时看到目标位置的前后信息；而自回归任务（如GPT系列）是单向的，模型只能看到目标位置之前的信息。

6. **在BERT4Rec中的应用**：BERT4Rec使用Cloze任务对用户行为序列进行预训练，将用户的历史交互序列视为"句子"，随机掩盖其中的部分物品，训练模型预测被掩盖的物品，从而学习用户的兴趣演化模式。

## 来源
- BERT原始论文 (Devlin et al., 2018)
- BERT4Rec原始论文 (Sun et al., 2019)

## 相关
- [[BERT]] — Cloze任务的主要应用对象
- [[BERT4Rec]] — Cloze任务在推荐系统中的应用
- [[预训练模型]] — Cloze任务的主要应用场景
- [[自注意力机制]] — Cloze任务依赖的计算机制
- [[序列推荐]] — Cloze任务在推荐系统中的应用领域