---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, 序列推荐, 深度学习, RNN]
aliases: ["Session-based Recommendations with Recurrent Neural Networks", "基于循环神经网络的会话推荐"]
relates_to:
  - target: "[[GRU4Rec]]"
    type: describes
    confidence: 0.9
  - target: "[[会话推荐]]"
    type: addresses_problem
    confidence: 0.9
  - target: "[[序列推荐]]"
    type: foundational_work
    confidence: 0.9
  - target: "[[Balazs Hidasi]]"
    type: authored_by
    confidence: 0.9
  - target: "[[ICLR 2016]]"
    type: published_at
    confidence: 0.9
  - target: "[[RNN]]"
    type: utilizes
    confidence: 0.9
  - target: "[[GRU]]"
    type: utilizes
    confidence: 0.9
supersedes: null
---

# GRU4Rec 论文

## 概述
[[GRU4Rec]]论文《[[会话推荐|Session-based Recommendations]] with [[循环神经网络（RNN）|Recurrent Neural Network]]s》是2016年ICLR会议上发表的开创性工作，首次将[[GRU|门控循环单元]](GRU)应用于基于会话的推荐场景，开启了深度学习在[[序列推荐]]领域的先河。

## 关键内容

1. **研究背景**：
   2015年推荐系统领域面临转折点，[[协同过滤]]和[[矩阵分解]]方法在有长期用户历史的场景下表现优异，但在[[会话推荐]]场景下表现不佳。大量用户以匿名身份访问，缺乏长期[[Transcripts|历史记录]]，而传统的Item-KNN、[[马尔可夫链]]等方法无法有效利用完整的会话序列信息。

2. **核心贡献**：
   - 首次将深度RNN应用于推荐系统，开创了[[序列推荐]]方向
   - 提出[[Session-Parallel Mini-Batch]]训练策略，解决RNN训练中处理长度不一序列的效率问题
   - 设计Ranking-Aware Loss（[[BPR Loss]]和[[TOP1 Loss]]），强调推荐是排序问题而非分类问题

3. **技术特点**：
   - 使用[[GRU|GRU单元]]建模会话序列，相比LSTM参数更少、训练更快
   - 采用1-of-N编码表示物品，通过隐藏状态捕获用户短期兴趣
   - 基于mini-batch的[[负采样]]策略，提高训练效率

## 来源
- [[12-gru4rec.md]] — 详细解读资料

## 相关
- [[GRU4Rec]] — describes
- [[会话推荐]] — addresses_problem
- [[序列推荐]] — foundational_work
- [[Balazs Hidasi]] — authored_by
- [[ICLR 2016]] — published_at
- [[RNN]] — utilizes
- [[GRU]] — utilizes