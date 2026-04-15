---
title: "Attention Is All You Need"
type: source
tags: [transformer, attention, deep-learning, nlp, architecture]
created: 2025-03-01
updated: 2025-03-01
source_count: 1
status: mature
raw_file: raw/vaswani-attention-2017.pdf
author: "Vaswani et al. (Google Brain)"
published: 2017-06-12
domain: "arxiv.org"
word_count_approx: 8000
---

# Attention Is All You Need

**Author:** Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google Brain / Google Research)
**Published:** 2017-06-12 | **Domain:** arxiv.org/abs/1706.03762
**Ingested:** 2025-03-01 | **Raw file:** `raw/vaswani-attention-2017.pdf`

---

## TL;DR

Introduces the **Transformer** — a sequence-to-sequence architecture that replaces recurrence (RNNs/LSTMs)
and convolutions entirely with multi-head self-attention. Achieves state-of-the-art on machine translation
with dramatically less training time. Widely considered the foundational paper for the modern LLM era.

## Key Claims

- Recurrence is not necessary for sequence modeling; attention alone suffices
- Self-attention connects all positions in O(1) sequential operations vs O(n) for RNNs
- Multi-head attention allows the model to attend to information from different representation subspaces
- Positional encodings can substitute for recurrence in encoding sequence order
- Achieves 28.4 BLEU on WMT 2014 English-to-German translation (new SOTA at time of publication)
- Training time: 3.5 days on 8 P100 GPUs (faster than prior SOTA architectures)

## Evidence & Data

| Task | Metric | Score | Prior SOTA |
|------|--------|-------|------------|
| WMT EN→DE | BLEU | 28.4 | 26.0 (ConvS2S) |
| WMT EN→FR | BLEU | 41.0 | 40.5 (ConvS2S) |
| English constituency parsing | F1 | 91.3 | 91.7 (semi-supervised) |

## Methodology

Encoder-decoder architecture. Encoder: 6 identical layers of (multi-head attention + FFN).
Decoder: 6 identical layers of (masked multi-head attention + cross-attention + FFN).
All sublayers use residual connections + layer normalization.
Attention: `Attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) * V`

## Author's Perspective & Potential Bias

Google Brain team with strong incentive to publish influential architecture work.
Self-citations are minimal. Claims are well-supported by ablation studies in §6.

## Tensions & Contradictions

- ✓ Consistent with [[concept-attention-mechanism]]: aligns with prior additive attention work by [[entity-bahdanau]]
- ⚡ Implicitly contradicts the necessity of [[concept-recurrence]] — later empirically confirmed at scale

## Wiki Impact

- Created [[entity-transformer]] — the architecture introduced here
- Created [[concept-self-attention]] — the core mechanism
- Updated [[concept-attention-mechanism]] — added scaled dot-product variant
- Updated [[overview]] — Transformer as inflection point thesis

## Raw Excerpts

> "We propose a new simple network architecture, the Transformer, based solely on attention mechanisms,
> dispensing with recurrence and convolutions entirely." (Abstract)

> "Multi-head attention allows the model to jointly attend to information from different
> representation subspaces at different positions." (§3.2.2)

## Open Questions Raised

- ❓ Why does attention scale better than recurrence at longer sequences?
- ❓ What are the theoretical limits of positional encodings for very long contexts?
- ❓ Can the architecture extend to modalities beyond text? (answered by later work — see [[entity-vit]])
