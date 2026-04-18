---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags:
- 机器学习
- 深度学习
- NLP
- 词嵌入
- 训练优化
aliases:
- Negative Sampling
- 负采样
- 负采样方法
relates_to:
- target: "[[Word2Vec]]"
  type: implements
  confidence: 0.99
  note: Word2Vec 的核心训练优化方法
- target: "[[Skip-gram]]"
  type: implements
  confidence: 0.95
  note: Skip-gram 的训练优化
- target: "[[Efficient Estimation of Word Representations in Vector Space (2013 论文)]]"
  type: caused_by
  confidence: 0.99
  note: 论文提出
supersedes: null
---

# 负采样（Negative Sampling）

## 概述

[[负采样]]是 [[Word2Vec]] 的核心训练优化方法，用 K 个随机负样本替代全量 Softmax，使训练速度提升 1000 倍以上。

## 关键内容

### 问题背景

原始 Softmax 的计算复杂度：
```
P(上下文词 w_o | 中心词 w_c) = exp(v'ᵀ v) / Σ_{w=1}^{V} exp(v'_w ᵀ v)
                                                  ↑
                                         对所有 V≈10万个词求和
                                         → 每步更新 10 万个参数！
```

### 负采样方案

每次只更新正样本 + K 个随机负样本（K=5~20）：

```
目标函数（代替 Softmax）：
  log σ(v'ᵀ_wo · v_c) + Σₖ₌₁ᴷ E_{wₖ~Pₙ}[log σ(-v'ᵀ_wₖ · v_c)]

正样本 (北京, 天安门)：输出接近 1
负样本 (北京, 随机词₁) ... K 个：输出接近 0

每步只更新 K+1 个词向量！速度提升 1000 倍以上
```

### 采样策略

按词频的 3/4 次方采样：`P(w) ∝ freq(w)^(3/4)`

这个"魔法数字"的作用：
- 高频词采样概率适度降低
- 低频词采样概率适度提升
- 平衡了词频分布的不均匀性

### 实现要点

在 PyTorch 中：
```python
# 负采样概率计算
def get_negative_sample_probs(self):
    freqs = np.array([self.word_freq[self.idx2word[i]] for i in range(len(self))])
    probs = freqs ** 0.75  # 3/4 次方
    return probs / probs.sum()

# 负样本选择
negatives = np.random.choice(len(self.vocab), self.n_neg, p=self.neg_probs, replace=False)
```

### 历史意义

[[负采样]]是 [[Word2Vec]] 能够实现高效训练的关键创新之一，使得在亿级语料上训练[[词嵌入（Word Embedding）|词向量]]成为可能，直接推动了 NLP 预训练[[规范化理论|范式]]的兴起。

## 来源

- [[raw/articles/ai-papers/machine-learning/08_word2vec_2013.md]]

## 相关

- [[Word2Vec]] — 所属模型
- [[Skip-gram]] — 应用的架构
- [[Efficient Estimation of Word Representations in Vector Space (2013 论文)]] — 提出论文
