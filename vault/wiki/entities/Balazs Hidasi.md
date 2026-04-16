---
type: entity
entity_type: person
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 序列推荐, RNN, 研究者]
aliases: [Balazs Hidasi, Balázs Hidasi]
relates_to:
  - {target: GRU4Rec, type: implements}
  - {target: Alexandros Karatzoglou, type: part_of}
supersedes: null
---

# Balazs Hidasi

## 概述
匈牙利研究者，Gravity R&D 团队成员，[[GRU4Rec]] 论文第一作者，首次将门控循环单元（[[生成式推荐|GR]]U）引入[[会话推荐]]场景，开创了深度学习在[[序列推荐]]领域的先河。

## 关键内容

1. **代表工作**：[[GRU4Rec]] — "[[GRU4Rec|Session-based Recommendations with Recurrent Neural Networks]]"（ICLR 2016），第一作者。该论文累计被引用超过 4000 次（截至2025年），是推荐系统领域引用量最高的论文之一。

2. **核心贡献**：
   - 首次将深度 RNN（[[生成式推荐|GR]]U）应用于[[会话推荐]]场景
   - 提出 [[Session-Parallel Mini-Batch]] 训练策略，解决 RNN 处理长短不一序列的效率问题
   - 提出 [[TOP1 Loss]]，将排序洞察转化为可操作的训练目标
   - 证明了在[[会话推荐]]场景下 [[生成式推荐|GR]]U > LSTM > 标准 RNN 的实证结论

3. **后续工作**：[[GRU4Rec]] v2（CIKM 2018），与团队成员共同提出 [[BPR]]-max 和 [[TOP1 Loss|TOP1]]-max 损失函数，将性能提升 35%。

4. **开源贡献**：维护 [[GRU4Rec]] 的官方代码仓库（Theano 实现和 PyTorch 官方实现），为后续研究者提供了可复现的基线。

5. **机构背景**：Gravity R&D（匈牙利），与 Telefonica Research（西班牙）合作完成 [[GRU4Rec]] 研究。

## 来源
- [GRU4Rec 原始论文 (arXiv)](https://arxiv.org/abs/1511.06939)
- [GRU4Rec 官方代码](https://github.com/hidasib/GRU4Rec)

## 相关
- [[GRU4Rec]] — 第一作者的开创性工作
- [[Alexandros Karatzoglou]] — 合作作者
