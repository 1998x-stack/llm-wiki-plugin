---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, CTR预估, Transformer, 阿里巴巴, KDD]
aliases: [BST, Behavior Sequence Transformer, Behavior Sequence Transformer for E-commerce Recommendation in Alibaba]
relates_to:
  - {target: SASRec, type: influenced_by}
  - {target: 两阶段推荐架构, type: part_of}
  - {target: CTR 预估, type: implements}
  - {target: 自注意力机制, type: uses}
  - {target: 淘宝, type: deployed_at}
  - {target: Transformer架构, type: uses}
  - {target: 序列推荐, type: extends}
  - {target: 阿里巴巴, type: developed_by}
supersedes: null
---

# BST

## 概述
Behavior Sequence [[Transformer架构|Transformer]]，阿里巴巴于 KDD 2019 发表的工业级 [[CTR 预估]]模型，直接将 [[SASRec]] 的 [[Transformer架构|Transformer]] 架构应用于[[淘宝]][[CTR 预估|点击率预估]]系统，为数亿用户提供[[服务]]。

## 关键内容

1. **论文信息**：标题 "Behavior Sequence [[Transformer架构|Transformer]] for E-commerce Recommendation in Alibaba"，阿里巴巴团队发表于 KDD 2019。BST证明了[[SASRec]]开创的[[Transformer架构]]不仅在[[序列推荐]]任务中有效，在CTR预估等其他推荐场景中同样具有强大潜力。

2. **开发背景**：阿里巴巴团队受[[SASRec]]成功的启发，将[[Self-Attention机制]]应用于[[淘宝]]的[[CTR 预估|点击率预估]]系统。BST是[[SASRec]]在工业界应用的直接延伸。

3. **核心创新**：
   - **行为序列建模**：将用户的历史行为序列（如浏览、点击、购买）作为输入，使用[[Self-Attention机制]]建模用户兴趣的动态变化
   - **多场特征融合**：不仅处理行为序列，还融合了用户画像、广告特征等多种特征场
   - **工业级优化**：针对大规模线上系统的性能要求，进行了[[计算]]效率优化

4. **核心方法**：受 [[SASRec]] 启发，将用户行为序列通过 [[Transformer架构|Transformer]] Encoder 进行编码，生成的序列表示与用户画像、物品特征等拼接后输入 [[CTR 预估]]模型。与 [[SASRec]] 的纯序列预测不同，BST 是多特征融合的工业级推荐模型。

5. **架构特点**：
   - **借鉴[[SASRec]]**：采用与[[SASRec]]类似的[[Self-Attention机制]]建模用户行为序列
   - **特征嵌入**：将用户行为、商品特征、上下文特征等统一映射到向量空间
   - **[[注意力机制]]**：[[计算]]当前广告与历史行为的相关性，动态聚合用户兴趣表示
   - **工业部署**：针对大规模在线[[服务]]进行了专门优化

6. **工业应用**：
   - **阿里巴巴部署**：BST在阿里巴巴的多个业务场景中得到应用
   - **[[淘宝]]实践**：直接部署于[[淘宝]]推荐系统，[[服务]]数亿用户
   - **效果验证**：在线A/B测试验证了显著的效果提升

7. **工业应用**（原文）：直接部署于[[淘宝]]推荐系统，[[服务]]数亿用户。证明了 [[Transformer架构|Transformer]] 架构在大规模工业推荐场景中的可行性和有效性。

8. **学术意义**：BST证明了[[SASRec]]提出的方法论在工业界的实际价值，为学术界和工业界的结合提供了典型范例。展示了[[Transformer架构]]从[[序列推荐]]到[[CTR 预估|点击率预估]]的可扩展性。

9. **与 [[SASRec]] 的关系**：BST 将 [[SASRec]] 的[[Self-Attention机制|自注意力]]序列编码思想迁移到 [[CTR 预估]]场景，是 [[SASRec]] 工业影响力的最直接体现。两者架构相似，但 BST 增加了丰富的[[特征工程（Feature Engineering）|特征工程]]和工业级优化。BST直接受[[SASRec]]启发，将[[SASRec]]在[[序列推荐]]中的成功迁移到[[CTR 预估|点击率预估]]场景，证明了[[Transformer架构]]在推荐系统中的普适性。

## 来源
- [BST 原始论文 (KDD 2019)](https://arxiv.org/abs/1905.06874)
- 阿里巴巴技术分享

## 相关
- [[SASRec]] — BST 的架构灵感来源
- [[CTR 预估]] — BST 解决的核心任务
- [[两阶段推荐架构]] — BST 在工业推荐系统中的位置
- [[自注意力机制]] — BST 的核心计算机制
- 阿里巴巴 — BST 的研发机构
- [[Transformer架构]] — BST 采用的核心架构
- [[序列推荐]] — BST 扩展的应用场景
- [[淘宝]] — BST 的部署平台
