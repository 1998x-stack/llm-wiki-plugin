# 14 · Transformer：注意力即一切
> 《Attention Is All You Need》  
> **作者**：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin（Google Brain / Google Research）　**会议**：NeurIPS　**年份**：2017

---

## 一、历史背景：RNN 的并行化困境

截至 2017 年，seq2seq + Attention（Bahdanau）已是机器翻译主流。但架构仍基于 RNN（LSTM/GRU），存在根本缺陷：

```
RNN 的串行依赖：
  h₁ → h₂ → h₃ → ... → hₙ

  hₜ 依赖 hₜ₋₁，无法并行计算！
  → 序列长度 1000：必须串行 1000 步
  → GPU 并行计算优势完全浪费

长程依赖仍然困难：
  即使有 LSTM，信息从 h₁ 到 h₅₀₀ 要经过 499 次变换
  → 信息损耗不可避免
```

Google Brain 的团队提出了一个大胆问题：

> **"如果只用注意力机制，完全去掉 RNN，会怎样？"**

答案是——更快、更好，同时可以完全并行。

---

## 二、Transformer 整体架构

```
                    输出词 (shifted right)
                         ↓
                   Output Embedding + Positional Encoding
                         ↓
              ┌──────────────────────────────┐
              │  Decoder × N（论文 N=6）      │
              │                               │
              │  ① Masked Multi-Head         │
              │     Self-Attention            │
              │     + Add & Norm             │
              │                               │
              │  ② Multi-Head                │
              │     Cross-Attention          │ ← K, V 来自 Encoder 输出
              │     + Add & Norm             │
              │                               │
              │  ③ Feed-Forward              │
              │     + Add & Norm             │
              └──────────────────────────────┘
                         ↑
                   Encoder 输出（K, V）
              ┌──────────────────────────────┐
              │  Encoder × N（论文 N=6）      │
              │                               │
              │  ① Multi-Head                │
              │     Self-Attention           │
              │     + Add & Norm             │
              │                               │
              │  ② Feed-Forward              │
              │     + Add & Norm             │
              └──────────────────────────────┘
                         ↑
              Input Embedding + Positional Encoding
                         ↑
                   输入词序列
```

---

## 三、缩放点积注意力（Scaled Dot-Product Attention）

这是 Transformer 的原子操作：

```
Attention(Q, K, V) = softmax(Q Kᵀ / √d_k) · V

Q（Query）：当前位置"想问什么"
K（Key）：其他位置"有什么"
V（Value）：其他位置实际"提供的信息"

Q Kᵀ：相关性打分矩阵，shape (N, N)
/√d_k：缩放，防止点积过大导致 Softmax 梯度消失
softmax：归一化为注意力权重
× V：加权求和，得到每个位置的输出
```

**为什么要除以 √d_k？**

```
若 Q, K 各分量独立，均值 0 方差 1，则 q·k 的方差 = d_k
d_k = 64 → 标准差 = 8，点积值分散在 [-24, +24]
→ Softmax 输出接近 one-hot，梯度消失

除以 √d_k = 8 后，标准差 = 1，梯度正常流动
```

---

## 四、多头注意力（Multi-Head Attention）

```
单头注意力：只能关注一种语义关系

多头注意力：h 个头并行，每个头学习不同的关联模式

MultiHead(Q, K, V) = Concat(head₁, ..., headₕ) · W_O

headᵢ = Attention(Q·W_Qᵢ, K·W_Kᵢ, V·W_Vᵢ)

论文设置：h=8，d_model=512，d_k=d_v=64（每头 512/8）

不同头的专长（实验观察）：
  head₁：局部位置关系
  head₂：远程句法依存
  head₃：共指消解
  ...（通过可视化注意力矩阵观察到）
```

---

## 五、位置编码（Positional Encoding）

Self-Attention 是**排列不变（Permutation Invariant）**的——序列打乱顺序，输出不变。必须显式注入位置信息：

```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))

特点：
  不同位置的编码各不相同
  相对位置差可通过线性变换推导
  泛化到训练时未见过的更长序列

现代变体：
  可学习位置编码（BERT, GPT）
  RoPE 旋转位置编码（LLaMA, GPT-NeoX）
  ALiBi 线性偏置（MPT）
```

---

## 六、完整代码实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import math
from typing import Optional, Tuple


# ── 缩放点积注意力 ────────────────────────────────────

def scaled_dot_product_attention(
    Q: torch.Tensor,
    K: torch.Tensor,
    V: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    dropout: float = 0.0,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    缩放点积注意力（Vaswani et al., 2017）

    Args:
        Q:    (B, H, T_q, d_k)  Query
        K:    (B, H, T_k, d_k)  Key
        V:    (B, H, T_k, d_v)  Value
        mask: (B, 1, T_q, T_k) 或 (B, H, T_q, T_k)，True 表示屏蔽位置
        dropout: 注意力权重上的 dropout 概率

    Returns:
        output:       (B, H, T_q, d_v)
        attn_weights: (B, H, T_q, T_k)
    """
    d_k = Q.size(-1)

    # Q Kᵀ / √d_k：计算相关性分数
    scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)  # (B,H,T_q,T_k)

    # 屏蔽不应关注的位置（如填充位、未来词）
    if mask is not None:
        scores = scores.masked_fill(mask, float('-inf'))

    attn_weights = F.softmax(scores, dim=-1)   # (B, H, T_q, T_k)

    if dropout > 0.0 and torch.is_grad_enabled():
        attn_weights = F.dropout(attn_weights, p=dropout)

    output = torch.matmul(attn_weights, V)     # (B, H, T_q, d_v)
    return output, attn_weights


# ── 多头注意力 ────────────────────────────────────────

class MultiHeadAttention(nn.Module):
    """
    多头注意力机制（Vaswani et al., 2017）

    输入：Q, K, V（对于 Self-Attention，三者相同；
                   对于 Cross-Attention，Q 来自 Decoder，K/V 来自 Encoder）
    """

    def __init__(self, d_model: int = 512, n_heads: int = 8,
                 dropout: float = 0.1):
        """
        Args:
            d_model:  模型总维度
            n_heads:  注意力头数（d_model 必须整除 n_heads）
            dropout:  注意力权重的 Dropout 概率
        """
        super().__init__()
        assert d_model % n_heads == 0, f"d_model ({d_model}) 必须整除 n_heads ({n_heads})"

        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads   # 每个头的维度

        # 四个线性投影（Q, K, V, 输出）
        self.W_Q = nn.Linear(d_model, d_model, bias=False)
        self.W_K = nn.Linear(d_model, d_model, bias=False)
        self.W_V = nn.Linear(d_model, d_model, bias=False)
        self.W_O = nn.Linear(d_model, d_model, bias=False)

        self.dropout = dropout
        self._reset_parameters()

    def _reset_parameters(self):
        nn.init.xavier_uniform_(self.W_Q.weight)
        nn.init.xavier_uniform_(self.W_K.weight)
        nn.init.xavier_uniform_(self.W_V.weight)
        nn.init.xavier_uniform_(self.W_O.weight)

    def _split_heads(self, x: torch.Tensor) -> torch.Tensor:
        """(B, T, d_model) → (B, n_heads, T, d_k)"""
        B, T, _ = x.shape
        return x.view(B, T, self.n_heads, self.d_k).transpose(1, 2)

    def _merge_heads(self, x: torch.Tensor) -> torch.Tensor:
        """(B, n_heads, T, d_k) → (B, T, d_model)"""
        B, _, T, _ = x.shape
        return x.transpose(1, 2).contiguous().view(B, T, self.d_model)

    def forward(self,
                query: torch.Tensor,
                key: torch.Tensor,
                value: torch.Tensor,
                mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            query: (B, T_q, d_model)
            key:   (B, T_k, d_model)
            value: (B, T_k, d_model)
            mask:  屏蔽矩阵（可选）

        Returns:
            output:       (B, T_q, d_model)
            attn_weights: (B, n_heads, T_q, T_k)
        """
        # 线性投影 + 分头
        Q = self._split_heads(self.W_Q(query))   # (B, H, T_q, d_k)
        K = self._split_heads(self.W_K(key))     # (B, H, T_k, d_k)
        V = self._split_heads(self.W_V(value))   # (B, H, T_k, d_k)

        # 缩放点积注意力
        dropout_p = self.dropout if self.training else 0.0
        attn_out, attn_w = scaled_dot_product_attention(Q, K, V, mask, dropout_p)

        # 合并多头 + 输出投影
        output = self.W_O(self._merge_heads(attn_out))   # (B, T_q, d_model)
        return output, attn_w


# ── 前馈网络 ──────────────────────────────────────────

class FeedForward(nn.Module):
    """
    Position-wise 前馈网络（每个位置独立，参数共享）
    结构：Linear(d_model → d_ff) - ReLU - Dropout - Linear(d_ff → d_model)
    """

    def __init__(self, d_model: int = 512, d_ff: int = 2048,
                 dropout: float = 0.1):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


# ── 位置编码 ──────────────────────────────────────────

class PositionalEncoding(nn.Module):
    """
    正弦/余弦位置编码（Vaswani et al., 2017）
    PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
    PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
    """

    def __init__(self, d_model: int = 512, max_len: int = 5000,
                 dropout: float = 0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)

        # 预计算位置编码表
        pe = torch.zeros(max_len, d_model)
        pos = torch.arange(max_len, dtype=torch.float).unsqueeze(1)
        div = torch.exp(torch.arange(0, d_model, 2, dtype=torch.float)
                        * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(pos * div)   # 偶数维度：sin
        pe[:, 1::2] = torch.cos(pos * div)   # 奇数维度：cos

        self.register_buffer('pe', pe.unsqueeze(0))   # (1, max_len, d_model)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, T, d_model)"""
        return self.dropout(x + self.pe[:, :x.size(1)])


# ── Encoder Layer ────────────────────────────────────

class TransformerEncoderLayer(nn.Module):
    """
    单个 Transformer Encoder 层

    结构（Pre-LN，现代变体，更稳定）：
      x = x + Dropout(Self-Attention(LayerNorm(x)))
      x = x + Dropout(FFN(LayerNorm(x)))
    """

    def __init__(self, d_model: int = 512, n_heads: int = 8,
                 d_ff: int = 2048, dropout: float = 0.1):
        super().__init__()
        self.self_attn = MultiHeadAttention(d_model, n_heads, dropout)
        self.ffn       = FeedForward(d_model, d_ff, dropout)
        self.norm1     = nn.LayerNorm(d_model)
        self.norm2     = nn.LayerNorm(d_model)
        self.dropout1  = nn.Dropout(dropout)
        self.dropout2  = nn.Dropout(dropout)

    def forward(self, x: torch.Tensor,
                src_mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        # Pre-LN Self-Attention
        normed = self.norm1(x)
        attn_out, attn_w = self.self_attn(normed, normed, normed, src_mask)
        x = x + self.dropout1(attn_out)

        # Pre-LN FFN
        x = x + self.dropout2(self.ffn(self.norm2(x)))
        return x, attn_w


# ── Decoder Layer ────────────────────────────────────

class TransformerDecoderLayer(nn.Module):
    """
    单个 Transformer Decoder 层

    结构：
      ① Masked Self-Attention（防止看到未来词）
      ② Cross-Attention（Q←Decoder，K/V←Encoder）
      ③ FFN
    """

    def __init__(self, d_model: int = 512, n_heads: int = 8,
                 d_ff: int = 2048, dropout: float = 0.1):
        super().__init__()
        self.self_attn  = MultiHeadAttention(d_model, n_heads, dropout)
        self.cross_attn = MultiHeadAttention(d_model, n_heads, dropout)
        self.ffn        = FeedForward(d_model, d_ff, dropout)
        self.norm1  = nn.LayerNorm(d_model)
        self.norm2  = nn.LayerNorm(d_model)
        self.norm3  = nn.LayerNorm(d_model)
        self.drop1  = nn.Dropout(dropout)
        self.drop2  = nn.Dropout(dropout)
        self.drop3  = nn.Dropout(dropout)

    def forward(self,
                x: torch.Tensor,
                enc_out: torch.Tensor,
                tgt_mask: Optional[torch.Tensor] = None,
                src_mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        # ① Masked Self-Attention（causal mask 防止看未来）
        normed = self.norm1(x)
        sa_out, sa_w = self.self_attn(normed, normed, normed, tgt_mask)
        x = x + self.drop1(sa_out)

        # ② Cross-Attention（Q 来自 Decoder，K/V 来自 Encoder）
        normed = self.norm2(x)
        ca_out, ca_w = self.cross_attn(normed, enc_out, enc_out, src_mask)
        x = x + self.drop2(ca_out)

        # ③ FFN
        x = x + self.drop3(self.ffn(self.norm3(x)))
        return x, sa_w, ca_w


def make_causal_mask(size: int, device: torch.device) -> torch.Tensor:
    """
    生成 Causal（因果）掩码，防止 Decoder 看到未来词
    mask[i,j]=True 表示位置 i 不能关注位置 j（j>i）
    """
    return torch.triu(torch.ones(size, size, dtype=torch.bool, device=device), diagonal=1)


# ── 完整 Transformer ──────────────────────────────────

class Transformer(nn.Module):
    """Transformer 机器翻译模型（Vaswani et al., 2017）"""

    def __init__(self, src_vocab: int, tgt_vocab: int,
                 d_model: int = 512, n_heads: int = 8,
                 n_encoder_layers: int = 6, n_decoder_layers: int = 6,
                 d_ff: int = 2048, dropout: float = 0.1,
                 max_len: int = 512):
        super().__init__()
        self.src_embed = nn.Embedding(src_vocab, d_model, padding_idx=0)
        self.tgt_embed = nn.Embedding(tgt_vocab, d_model, padding_idx=0)
        self.pos_enc   = PositionalEncoding(d_model, max_len, dropout)

        self.encoder = nn.ModuleList([
            TransformerEncoderLayer(d_model, n_heads, d_ff, dropout)
            for _ in range(n_encoder_layers)
        ])
        self.decoder = nn.ModuleList([
            TransformerDecoderLayer(d_model, n_heads, d_ff, dropout)
            for _ in range(n_decoder_layers)
        ])

        self.enc_norm = nn.LayerNorm(d_model)
        self.dec_norm = nn.LayerNorm(d_model)
        self.output_proj = nn.Linear(d_model, tgt_vocab, bias=False)

        # 权重绑定（src/tgt embedding 与输出投影共享，减少参数）
        if src_vocab == tgt_vocab:
            self.output_proj.weight = self.src_embed.weight

        self._init_weights()

    def _init_weights(self):
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)

    def encode(self, src: torch.Tensor,
               src_key_padding_mask: Optional[torch.Tensor] = None
               ) -> torch.Tensor:
        x = self.pos_enc(self.src_embed(src) * math.sqrt(self.src_embed.embedding_dim))
        for layer in self.encoder:
            x, _ = layer(x, src_key_padding_mask)
        return self.enc_norm(x)

    def decode(self, tgt: torch.Tensor, enc_out: torch.Tensor,
               tgt_mask: Optional[torch.Tensor] = None,
               src_key_padding_mask: Optional[torch.Tensor] = None
               ) -> torch.Tensor:
        d = self.tgt_embed.embedding_dim
        x = self.pos_enc(self.tgt_embed(tgt) * math.sqrt(d))
        for layer in self.decoder:
            x, _, _ = layer(x, enc_out, tgt_mask, src_key_padding_mask)
        return self.dec_norm(x)

    def forward(self, src: torch.Tensor, tgt: torch.Tensor,
                src_key_padding_mask: Optional[torch.Tensor] = None
                ) -> torch.Tensor:
        T_tgt = tgt.size(1)
        tgt_mask = make_causal_mask(T_tgt, src.device).unsqueeze(0).unsqueeze(0)
        enc_out  = self.encode(src, src_key_padding_mask)
        dec_out  = self.decode(tgt, enc_out, tgt_mask, src_key_padding_mask)
        return self.output_proj(dec_out)   # (B, T_tgt, tgt_vocab)


# ── 演示 ──────────────────────────────────────────────
if __name__ == "__main__":
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    B, T_src, T_tgt = 4, 20, 18

    print("=== Transformer 架构验证 ===")
    model = Transformer(src_vocab=8000, tgt_vocab=6000,
                        d_model=512, n_heads=8,
                        n_encoder_layers=6, n_decoder_layers=6,
                        d_ff=2048, dropout=0.1).to(device)

    src = torch.randint(1, 8000, (B, T_src), device=device)
    tgt = torch.randint(1, 6000, (B, T_tgt), device=device)

    logits = model(src, tgt)
    print(f"  输入 src：{src.shape}")
    print(f"  输入 tgt：{tgt.shape}")
    print(f"  输出 logits：{logits.shape}")   # (4, 18, 6000)
    total = sum(p.numel() for p in model.parameters())
    print(f"  总参数量：{total:,}")

    # 注意力权重可视化验证
    enc_layer = TransformerEncoderLayer(d_model=64, n_heads=4)
    x = torch.randn(2, 10, 64)
    out, attn_w = enc_layer(x)
    print(f"\n  Encoder 层输出：{out.shape}")
    print(f"  注意力权重：{attn_w.shape}")     # (2, 4, 10, 10)
    print(f"  权重行和（≈1.0）：{attn_w[0,0].sum(dim=-1).round(decimals=4)}")
```

---

## 七、Transformer 的架构变体

```
原版 Transformer（2017）：Encoder + Decoder，机器翻译
  ↓                              ↓
BERT（2018）                  GPT（2018）
  只用 Encoder                  只用 Decoder
  双向自注意力                   单向（Causal）自注意力
  填空式预训练（MLM）             语言模型预训练
  分类/NER/QA 微调              生成式任务
  ↓                              ↓
RoBERTa, ALBERT, DistilBERT    GPT-2, GPT-3, GPT-4, Claude
  ↓                    多模态融合 ↘
ViT（2020）                     CLIP, DALL-E, GPT-4V
图像 Patch → Transformer         Gemini, Claude 3
```

---

## 八、Transformer vs RNN 的关键优势

| 维度 | RNN（LSTM）| Transformer |
|------|-----------|-------------|
| 并行度 | 串行（O(T)步）| 完全并行（O(1)步） |
| 长程依赖 | O(T)次变换 | 直接注意力（O(1)） |
| 训练速度 | 慢 | GPU 友好，快 |
| 内存复杂度 | O(T) | O(T²)（注意力矩阵） |
| 外推能力 | 较好 | 需要 RoPE 等位置编码 |

---

## 九、历史地位

| 维度 | 评价 |
|------|------|
| 架构革命 | ⭐⭐⭐⭐⭐ 彻底取代 RNN，成为 NLP 统一框架 |
| 并行化 | ⭐⭐⭐⭐⭐ 充分利用 GPU/TPU，训练速度数量级提升 |
| 普适性 | ⭐⭐⭐⭐⭐ NLP→CV→音频→多模态，统治一切序列任务 |
| 历史影响 | ⭐⭐⭐⭐⭐ GPT、BERT、Claude 的直接基础架构 |

---

## 一句话总结

> Transformer 把"注意力"从一个辅助机制变成了万物的基础——7 年后，人类文明使用的最强 AI 系统，无一例外都建立在这篇论文的架构之上。

---

*参考：Vaswani, A., et al. (2017). Attention is all you need. NeurIPS, 30.*
