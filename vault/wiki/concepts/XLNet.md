---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [nlp, pre-trained models, autoregressive models]
aliases: ["XLNet", "Generalized Autoregressive Pretraining"]
relates_to:
  - target: "[[XLNet: Generalized Autoregressive Pretraining (2019 论文)]]"
    type: described_in
  - target: "[[Zhilin Yang]]"
    type: created_by
  - target: "[[CMU]]"
    type: developed_at
  - target: "[[Google Brain]]"
    type: developed_at
  - target: "[[BERT]]"
    type: compares_to
  - target: "[[Autoregressive Models]]"
    type: instance_of
  - target: "[[Permutation Language Modeling]]"
    type: implements
supersedes: null
---

# XLNet

## 概述
XLNet是一种广义[[AR 模型（自回归模型）|自回归]]预训练模型，通过排列语言建模目标改进了传统[[AR 模型（自回归模型）|自回归]]模型的局限性。

## 关键内容

1. **排列语言建模**：XLNet提出了一种新的预训练目标——排列语言建模（Permutation Language Modeling），通过随机排列输入序列的位置，使模型能够在双向上下文中学习。

2. **优势对比**：相比BERT的双向编码器，XLNet能够更好地处理序列生成任务，因为它保持了[[AR 模型（自回归模型）|自回归]]性质；相比传统的单向[[AR 模型（自回归模型）|自回归]]模型，它能够利用双向上下文信息。

3. **技术特点**：使用双流[[注意力机制（Attention Mechanism）|注意力机制]]（Two-Stream [[Self-Attention机制|Self-Attention]]）分别处理内容表示和位置表示，从而在预训练阶段实现更全面的上下文建模。

## 来源
- [[ai_papers_timeline.md]] — 2019年XLNet提出
- [[XLNet: Generalized Autoregressive Pretraining (2019 论文)]] — Zhilin Yang等CMU与Google Brain合作的研究

## 相关
- [[XLNet: Generalized Autoregressive Pretraining (2019 论文)]] — described_in
- [[Zhilin Yang]] — created_by
- [[CMU]] — developed_at
- [[Google Brain]] — developed_at
- [[BERT]] — compares_to
- [[Autoregressive Models]] — instance_of
- [[Permutation Language Modeling]] — implements