---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["注意力机制", "NLP", "机器翻译", "深度学习"]
aliases: ["Neural Machine Translation by Jointly Learning to Align and Translate", "Bahdanau et al. 2015", "NMT by Jointly Learning to Align and Translate"]
relates_to:
  - target: "[[Yoshua Bengio]]"
    type: uses
    confidence: 0.95
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: caused
    confidence: 0.95
  - target: "[[Bahdanau注意力]]"
    type: caused
    confidence: 0.95
  - target: "[[编码器-解码器架构（Seq2Seq）]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Neural Machine Translation by Jointly Learning to Align and Translate (2015 论文)

## 概述

Bahdanau、Cho、Bengio 在 ICLR 2015 发表的论文，首次提出[[注意力机制（Attention Mechanism）|注意力机制]]解决 seq2seq 固定长度瓶颈，使机器翻译具备可解释的对齐[[矩阵]]，是 [[Transformer 架构|Transformer]] 和现代 LLM 的直接前身。

## 关键内容

### 核心贡献

1. **[[注意力机制（Attention Mechanism）|注意力机制]]的提出**：翻译每个目标词时，动态对源句子所有位置加权求和，生成该时刻专属的上下文向量 $c_t$，彻底解决固定长度瓶颈
2. **对齐函数设计**：$e_{it} = v^\top \tanh(W_a s_{t-1} + U_a h_i)$，通过小型前馈网络学习源位置与当前解码的相关性
3. **可解释性突破**：[[注意力机制|注意力]]权重 $\alpha$ 构成对齐[[矩阵]]，使机器翻译首次可视化，英法翻译呈现对角线模式
4. **实验验证**：在英法翻译任务上 BLEU 分数显著提升，且长句翻译质量不再随长度急剧下降

### 实验结果

- 在 WMT'14 英法翻译任务上达到 28.4 BLEU（当时最优）
- 长句翻译 BLEU 不再随源句长度下降，验证了[[注意力机制（Attention Mechanism）|注意力机制]]的有效性
- 对齐[[矩阵]]可视化证明模型学会了语言学上合理的词对词对齐

### 历史影响

该论文是[[注意力机制（Attention Mechanism）|注意力机制]]的**开山之作**，直接启发了 Luong (2015) 的[[Luong注意力|点积注意力]]、Vaswani (2017) 的 [[Self-Attention机制|Self-Attention]] 和 [[Transformer 架构]]。现代所有 LLM（GPT、[[Claude_Code|Claude]] 等）的核心机制均可追溯至此。

## 来源

- [[raw/articles/ai-papers/machine-learning/12_attention_2015.md]] — 完整论文解读与代码实现

## 相关

- [[Yoshua Bengio]] — author（论文第三作者，深度学习先驱）
- [[注意力机制（Attention Mechanism）]] — caused（本论文首次提出注意力机制）
- [[Bahdanau注意力]] — caused（本论文提出的加性注意力具体实现）
- [[编码器-解码器架构（Seq2Seq）]] — extends（在 Cho 等人 seq2seq 基础上引入注意力）
