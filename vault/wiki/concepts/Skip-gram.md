---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags:
- 机器学习
- 深度学习
- NLP
- 词嵌入
aliases:
- Skip-gram
- Skip-gram 模型
- 跳字模型
relates_to:
- target: "[[Word2Vec]]"
  type: part_of
  confidence: 0.99
  note: Word2Vec 的核心架构之一
- target: "[[CBOW（连续词袋模型）]]"
  type: compares_to
  confidence: 0.9
  note: Word2Vec 的另一种架构
- target: "[[负采样（Negative Sampling）]]"
  type: implements
  confidence: 0.95
  note: 常用训练优化方法
- target: "[[Efficient Estimation of Word Representations in Vector Space (2013 论文)]]"
  type: caused_by
  confidence: 0.99
  note: 论文提出
supersedes: null
---

# Skip-gram

## 概述

Skip-gram 是 [[Word2Vec]] 的核心架构之一，通过中心词预测[[上下文窗口]]内的词，学习稠密低维的[[词嵌入（Word Embedding）|词向量]]表示。

## 关键内容

### 工作原理

给定[[上下文窗口]]大小（如 window_size=2）：
```
句子：我 爱 [北京] 天安门
              ↑ 中心词

目标：最大化 P(我|北京) · P(爱|北京) · P(天安门|北京)
```

网络结构：
1. 中心词 → Embedding 层（300维）→ 隐向量 v
2. 隐向量 v → 输出层 + Softmax → 词表上的概率分布

### 与 CBOW 的对比

| 特性 | Skip-gram | CBOW |
|------|-----------|------|
| 预测方向 | 中心词 → 上下文 | 上下文 → 中心词 |
| 训练速度 | 较慢 | 较快 |
| 低频词效果 | 更好 | 较差 |
| 适用场景 | 生僻词、罕见词 | 通用语料 |

Skip-gram 对低频词和生僻词效果更好，是《Efficient Estimation of Word Representations in Vector Space》论文的重点推荐模型。

### 训练优化

- **动态窗口**：训练时每次随机减小窗口大小（1 到 window_size 之间），增加训练样本多样性
- **[[负采样（Negative Sampling）]]**：用 K 个随机负样本代替全量 Softmax，每步只更新 K+1 个词向量
- **高频词下采样**：减少无信息高频词的影响

### PyTorch 实现要点

```python
class Word2VecSkipGram(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int = 300):
        # 中心词嵌入矩阵（输入矩阵）
        self.center_embed = nn.Embedding(vocab_size, embed_dim, sparse=True)
        # 上下文词嵌入矩阵（输出矩阵）
        self.context_embed = nn.Embedding(vocab_size, embed_dim, sparse=True)
```

- 使用两个独立的嵌入[[矩阵]]：center_embed（中心词）和 context_embed（上下文词）
- 推荐使用 sparse=True 以配合 Sparse[[Adam（自适应矩估计）|Adam 优化器]]
- 初始化：均匀分布小范围，上下文[[矩阵]]初始化为零

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Word2Vec]] — 所属模型
- [[CBOW（连续词袋模型）]] — 对比架构
- [[负采样（Negative Sampling）]] — 训练优化方法
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 提出论文
