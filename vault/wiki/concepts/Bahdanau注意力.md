---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["深度学习", "注意力机制", "NLP", "机器翻译", "机器学习"]
aliases: ["Bahdanau Attention", "Additive Attention", "加性注意力", "Bahdanau 注意力"]
relates_to:
  - target: "[[注意力机制（Attention Mechanism）]]"
    type: implements
    confidence: 0.95
  - target: "[[Luong注意力]]"
    type: compares_to
    confidence: 0.9
  - target: "[[编码器-解码器架构（Seq2Seq）]]"
    type: extends
    confidence: 0.9
supersedes: null
---

# Bahdanau注意力

## 概述

Bahdanau 加性[[注意力机制|注意力]]通过前馈网络 $v^\top \tanh(W_a s + U_a h)$ [[计算]]对齐分数，使 Decoder 在每步动态聚焦源序列不同位置，是[[注意力机制（Attention Mechanism）|注意力机制]]的首次成功实现。

## 关键内容

### 对齐函数

核心公式：$e(s_{t-1}, h_i) = v^\top \cdot \tanh(W_a \cdot s_{t-1} + U_a \cdot h_i)$

其中 $s_{t-1}$ 为 Decoder 当前状态，$h_i$ 为 Encoder 第 $i$ 位置隐藏状态。这是一个小型前馈网络，学习"哪些源位置对当前解码最相关"。

### PyTorch 实现要点

```python
class BahdanauAttention(nn.Module):
    def __init__(self, encoder_dim, decoder_dim, attn_dim=256):
        self.Wa = nn.Linear(decoder_dim, attn_dim, bias=False)  # 解码器投影
        self.Ua = nn.Linear(encoder_dim, attn_dim, bias=False)  # 编码器投影
        self.va = nn.Linear(attn_dim, 1, bias=False)            # 分数压缩

    def forward(self, decoder_state, encoder_outputs, mask=None):
        # 对齐分数: e = vᵀ tanh(Wa·s + Ua·h)
        energy = torch.tanh(self.Wa(decoder_state).unsqueeze(1) + self.Ua(encoder_outputs))
        scores = self.va(energy).squeeze(-1)
        # 屏蔽填充 + Softmax
        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))
        attn_weights = F.softmax(scores, dim=-1)
        # 加权上下文
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context, attn_weights
```

### 与 Luong 注意力的对比

| 维度 | Bahdanau（加性） | Luong（点积） |
|------|-----------------|--------------|
| 对齐函数 | $v^\top \tanh(W_a s + U_a h)$ | $s^\top W h$ |
| 参数量 | 较多（三个[[矩阵]]） | 较少（一个[[矩阵]]或无） |
| 速度 | 较慢 | 更快 |
| 效果 | 略优 | 接近 |
| 编码器/解码器维度 | 可不同 | 必须相同 |

### 历史地位

Bahdanau [[注意力机制|注意力]]是[[注意力机制（Attention Mechanism）|注意力机制]]的**首次成功实现**，直接解决了 [[编码器-解码器架构（Seq2Seq）]] 的固定长度瓶颈。其对齐[[矩阵]]使机器翻译首次具备可解释性，为后续 [[Luong注意力]]、[[自注意力机制]] 乃至 [[Transformer架构]] 奠定了理论基础。

## 来源

- [[Neural Machine Translation by Jointly Learning to Align and Translate (2015 论文)]] — 提出 Bahdanau 加性注意力

## 相关

- [[注意力机制（Attention Mechanism）]] — implements（注意力机制的首次具体实现）
- [[Luong注意力]] — compares_to（同年提出的点积变体，更简洁快速）
- [[编码器-解码器架构（Seq2Seq）]] — extends（在 seq2seq 基础上引入动态上下文）
