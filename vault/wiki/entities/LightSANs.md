---
type: entity
entity_type: paper
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 轻量级, Self-Attention, SIGIR]
aliases: [LightSANs, Lightweight Self-Attentive Network for Sequential Recommendation]
relates_to:
  - {target: SASRec, type: extends}
  - {target: 序列推荐, type: implements}
  - {target: 自注意力机制, type: uses}
supersedes: null
---

# LightSANs

## 概述
LightSANs（Lightweight Self-Attentive Network），2021 年提出的轻量级[[Self-Attention机制|自注意力]][[序列推荐]]模型，在保持 [[SASRec]] 性能的同时显著减少参数量和计算开销。

## 关键内容

1. **论文信息**：LightSANs（Lightweight Self-Attentive Network for [[序列推荐|Sequential Recommendation]]），发表于 SIGIR 2021。

2. **核心创新**：针对 [[SASRec]] 中 $O(n^2 d)$ 的[[Self-Attention机制|自注意力]]复杂度问题，提出轻量化的[[自注意力机制]]。通过低秩近似或[[核技巧|核方法]]减少注意力计算的参数量和计算量。

3. **方法**：使用用户兴趣表示作为 Query，物品表示作为 Key/Value，将注意力计算从序列级别压缩到兴趣级别，大幅减少计算开销。

4. **效果**：在多个数据集上达到与 [[SASRec]] 相当的性能，同时参数量和推理速度显著优化，更适合资源受限的部署场景。

## 来源
- [LightSANs 原始论文 (SIGIR 2021)](https://dl.acm.org/doi/10.1145/3404835.3462943)

## 相关
- [[SASRec]] — LightSANs 的基础模型
- [[自注意力机制]] — LightSANs 轻量化的核心机制
- [[序列推荐]] — LightSANs 解决的核心场景
