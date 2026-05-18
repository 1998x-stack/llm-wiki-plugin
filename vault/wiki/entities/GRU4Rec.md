---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 序列推荐, 会话推荐, RNN, GRU, ICLR]
aliases: [GRU4Rec, Session-based Recommendations with Recurrent Neural Networks]
relates_to:
  - {target: Balazs Hidasi, type: part_of}
  - {target: 会话推荐, type: implements}
  - {target: 序列推荐, type: part_of}
  - {target: BPR 论文, type: uses}
  - {target: 矩阵分解, type: compares_to}
  - {target: 基于物品的协同过滤, type: compares_to}
  - {target: SASRec, type: supersedes}
  - {target: BERT4Rec, type: supersedes}
  - {target: NARM, type: extends}
  - {target: HRNN, type: extends}
  - {target: STAMP, type: supersedes}
  - {target: SR-GNN, type: supersedes}
  - {target: TOP1 Loss, type: uses}
  - {target: Session-Parallel Mini-Batch, type: uses}
  - {target: Recall@K, type: uses}
  - {target: MRR, type: uses}
supersedes: null
---

# GRU4Rec

## 概述
[[Balazs Hidasi]] 等人于 [[ICLR 2016]] 发表的开创性论文，首次将 GRU 引入[[会话推荐]]场景，通过 [[Session-Parallel Mini-Batch]] 训练策略和排序损失函数，开创了深度学习在[[序列推荐]]领域的先河。

## 关键内容

1. **论文信息**：标题 "[[会话推荐|Session-based Recommendations]] with [[循环神经网络（RNN）|Recurrent Neural Network]]s"，作者 [[Balazs Hidasi]], Alexandros Karatzoglou, Linas Baltrunas, Donat Tikk，机构 [[Gravity R&D]]（匈牙利）/ [[Telefonica Research]]（西班牙），发表于 [[ICLR 2016]]，首次公开 2015年11月（arXiv: 1511.06939），累计引用超过 4000 次（截至2025年）。

2. **核心问题**：给定匿名用户在当前会话中的点击序列 $[x_1, x_2, ..., x_t]$，预测下一次最可能点击的物品 $x_{t+1}$。不使用任何跨会话的用户信息，不依赖显式用户画像，本质上是一个序列到一的预测问题。

3. **架构设计**：输入层（1-of-N 编码）→ GRU 层（单层，100 隐藏单元）→ 输出层（全连接 + 排序损失）。实验发现 GRU > LSTM > 标准 RNN，单层即可取得最佳效果。

4. **[[Session-Parallel Mini-Batch]] 训练策略**：将多个会话并排放置，每步取各会话的当前事件作为输入、下一事件作为目标；会话结束时替换为新会话并重置对应隐藏状态。充分利用 GPU 并行能力，mini-batch 内其他会话的目标物品天然作为负样本。

5. **排序损失函数**：提出 [[BPR Loss]] 和 [[TOP1 Loss]] 两种 pairwise 排序损失，显著优于[[交叉熵]]（[[交叉熵]]在100次随机实验中仅10次收敛）。TOP1 内置正则化项使其在更大隐藏层尺寸下表现更稳定。

6. **实验结果**：在 RSC15（YOOCHOOSE）数据集上，[[候选生成|Recall]]@20 达 0.5196，MRR@20 达 0.2164，相比 [[基于物品的协同过滤|Item-KNN]] 提升约 20-30%。后续 GRU4Rec v2（CIKM 2018）提出 BPR-max 和 TOP1-max，性能再提升 35%。

7. **历史地位**：开创了基于深度学习的[[序列推荐]]研究方向，将 NLP 中的序列建模思想迁移到推荐系统。催生了 NARM（2017, [[注意力机制（Attention Mechanism）|注意力机制]]）、HRNN（2017, 层次化 RNN）、STAMP（2018, 纯[[注意力机制|注意力]]）、[[SASRec]]（2018, [[Self-Attention机制|自注意力]]）、[[BERT4Rec]]（2019, 双向 [[Transformer架构|Transformer]]）、[[SR-GNN]]（2019, 图神经网络）等一系列后续工作。

8. **局限性**：RNN 单向顺序处理无法并行化；完全丢失会话间信息；无法捕获全局物品关系；使用简单 one-hot 编码未利用物品侧信息；在某些场景下被精心设计的会话 KNN 方法超越。

9. **工业界采纳**：[[Spotify]] 和 Pinterest 等公司的推荐系统借鉴了 GRU4Rec 的思想。在 [[NVIDIA]] Merlin / [[Transformer架构|Transformer]]s4Rec 等现代框架中仍保留为标准基线模型。

## 来源
- [原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)
- [官方 PDF (ICLR 2016)](https://hidasi.eu/assets/pdf/gru4rec_iclr16.pdf)
- [官方代码 (Theano)](https://github.com/hidasib/GRU4Rec)
- [PyTorch 官方实现](https://github.com/hidasib/GRU4Rec_PyTorch_Official)
- [GRU4Rec v2 (CIKM 2018)](https://hidasi.eu/assets/pdf/gru4rec_v2_cikm18.pdf)

## 相关
- [[Balazs Hidasi]] — 第一作者
- [[会话推荐]] — GRU4Rec 解决的核心场景
- [[序列推荐]] — GRU4Rec 开创的研究方向
- [[BPR 论文]] — 损失函数来源
- [[TOP1 Loss]] — GRU4Rec 提出的排序损失
- [[Session-Parallel Mini-Batch]] — GRU4Rec 的训练策略
- [[矩阵分解]] — GRU4Rec 对比的基线方法
- [[基于物品的协同过滤]] — GRU4Rec 对比的基线方法
- NARM — 在 GRU4Rec 基础上加入注意力机制
- HRNN — 层次化 RNN，跨会话建模
- [[STAMP]] — 纯注意力机制，不使用 RNN
- [[SASRec]] — 自注意力 Transformer 架构，超越 GRU4Rec
- [[BERT4Rec]] — 双向 Transformer，超越 GRU4Rec
- [[SR-GNN]] — 图神经网络方法，超越 GRU4Rec
- [[Recall@K]] — 主要评估指标
- MRR — 主要评估指标
- [[Spotify]] — 工业界采纳者
