---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, 专用模型]
aliases: [GLoSS]
relates_to:
  - {target: P5 论文, type: compares_to}
  - {target: 序列推荐, type: implements}
  - {target: SASRec, type: compares_to}
  - {target: BERT4Rec, type: compares_to}
supersedes: null
---

# GLoSS

## 概述
在[[序列推荐]]任务上超越 [[P5 论文|P5]] 的后续专用模型，在相同数据集上取得了更好的 [[候选生成|Recall]]@5 指标。

## 关键内容

1. **与 [[P5 论文|P5]] 的对比**：在[[序列推荐]]任务上，GLoSS 在 [[Amazon]] Reviews 数据集上取得了比 [[P5 论文|P5]] 更好的 [[候选生成|Recall]]@5 指标，说明在某些具体任务上，专用模型仍然可以超越统一模型。

2. **技术定位**：GLoSS 是为[[序列推荐]]任务精心设计的专用模型，而非像 [[P5 论文|P5]] 那样的统一多任务模型。这验证了 [[P5 论文]]中提到的局限性——"在某些具体任务上，它仍然无法完全匹敌为该任务精心设计的专用模型"。

3. **在推荐系统谱系中的位置**：属于[[序列推荐]]方向的专用模型，与 [[SASRec]]、[[BERT4Rec]]、[[GRU4Rec]] 等工作属于同一技术路线。

4. **对 [[P5 论文|P5]] 范式的启示**：GLoSS 的成功说明统一模型和专用模型各有优势——统一模型胜在通用性和灵活性，专用模型在特定任务上可能更优。未来的方向可能是两者的结合。

## 来源
- GLoSS 论文 — Generative Language Model for Sequential Recommendation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — GLoSS 超越的统一模型
- [[序列推荐]] — GLoSS 服务的任务
- [[SASRec]] — 序列推荐的专用模型
- [[BERT4Rec]] — 序列推荐的专用模型
- [[GRU4Rec]] — 序列推荐的专用模型
