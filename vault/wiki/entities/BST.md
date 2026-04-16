---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, CTR预估, Transformer, 阿里巴巴, KDD]
aliases: [BST, Behavior Sequence Transformer]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 两阶段推荐架构, type: part_of}
  - {target: CTR 预估, type: implements}
  - {target: 自注意力机制, type: uses}
  - {target: 淘宝, type: part_of}
supersedes: null
---

# BST

## 概述
Behavior Sequence [[Transformer架构|Transformer]]，阿里巴巴于 KDD 2019 发表的工业级 [[CTR 预估]]模型，直接将 [[SASRec]] 的 [[Transformer架构|Transformer]] 架构应用于淘宝[[CTR 预估|点击率预估]]系统，为数亿用户提供服务。

## 关键内容

1. **论文信息**：标题 "Behavior Sequence [[Transformer架构|Transformer]] for E-commerce Recommendation in Alibaba"，阿里巴巴团队发表于 KDD 2019。

2. **核心方法**：受 [[SASRec]] 启发，将用户行为序列通过 [[Transformer架构|Transformer]] Encoder 进行编码，生成的序列表示与用户画像、物品特征等拼接后输入 [[CTR 预估]]模型。与 [[SASRec]] 的纯序列预测不同，BST 是多特征融合的工业级推荐模型。

3. **工业应用**：直接部署于淘宝推荐系统，服务数亿用户。证明了 [[Transformer架构|Transformer]] 架构在大规模工业推荐场景中的可行性和有效性。

4. **与 [[SASRec]] 的关系**：BST 将 [[SASRec]] 的[[Self-Attention机制|自注意力]]序列编码思想迁移到 [[CTR 预估]]场景，是 [[SASRec]] 工业影响力的最直接体现。两者架构相似，但 BST 增加了丰富的特征工程和工业级优化。

## 来源
- [BST 原始论文 (KDD 2019)](https://arxiv.org/abs/1905.06874)

## 相关
- [[SASRec]] — BST 的架构灵感来源
- [[CTR 预估]] — BST 解决的核心任务
- [[两阶段推荐架构]] — BST 在工业推荐系统中的位置
- [[自注意力机制]] — BST 的核心计算机制
- 阿里巴巴 — BST 的研发机构
