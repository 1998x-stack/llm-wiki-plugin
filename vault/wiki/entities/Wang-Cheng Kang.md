---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, UCSD, 研究者]
aliases: [Wang-Cheng Kang, Kang Wang-Cheng]
relates_to:
  - {target: SASRec, type: part_of}
  - {target: Julian McAuley, type: part_of}
  - {target: 序列推荐, type: part_of}
supersedes: null
---

# Wang-Cheng Kang

## 概述
推荐系统领域研究者，UCSD 博士，与 [[Julian McAuley]] 合作发表了 [[SASRec]]（ICDM 2018），首次将 [[Self-Attention机制|Self-Attention]] 引入[[序列推荐]]，开创了推荐系统的 [[Transformer架构|Transformer]] 时代。

## 关键内容

1. **代表工作**：[[SASRec]]（[[SASRec|Self-Attentive Sequential Recommendation]], ICDM 2018），与 [[Julian McAuley]] 合作。该论文累计引用 3000+ 次，是[[序列推荐]]领域引用量最高的论文之一。

2. **研究贡献**：系统性地将 [[Self-Attention机制|Self-Attention]] 应用于[[序列推荐]]任务，设计了[[因果掩码]]的单向 [[Transformer架构|Transformer]] 架构，证明了 [[Self-Attention机制|Self-Attention]] 在用户行为建模中的自适应能力——在稀疏数据上聚焦近期行为（类似[[马尔可夫链]]），在密集数据上捕获长程依赖（类似 RNN）。

3. **开源贡献**：[[SASRec]] 官方代码开源在 [[GitHub]]（https://github.com/kang205/[[SASRec]]），成为[[序列推荐]]领域最常用的基准实现之一。

4. **学术影响**：[[SASRec]] 直接催生了 [[BERT4Rec]]、[[TiSASRec]]、BST、[[S3-Rec]]、[[SSE-PT]]、[[LightSANs]]、[[DuoRec]]、[[SASRec+]] 等一系列后续工作，奠定了 [[Transformer架构|Transformer]] 在推荐系统中的基础地位。

## 来源
- [SASRec 原始论文 (ICDM 2018)](https://ieeexplore.ieee.org/document/8594844)

## 相关
- [[SASRec]] — 代表工作
- [[Julian McAuley]] — 合作导师
- [[序列推荐]] — 主要研究方向
