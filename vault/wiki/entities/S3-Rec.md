---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, 序列推荐, 自监督学习, 预训练, CIKM]
aliases: [S3-Rec, Self-Supervised Learning for Sequential Recommendation, S3-Rec: Self-Supervised Learning for Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 对比学习, type: uses}
  - {target: 自注意力机制, type: uses}
  - {target: 预训练模型, type: implements}
  - {target: Transformer架构, type: uses}
supersedes: null
---

# S3-Rec

## 概述
S3-Rec（Self-Supervised [[序列推荐|Sequential Recommendation]]），2020 年提出的 [[SASRec]] 后续工作，引入自监督预训练增强[[序列推荐]]，通过辅助任务学习更好的物品表示。

## 关键内容

1. **论文信息**：S3-Rec（Self-Supervised Learning for [[序列推荐|Sequential Recommendation]] via Contrastive Estimation），发表于 CIKM 2020。是首个将自监督学习系统性应用于[[序列推荐]]任务的工作，基于[[SASRec]]的[[Transformer架构]]扩展。

2. **研究背景**：[[序列推荐]]面临数据稀疏性问题，直接训练深度神经网络效果不佳。借鉴NLP领域的成功经验，S3-Rec提出将自监督预训练引入[[序列推荐]]，通过在大规模历史数据上进行预训练，再对特定任务进行微调。

3. **核心创新**：
   - **六种自监督任务**：提出6种针对[[序列推荐]]的预训练任务，包括Item Recovery、Interest Category Recovery、Position Prediction、Item Attribute Prediction、Sequence Membership Identification、Interest Category Prediction
   - **统一框架**：基于[[SASRec]]的[[Transformer架构]]，将[[预训练-微调范式|预训练与微调]]有机结合
   - **领域知识融入**：将推荐领域的特定知识（如商品类别、属性等）融入预训练任务

4. **技术特点**：
   - **[[预训练-微调范式]]**：先在大规模未[[标注]]数据上进行预训练，再在目标任务上进行微调
   - **[[多任务学习]]**：同时优化多个自监督任务，提升模型的泛化能力
   - **基于[[Transformer]]**：继承[[SASRec]]的[[自注意力机制]]和序列建模能力
   - **核心创新**：在 [[SASRec]] 的基础上引入自监督预训练阶段，通过四个辅助任务（Attribute Prediction, Masked Item Prediction, Segment Prediction, Maximal Association Prediction）学习物品和序列的表示，然后在下游推荐任务上进行微调。

5. **方法**：利用序列数据本身的内在关联作为监督信号，无需额外[[标注]]数据。预训练阶段学习通用的序列表示，微调阶段针对具体推荐任务优化。通过自监督预训练，S3-Rec能够从大规模未[[标注]]的序列数据中学习有效的表示。

6. **实验验证**：在多个公开数据集上验证了预训练的有效性，特别是对于冷启动和数据稀疏场景，S3-Rec表现尤为突出。

7. **学术影响**：为推荐系统中的预训练方法奠定了基础，后续的许多工作都受到S3-Rec的启发。证明了自监督学习在推荐系统中的巨大潜力。S3-Rec以[[SASRec]]作为基础架构，在其之上增加了预训练能力，进一步提升了[[序列推荐]]的性能。

8. **效果**：在多个数据集上显著超越 [[SASRec]] 基线，证明了自监督学习在[[序列推荐]]中的有效性。

## 来源
- [S3-Rec 原始论文 (CIKM 2020)](https://dl.acm.org/doi/10.1145/3340531.3411954)
- 相关自监督推荐系统研究

## 相关
- [[SASRec]] — S3-Rec 的基础模型
- [[对比学习]] — S3-Rec 使用的学习方法
- [[序列推荐]] — S3-Rec 解决的核心场景
- [[自注意力机制]] — S3-Rec 的核心编码机制
- [[预训练模型]] — S3-Rec 的研究范式
- [[Transformer架构]] — S3-Rec 的底层架构
