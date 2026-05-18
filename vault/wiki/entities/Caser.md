---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, CNN, WWW]
aliases: [Caser, Convolutional Sequence Embedding Recommendation]
relates_to:
  - {target: 序列推荐, type: implements}
  - {target: GRU4Rec, type: compares_to}
  - {target: SASRec, type: supersedes}
  - {target: FPMC, type: compares_to}
supersedes: null
---

# Caser

## 概述
Tang 与 Wang 于 WWW 2018 提出的 CNN [[序列推荐]]方法，用水平和垂直卷积捕获序列模式，但[[感受野]]受限，后被 [[SASRec]] 以显著效率优势超越。

## 关键内容

1. **论文信息**：标题 "Personalized Top-N [[序列推荐|Sequential Recommendation]] via Convolutional Sequence [[Embedding]]"，作者 Jiaxi Tang 与 Ke Wang，发表于 WWW 2018（[[KDD|KDD 2018]] 也有相关版本）。

2. **核心方法**：将用户历史交互序列视为二维图像（用户嵌入 × 序列位置），通过水平卷积（捕获序列模式）和垂直卷积（捕获点级特征）进行特征提取。CNN 支持并行[[计算]]，但[[感受野]]受限于卷积核大小，捕获长程依赖需要堆叠多层。

3. **与 [[SASRec]] 的对比**：[[SASRec]] 在训练速度上比 Caser 快约 11 倍（[[MovieLens]]-1M 上 ~350 秒 vs ~3,850 秒），且在所有指标上均优于 Caser。[[Self-Attention机制|Self-Attention]] 的任意位置直接连接（O(1) 最短路径）相比 CNN 的局部[[感受野]]在[[序列推荐]]中具有明显优势。

4. **局限性**：卷积操作的局部相关性先验假设并不完全适用于用户行为序列；长程依赖需要深层堆叠；[[感受野]]受限于卷积核大小。

## 来源
- [Caser 原始论文 (WWW 2018)](https://dl.acm.org/doi/10.1145/3159652.3159656)

## 相关
- [[SASRec]] — 在效果和效率上全面超越 Caser
- [[GRU4Rec]] — Caser 对比的 RNN 基线
- FPMC — Caser 对比的 MC 基线
- [[序列推荐]] — Caser 解决的核心场景
