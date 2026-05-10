---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 训练技术, Softmax, 负采样]
aliases: [Sampled Softmax, 采样softmax, Negative Sampling Softmax]
relates_to:
  - {target: Deep Neural Networks for YouTube Recommendations, type: implements}
  - {target: 负采样, type: uses}
  - {target: Embedding, type: implements}
  - {target: 对比学习, type: compares_to}
  - {target: InfoNCE, type: compares_to}
supersedes: null
---

# 采样 Softmax

## 概述
超大规模多分类训练技术：每次只采样数千个负样本来近似完整 softmax，将[[计算]]开销从语料库大小降低到可接受范围。

## 关键内容

1. **问题背景**：在推荐系统的极端多分类建模中，类别数等于视频语料库大小（数百万到数十亿级别）。完整 softmax 需要[[计算]]所有类别的指数和，[[计算]]复杂度为 O(V)，在超大规模场景下完全不可行。

2. **核心思想**：每次训练时只采样数千个负样本（negative samples），加上真实正样本，在这个缩小后的集合上[[计算]] softmax。这样[[计算]]复杂度从 O(V) 降低到 O(k)，其中 k 是采样数量（通常数千）。

3. **在 [[Deep Neural Networks for YouTube Recommendations|YouTube DNN]] 中的应用**：[[Deep Neural Networks for YouTube Recommendations]] 的[[候选生成]]模型将推荐建模为超大规模多分类问题，使用采样 [[Softmax]] 技术大幅降低训练开销。公式 P(w_t = i | U, C) = e^{v_i · u} / Σ_{j ∈ V} e^{v_j · u} 中的分母通过采样近似。

4. **与[[负采样]]的关系**：采样 [[Softmax]] 本质上是一种结构化的 [[负采样]] 策略。它不仅随机采样负样本，还会根据频率等因素调整采样分布，确保训练的稳定性和效率。

5. **[[Embedding]] 学习的副产品**：论文发现"softmax 输出层的权重就是每个视频的良好表示（embeddings）"。这意味着训练分类器的过程同时也是学习高质量 embedding 的过程。这种"分类即表示学习"的思想后来在 [[对比学习]]（如 [[InfoNCE]]）等领域得到了更加系统的发展。

6. **现代替代方案**：随着 [[对比学习]] 的发展，[[InfoNCE]] 等损失函数在某些场景下替代了采样 [[Softmax]]，但核心思想——通过负样本来近似全量[[计算]]——一脉相承。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Deep Neural Networks for YouTube Recommendations]] — 应用该技术的论文
- [[负采样]] — 采样 Softmax 的核心机制
- [[Embedding]] — 采样 Softmax 训练的副产品
- [[对比学习]] — 采样 Softmax 的思想延伸
- [[InfoNCE]] — 对比学习中类似的负采样机制
- [[CTR 预估]] — 另一种需要处理大规模分类的推荐任务
