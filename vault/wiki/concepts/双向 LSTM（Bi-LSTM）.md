---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "序列建模"]
aliases: ["Bi-LSTM", "Bidirectional LSTM", "双向长短期记忆网络"]
relates_to:
  - target: "[[LSTM（长短期记忆网络）]]"
    type: extends
    confidence: 0.95
  - target: "[[循环神经网络（RNN）]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# 双向 LSTM（Bi-LSTM）

## 概述 (50-200字符)
LSTM 的扩展架构，同时使用正向和反向两个 LSTM 处理序列，使每个时刻的表示能同时利用过去和未来的上下文信息。2005 年提出，广泛应用于序列标注、情感分析等任务。

## 关键内容 (≥300字符, 用[[双链]])
1. **架构设计**：Bi-LSTM 包含两个独立的 [[LSTM（长短期记忆网络）]] 层——正向 LSTM 从左到右处理序列（捕捉过去上下文），反向 LSTM 从右到左处理序列（捕捉未来上下文）。两个方向的隐藏状态在每个时刻拼接或相加，形成完整的序列表示。
2. **优势**：标准 LSTM 只能利用历史信息（单向因果），而 Bi-LSTM 可以同时利用过去和未来上下文。在序列标注（NER、POS）、情感分析、机器翻译等任务中，双向上下文能显著提升模型表现。
3. **代码实现**：PyTorch 中通过 `nn.LSTM(..., bidirectional=True)` 启用。双向 LSTM 的隐藏状态维度变为 `hidden_dim * 2`，最后时刻的隐藏状态需要拼接两个方向：`torch.cat([h_n[-2], h_n[-1]], dim=1)`。
4. **演进路径**：[[循环神经网络（RNN）]] → LSTM（1997）→ Bi-LSTM（2005）→ Encoder-Decoder + Attention（2014-2015）→ [[Transformer架构]]（2017）。Bi-LSTM 在 NLP 主要任务上已被 [[Transformer 架构|Transformer]] 替代，但在时间序列、嵌入式设备等场景仍广泛使用。

## 来源
- [[Long Short-Term Memory (1997 论文)]] — LSTM 原始论文，Bi-LSTM 为其后续扩展
- [[raw/articles/ai-papers/machine-learning/04_lstm_1997.md]] — LSTM 的演进路径与 PyTorch 双向实现

## 相关
- [[LSTM（长短期记忆网络）]] — extends（双向扩展）
- [[循环神经网络（RNN）]] — extends（序列建模架构）
- [[Transformer架构]] — compares_to（后续替代方案）
- [[门控机制（Gating Mechanism）]] — uses（继承 LSTM 门控设计）
