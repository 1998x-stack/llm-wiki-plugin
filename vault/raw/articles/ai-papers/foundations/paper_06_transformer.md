# 论文精读 #06：Transformer
## Attention Is All You Need
**作者：Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin | 2017 | Google Brain / Google Research**

---

## 🎯 一句话概括

> Transformer 抛弃了 RNN/CNN，完全基于**自注意力机制**构建序列模型，不仅在机器翻译上刷新记录，更成为 BERT、GPT、ViT、Stable Diffusion 等一切现代 AI 的统一基座——这是过去十年最重要的一篇 AI 论文。

---

## 🌍 时代背景：RNN 的极限

### 2017年前的 NLP 主流：RNN / LSTM

序列到序列（Seq2Seq）任务（翻译、摘要、问答）的标准做法：

```
"我 爱 中 国" → [Encoder LSTM] → 语义向量 → [Decoder LSTM] → "I love China"
```

**RNN 的三大痛点：**

| 痛点 | 描述 | 影响 |
|------|------|------|
| **串行计算** | $t$ 时刻必须等 $t-1$ 完成 | GPU 并行度极低，训练慢 |
| **长距离依赖** | 梯度随距离指数衰减 | 记不住100步前的单词 |
| **信息瓶颈** | 整个句子压缩到一个向量 | 长句翻译质量差 |

2014年 Bahdanau 的注意力机制（Attention）缓解了信息瓶颈，但 RNN 的串行本质没有改变。

### 论文的赌注

Vaswani 等人提出了一个激进的想法：

> **把 RNN 完全扔掉，只用 Attention！**

这在当时是极具争议的——"没有循环结构，模型怎么感知序列顺序？"

---

## 🏗️ Transformer 完整架构

```
输入序列                          输出序列（右移一位）
"我 爱 中 国"                    "<BOS> I love China"
     │                                    │
     ▼                                    ▼
┌─ Input Embedding ─┐            ┌─ Output Embedding ─┐
│ + Positional Enc  │            │ + Positional Enc   │
└───────────────────┘            └────────────────────┘
     │                                    │
     ▼                                    ▼
┌──────────────────────┐    ┌──────────────────────────┐
│   Encoder (×N=6)     │    │    Decoder (×N=6)         │
│                      │    │                           │
│  ┌─────────────────┐ │    │  ┌──────────────────────┐ │
│  │ Multi-Head      │ │    │  │ Masked Multi-Head    │ │
│  │ Self-Attention  │ │    │  │ Self-Attention       │ │
│  └────────┬────────┘ │    │  └──────────┬───────────┘ │
│  Add & LayerNorm     │    │  Add & LayerNorm           │
│  ┌─────────────────┐ │    │  ┌──────────────────────┐ │
│  │ Feed Forward    │ │    │  │ Cross-Attention      │◄──── Encoder输出
│  │ Network (FFN)   │ │    │  │ (Q from decoder,     │ │
│  └────────┬────────┘ │    │  │  K,V from encoder)   │ │
│  Add & LayerNorm     │    │  └──────────┬───────────┘ │
└──────────────────────┘    │  Add & LayerNorm           │
          │                 │  ┌──────────────────────┐ │
          └──────────────►  │  │ Feed Forward Network │ │
                            │  └──────────────────────┘ │
                            │  Add & LayerNorm           │
                            └──────────────────────────────┘
                                          │
                                   Linear + Softmax
                                          │
                                   输出词概率分布
```

---

## 🔑 核心组件一：自注意力机制（Self-Attention）

### 直觉理解

处理句子"The animal didn't cross the street because **it** was too tired"时，"it"指代什么？

人类通过**上下文关联**知道"it"指"animal"。自注意力让模型对序列中**每个词**都能动态关注其他任意位置的词。

### Q、K、V：查询、键、值

自注意力的三个角色来自信息检索的类比：

```
你去图书馆找书的过程：

Query (Q)  = 你的需求（"我想找量子物理的书"）
Key   (K)  = 书架标签（每本书的主题标签）
Value (V)  = 书的实际内容

注意力 = softmax(Q·K^T / √d) → 匹配度权重
输出   = 权重 × V（按相关性加权求和书的内容）
```

### 数学公式

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right) V$$

**完整计算流程（以一个词为例）：**

```
输入词向量 x_i ∈ ℝ^{d_model}
     │
     ├── × W_Q → q_i ∈ ℝ^{d_k}   (Query)
     ├── × W_K → k_i ∈ ℝ^{d_k}   (Key)  
     └── × W_V → v_i ∈ ℝ^{d_v}   (Value)

注意力分数（第 i 个词对第 j 个词的关注程度）：
     e_{ij} = q_i · k_j / √d_k

归一化（让所有词的权重和为1）：
     α_{ij} = softmax({e_{ij}})

输出（加权求和）：
     z_i = Σ_j α_{ij} · v_j
```

**为什么除以 √d_k？**

$d_k$ 越大，点积值越大，Softmax 输出越接近 one-hot（梯度消失）。除以 $\sqrt{d_k}$ 把方差稳定在合理范围。

### 矩阵形式（高效并行）

```python
import torch
import torch.nn.functional as F
import math

def scaled_dot_product_attention(Q, K, V, mask=None):
    """
    Q: (batch, heads, seq_len, d_k)
    K: (batch, heads, seq_len, d_k)
    V: (batch, heads, seq_len, d_v)
    """
    d_k = Q.size(-1)
    
    # 计算注意力分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
    # scores: (batch, heads, seq_len_q, seq_len_k)
    
    # Mask（解码器自注意力：防止看到未来）
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
    
    # Softmax 归一化
    attn_weights = F.softmax(scores, dim=-1)
    
    # 加权求和 Value
    output = torch.matmul(attn_weights, V)
    
    return output, attn_weights
```

---

## 🔑 核心组件二：多头注意力（Multi-Head Attention）

单头注意力只能关注一种关系。多头注意力允许模型**从不同子空间同时关注不同类型的关系**：

```
输入 X
 │
 ├─ Head 1: W_Q1, W_K1, W_V1 → Attention_1（关注语法关系）
 ├─ Head 2: W_Q2, W_K2, W_V2 → Attention_2（关注语义关系）
 ├─ Head 3: W_Q3, W_K3, W_V3 → Attention_3（关注指代关系）
 │  ...
 └─ Head h: W_Qh, W_Kh, W_Vh → Attention_h
 
所有头的输出拼接：Concat(head1, head2, ..., headh)
再过线性层：× W_O
输出
```

**数学表示：**

$$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h) W^O$$

$$\text{head}_i = \text{Attention}(Q W_i^Q, K W_i^K, V W_i^V)$$

论文设置：$h=8$ 个头，$d_k = d_v = d_{model}/h = 64$。

```python
import torch.nn as nn

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, num_heads=8):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        # Q, K, V 投影矩阵
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
    
    def split_heads(self, x):
        """(batch, seq, d_model) → (batch, heads, seq, d_k)"""
        B, L, _ = x.shape
        x = x.view(B, L, self.num_heads, self.d_k)
        return x.transpose(1, 2)
    
    def forward(self, Q, K, V, mask=None):
        B = Q.size(0)
        
        # 线性投影
        Q = self.split_heads(self.W_Q(Q))
        K = self.split_heads(self.W_K(K))
        V = self.split_heads(self.W_V(V))
        
        # 注意力计算
        attn_out, attn_w = scaled_dot_product_attention(Q, K, V, mask)
        
        # 合并多头 (batch, heads, seq, d_k) → (batch, seq, d_model)
        attn_out = attn_out.transpose(1, 2).contiguous()
        attn_out = attn_out.view(B, -1, self.d_model)
        
        return self.W_O(attn_out), attn_w
```

---

## 🔑 核心组件三：位置编码（Positional Encoding）

**问题**：自注意力对位置没有感知——把句子中所有词打乱顺序，输出不变！

**解决**：在词嵌入上加入位置信息：

$$PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$
$$PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d_{model}}}\right)$$

**直觉**：不同频率的正弦波编码位置，类似二进制计数：
- 低频维度：区分远距离位置
- 高频维度：区分相邻位置

```python
import numpy as np

def positional_encoding(max_len, d_model):
    """生成位置编码矩阵"""
    PE = np.zeros((max_len, d_model))
    positions = np.arange(max_len)[:, np.newaxis]   # (max_len, 1)
    dims = np.arange(0, d_model, 2)                 # 偶数维度
    
    # 不同频率的正弦/余弦
    angles = positions / (10000 ** (dims / d_model))
    PE[:, 0::2] = np.sin(angles)   # 偶数维：sin
    PE[:, 1::2] = np.cos(angles)   # 奇数维：cos
    
    return torch.FloatTensor(PE).unsqueeze(0)  # (1, max_len, d_model)
```

---

## 🔑 核心组件四：前馈网络（FFN）

每个注意力层后接一个**位置无关的两层 MLP**：

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$$

- 输入/输出维度：$d_{model} = 512$
- 内部维度：$d_{ff} = 2048$（4倍扩展）

```python
class FeedForward(nn.Module):
    def __init__(self, d_model=512, d_ff=2048, dropout=0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model)
        )
    
    def forward(self, x):
        return self.net(x)
```

**注意力 vs FFN 的分工：**
- 注意力：跨位置信息聚合（"哪些词相关？"）
- FFN：逐位置特征变换（"这个词的特征如何处理？"）

---

## 🔑 核心组件五：Add & LayerNorm

每个子层后接残差连接（ResNet 思想）+ Layer Normalization：

$$\text{output} = \text{LayerNorm}(x + \text{SubLayer}(x))$$

**为什么用 Layer Norm 而非 Batch Norm？**
- 序列长度可变，batch 维度归一化不适合
- Layer Norm 在序列的特征维度归一化，与 batch size 无关

---

## 🎭 Decoder 特有：Masked Self-Attention

解码器在生成时不能"偷看"未来的词，需要 **Causal Mask（因果掩码）**：

```
生成"I love China"时的注意力矩阵：

         I    love  China
    I  [1.0   0     0  ]   "I" 只能看自己
  love [0.3  0.7    0  ]   "love" 看 I 和自己
 China [0.2  0.3   0.5 ]   "China" 看所有

屏蔽上三角（未来位置），防止信息泄漏
```

```python
def create_causal_mask(seq_len):
    """下三角为1，上三角为0（屏蔽未来）"""
    mask = torch.tril(torch.ones(seq_len, seq_len))
    return mask.unsqueeze(0).unsqueeze(0)  # (1, 1, seq, seq)
```

---

## 📊 实验结果：机器翻译 SOTA

### WMT 2014 英德翻译

| 模型 | BLEU | 训练成本 (FLOPs) |
|------|------|----------------|
| GNMT + RL（Google） | 24.6 | 极高 |
| ConvS2S（Facebook） | 25.2 | 高 |
| **Transformer (base)** | **27.3** | 低 |
| **Transformer (big)** | **28.4** | 中 |

### WMT 2014 英法翻译

| 模型 | BLEU | 训练时间 |
|------|------|---------|
| 之前最佳 | 41.0 | 数周 |
| **Transformer (big)** | **41.8** | **8 GPU × 3.5天** |

---

## ⏱️ 并行化：Transformer 最大的工程优势

```
RNN（串行）：                    Transformer（并行）：

时刻1: x₁ → h₁                  所有词同时计算注意力！
时刻2: x₂, h₁ → h₂              ┌────────────────────┐
时刻3: x₃, h₂ → h₃              │ x₁ x₂ x₃ x₄ x₅   │
时刻4: x₄, h₃ → h₄              │  ↕  ↕  ↕  ↕  ↕   │ 
时刻5: x₅, h₄ → h₅              │ Multi-Head Attention│
                                 └────────────────────┘

GPU 利用率：~10%                  GPU 利用率：~95%
```

这让 Transformer 在 GPU/TPU 上的训练效率远超 RNN，也是扩展到更大模型的关键。

---

## 🧮 各组件参数量分析（base 版）

| 组件 | 参数量 | 说明 |
|------|-------|------|
| 词嵌入 | $V \times d_{model}$ | V=37000词表 |
| 每个编码器层 | ~3.15M | Attention + FFN |
| 6个编码器 | ~18.9M | |
| 6个解码器 | ~25.2M | 多一个Cross-Attention |
| **总计** | **~65M** | base 版本 |

---

## 💻 完整 Transformer 实现

```python
class EncoderLayer(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Self-Attention + Add & Norm
        attn_out, _ = self.self_attn(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_out))
        
        # FFN + Add & Norm
        ffn_out = self.ffn(x)
        x = self.norm2(x + self.dropout(ffn_out))
        return x


class DecoderLayer(nn.Module):
    def __init__(self, d_model=512, num_heads=8, d_ff=2048, dropout=0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, num_heads)
        self.cross_attn = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.norm3 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, enc_out, src_mask=None, tgt_mask=None):
        # Masked Self-Attention（因果）
        attn1, _ = self.self_attn(x, x, x, tgt_mask)
        x = self.norm1(x + self.dropout(attn1))
        
        # Cross-Attention（Q 来自 decoder，K/V 来自 encoder）
        attn2, _ = self.cross_attn(x, enc_out, enc_out, src_mask)
        x = self.norm2(x + self.dropout(attn2))
        
        # FFN
        x = self.norm3(x + self.dropout(self.ffn(x)))
        return x


class Transformer(nn.Module):
    def __init__(self, src_vocab, tgt_vocab, d_model=512, 
                 num_heads=8, num_layers=6, d_ff=2048, 
                 max_len=5000, dropout=0.1):
        super().__init__()
        self.src_embed = nn.Embedding(src_vocab, d_model)
        self.tgt_embed = nn.Embedding(tgt_vocab, d_model)
        self.pos_enc = positional_encoding(max_len, d_model)
        
        self.encoder = nn.ModuleList([
            EncoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        self.decoder = nn.ModuleList([
            DecoderLayer(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.output_proj = nn.Linear(d_model, tgt_vocab)
        self.dropout = nn.Dropout(dropout)
    
    def encode(self, src, src_mask):
        x = self.dropout(
            self.src_embed(src) * math.sqrt(self.src_embed.embedding_dim)
            + self.pos_enc[:, :src.size(1)].to(src.device)
        )
        for layer in self.encoder:
            x = layer(x, src_mask)
        return x
    
    def decode(self, tgt, enc_out, src_mask, tgt_mask):
        x = self.dropout(
            self.tgt_embed(tgt) * math.sqrt(self.tgt_embed.embedding_dim)
            + self.pos_enc[:, :tgt.size(1)].to(tgt.device)
        )
        for layer in self.decoder:
            x = layer(x, enc_out, src_mask, tgt_mask)
        return x
    
    def forward(self, src, tgt, src_mask=None, tgt_mask=None):
        enc_out = self.encode(src, src_mask)
        dec_out = self.decode(tgt, enc_out, src_mask, tgt_mask)
        return self.output_proj(dec_out)
```

---

## 🌊 Transformer 改变了整个 AI 世界

```
Transformer (2017)
│
├── NLP 方向
│   ├── GPT-1 (2018) → GPT-2 → GPT-3 → ChatGPT → GPT-4
│   ├── BERT (2018) → RoBERTa → ALBERT → DeBERTa
│   └── T5 / BART / XLNet / ...
│
├── 视觉方向
│   ├── ViT (2021)：图像 patch 当 token
│   ├── CLIP (2021)：图文对齐
│   ├── DALL-E / Stable Diffusion：文生图
│   └── Swin Transformer：分层视觉 Transformer
│
├── 多模态
│   ├── Flamingo / GPT-4V：视觉语言模型
│   └── Gemini / Claude：通用多模态
│
└── 科学
    ├── AlphaFold2 (2021)：蛋白质结构预测
    ├── AlphaCode：代码生成
    └── 基因组学、分子设计...
```

---

## 🎓 总结

| 维度 | 评价 |
|------|------|
| **历史地位** | ⭐⭐⭐⭐⭐ 近十年最重要的 AI 论文 |
| **核心创新** | 纯注意力架构，完全并行化 |
| **翻译 BLEU** | 28.4（英德），超越所有 RNN 模型 |
| **影响范围** | NLP/视觉/音频/科学，无处不在 |
| **引用次数** | 超过 10 万次（截至 2024） |

> **一句话总结**：Transformer 用自注意力机制替代了循环结构，证明了"序列建模不需要时间步"——这个架构创新如同发现了一种新的"神经网络语言"，此后几乎所有前沿 AI 模型都用这种语言书写。

---
*⬇️ 下一篇：BERT (2018) —— 预训练时代的新范式，NLP的 ImageNet 时刻*
