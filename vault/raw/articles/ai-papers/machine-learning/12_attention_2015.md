# 12 · 注意力机制（Attention Mechanism）
> 《Neural Machine Translation by Jointly Learning to Align and Translate》  
> **作者**：Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio　**会议**：ICLR　**年份**：2015

---

## 一、历史背景：编码器-解码器的固定瓶颈

2014 年，Cho 等人提出了 seq2seq 架构（Encoder-Decoder），在机器翻译上取得突破：

```
"Je suis étudiant"
  ↓ Encoder（RNN）逐词处理
  → 最终隐藏状态 c（固定长度向量，如 512 维）
  ↓ Decoder（RNN）从 c 逐词生成
"I am a student"
```

**致命瓶颈**：整个源句子的信息被压缩进**一个固定长度向量 c**：

```
短句（5词）→ c        ← 还能装下
长句（50词）→ c       ← 信息丢失严重！
复杂句（100词）→ c    ← 几乎无法翻译

实验验证：BLEU 分数随源句长度增加急剧下降
```

Bahdanau 的核心问题：

> **"翻译每个目标词时，Decoder 能不能回头看原文的不同位置，而不是仅依赖一个固定向量？"**

答案正是**注意力机制（Attention Mechanism）**。

---

## 二、注意力机制：动态上下文向量

**核心思想**：翻译每个目标词时，动态地对源句子所有位置加权求和，生成**该时刻专属的上下文向量 cₜ**：

```
翻译 "étudiant" → "student" 时：

源句子各位置注意力权重：
  Je      : α₁ = 0.05   ← 几乎不看
  suis    : α₂ = 0.08   ← 几乎不看
  étudiant: α₃ = 0.82   ← 高度关注！

上下文向量 c₃ = 0.05·h₁ + 0.08·h₂ + 0.82·h₃   ← 动态加权！

（对比 seq2seq：每个时刻都用同一个固定 c）
```

这使得翻译可以**选择性地聚焦**于源句子中与当前目标词最相关的部分。

---

## 三、注意力计算的完整步骤

设：
- 源句子编码：h₁, h₂, ..., hₙ（双向 RNN 各位置的隐藏状态）
- Decoder 当前状态：sₜ₋₁

**第一步：计算对齐分数（Alignment Scores）**

```
eᵢₜ = a(sₜ₋₁, hᵢ) = vᵀ · tanh(Wa · sₜ₋₁ + Ua · hᵢ)
         ↑ 一个小的前馈网络，学习"哪些源位置对当前解码最相关"
```

**第二步：Softmax 归一化得到注意力权重**

```
αᵢₜ = exp(eᵢₜ) / Σⱼ exp(eⱼₜ)     ← αᵢₜ ∈ [0,1]，Σᵢ αᵢₜ = 1
```

**第三步：加权求和得到上下文向量**

```
cₜ = Σᵢ αᵢₜ · hᵢ
```

**第四步：Decoder 利用 cₜ 生成当前词**

```
sₜ = f(sₜ₋₁, yₜ₋₁, cₜ)
P(yₜ | y₁,...,yₜ₋₁, x) = softmax(g(sₜ, cₜ, yₜ₋₁))
```

---

## 四、注意力对齐矩阵：可解释性的突破

注意力权重 α 构成了一个**对齐矩阵**——机器翻译第一次变得直观可解释：

```
（行=目标词，列=源词，颜色深度=注意力权重）

             I    am   a   student
  Je         ██   ░    ░    ░
  suis       ░    ██   ░    ░
  étudiant   ░    ░    ░    ██
  
（对角线模式 = 语序相近的语言对，如英法）

复杂对齐（英语→法语 "the European Economic Area"）：
  la    zone    économique    européenne
  the   Area    Economic      European
  ← 语序调换，注意力矩阵出现了反对角线 ↗ 模式
```

---

## 五、三种注意力变体对比

| 类型 | 对齐函数 | 优点 | 提出者 |
|------|---------|------|--------|
| **加性注意力（Additive）** | `vᵀ tanh(Wa·s + Ua·h)` | 参数灵活，效果好 | Bahdanau (2015) |
| **点积注意力（Dot-product）** | `sᵀ h` | 无需额外参数，速度快 | Luong (2015) |
| **缩放点积（Scaled Dot-product）** | `sᵀ h / √d` | 防止维度高时点积过大 | Vaswani (2017) |
| **乘性注意力（General）** | `sᵀ W h` | 折中方案 | Luong (2015) |

---

## 六、完整代码实现

```python
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from typing import Tuple, Optional


class BahdanauAttention(nn.Module):
    """
    Bahdanau 加性注意力机制（2015）

    对齐函数：e(s, h) = vᵀ · tanh(Wa·s + Ua·h)
    """

    def __init__(self, encoder_dim: int, decoder_dim: int,
                 attn_dim: int = 256):
        """
        Args:
            encoder_dim: 编码器隐藏状态维度
            decoder_dim: 解码器隐藏状态维度
            attn_dim:    注意力中间层维度
        """
        super().__init__()
        # 对齐网络参数
        self.Wa = nn.Linear(decoder_dim, attn_dim, bias=False)   # 解码器状态投影
        self.Ua = nn.Linear(encoder_dim, attn_dim, bias=False)   # 编码器状态投影
        self.va = nn.Linear(attn_dim, 1, bias=False)             # 分数压缩到标量

    def forward(self, decoder_state: torch.Tensor,
                encoder_outputs: torch.Tensor,
                mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            decoder_state:   (B, decoder_dim)  当前解码器状态 sₜ₋₁
            encoder_outputs: (B, T_src, encoder_dim)  编码器所有输出
            mask:            (B, T_src)  True 表示填充位置（需要屏蔽）

        Returns:
            context:      (B, encoder_dim)  加权上下文向量 cₜ
            attn_weights: (B, T_src)       注意力权重（可用于可视化）
        """
        T_src = encoder_outputs.size(1)

        # 计算对齐分数 eᵢₜ = vᵀ · tanh(Wa·s + Ua·h)
        # decoder_state: (B, D) → (B, 1, attn_dim) 广播到所有源位置
        dec_proj = self.Wa(decoder_state).unsqueeze(1)          # (B, 1, attn_dim)
        enc_proj = self.Ua(encoder_outputs)                      # (B, T_src, attn_dim)

        energy = torch.tanh(dec_proj + enc_proj)                 # (B, T_src, attn_dim)
        scores = self.va(energy).squeeze(-1)                     # (B, T_src)

        # 屏蔽填充位置（将 -inf 使得 softmax 后权重为 0）
        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        # Softmax 归一化
        attn_weights = F.softmax(scores, dim=-1)                 # (B, T_src)

        # 加权求和得到上下文向量
        context = torch.bmm(
            attn_weights.unsqueeze(1),    # (B, 1, T_src)
            encoder_outputs               # (B, T_src, encoder_dim)
        ).squeeze(1)                      # (B, encoder_dim)

        return context, attn_weights


class LuongAttention(nn.Module):
    """
    Luong 点积/通用注意力（2015）

    更简洁，Transformer 缩放点积注意力的直接前身
    """

    def __init__(self, hidden_dim: int, method: str = "general"):
        """
        Args:
            hidden_dim: 隐藏状态维度（编码器=解码器）
            method:     'dot'（点积）| 'general'（乘性）| 'concat'（拼接）
        """
        super().__init__()
        self.method = method
        if method == "general":
            self.W = nn.Linear(hidden_dim, hidden_dim, bias=False)
        elif method == "concat":
            self.W = nn.Linear(hidden_dim * 2, hidden_dim, bias=False)
            self.v = nn.Linear(hidden_dim, 1, bias=False)

    def forward(self, decoder_state: torch.Tensor,
                encoder_outputs: torch.Tensor,
                mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Args:
            decoder_state:   (B, H)
            encoder_outputs: (B, T, H)
        """
        if self.method == "dot":
            # 简单点积
            scores = torch.bmm(
                encoder_outputs,
                decoder_state.unsqueeze(2)
            ).squeeze(2)                                         # (B, T)

        elif self.method == "general":
            # 乘性注意力
            transformed = self.W(decoder_state)                  # (B, H)
            scores = torch.bmm(
                encoder_outputs,
                transformed.unsqueeze(2)
            ).squeeze(2)

        elif self.method == "concat":
            # 拼接注意力
            dec_expanded = decoder_state.unsqueeze(1).expand_as(encoder_outputs)
            concat = torch.cat([dec_expanded, encoder_outputs], dim=-1)
            scores = self.v(torch.tanh(self.W(concat))).squeeze(-1)

        if mask is not None:
            scores = scores.masked_fill(mask, float('-inf'))

        attn_weights = F.softmax(scores, dim=-1)
        context = torch.bmm(attn_weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context, attn_weights


class Seq2SeqWithAttention(nn.Module):
    """
    带 Bahdanau 注意力的 Encoder-Decoder 机器翻译模型
    """

    def __init__(self, src_vocab: int, tgt_vocab: int,
                 embed_dim: int = 256, hidden_dim: int = 512,
                 attn_dim: int = 256, dropout: float = 0.3):
        super().__init__()
        # Encoder：双向 GRU（合并两个方向，提供丰富上下文）
        self.src_embed = nn.Embedding(src_vocab, embed_dim, padding_idx=0)
        self.encoder = nn.GRU(embed_dim, hidden_dim, batch_first=True,
                               bidirectional=True)
        # 双向 → 单向投影（供 Decoder 初始化用）
        self.enc2dec = nn.Linear(hidden_dim * 2, hidden_dim)

        # Decoder：单向 GRU
        self.tgt_embed = nn.Embedding(tgt_vocab, embed_dim, padding_idx=0)
        self.decoder = nn.GRUCell(embed_dim + hidden_dim * 2, hidden_dim)

        # 注意力层
        self.attention = BahdanauAttention(hidden_dim * 2, hidden_dim, attn_dim)

        # 输出投影
        self.dropout = nn.Dropout(dropout)
        self.output_proj = nn.Linear(hidden_dim + hidden_dim * 2 + embed_dim, tgt_vocab)

    def encode(self, src: torch.Tensor,
               src_mask: Optional[torch.Tensor] = None
               ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        编码源序列

        Returns:
            enc_out:      (B, T_src, 2H)  所有位置的编码表示
            dec_init:     (B, H)          解码器初始隐藏状态
        """
        emb = self.dropout(self.src_embed(src))                  # (B, T_src, E)
        enc_out, h_n = self.encoder(emb)                         # enc_out: (B, T_src, 2H)
        # 合并双向最终状态作为解码器初始状态
        dec_init = torch.tanh(self.enc2dec(
            torch.cat([h_n[-2], h_n[-1]], dim=-1)))              # (B, H)
        return enc_out, dec_init

    def decode_step(self, tgt_token: torch.Tensor,
                    dec_hidden: torch.Tensor,
                    enc_out: torch.Tensor,
                    src_mask: Optional[torch.Tensor] = None
                    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        解码一步

        Returns:
            logits:      (B, tgt_vocab)
            dec_hidden:  (B, H)
            attn_weights:(B, T_src)
        """
        emb = self.dropout(self.tgt_embed(tgt_token))            # (B, E)
        context, attn_w = self.attention(dec_hidden, enc_out, src_mask)

        # GRUCell 输入：[词嵌入, 上下文向量]
        dec_input = torch.cat([emb, context], dim=-1)            # (B, E+2H)
        dec_hidden = self.decoder(dec_input, dec_hidden)         # (B, H)

        # 输出：基于隐藏状态+上下文+词嵌入的三路融合
        out = torch.cat([dec_hidden, context, emb], dim=-1)
        logits = self.output_proj(self.dropout(out))             # (B, tgt_vocab)
        return logits, dec_hidden, attn_w

    def forward(self, src: torch.Tensor, tgt: torch.Tensor,
                src_mask: Optional[torch.Tensor] = None
                ) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Teacher forcing 训练

        Returns:
            all_logits:   (B, T_tgt, tgt_vocab)
            all_attentions: (B, T_tgt, T_src)  注意力矩阵（可视化用）
        """
        B, T_tgt = tgt.shape
        enc_out, dec_hidden = self.encode(src, src_mask)

        all_logits, all_attentions = [], []
        for t in range(T_tgt):
            logits, dec_hidden, attn_w = self.decode_step(
                tgt[:, t], dec_hidden, enc_out, src_mask)
            all_logits.append(logits)
            all_attentions.append(attn_w)

        return (torch.stack(all_logits, dim=1),
                torch.stack(all_attentions, dim=1))

    @torch.no_grad()
    def translate(self, src: torch.Tensor, max_len: int = 50,
                  sos_id: int = 1, eos_id: int = 2
                  ) -> Tuple[list, torch.Tensor]:
        """贪婪解码推理"""
        self.eval()
        enc_out, dec_hidden = self.encode(src)
        token = torch.tensor([sos_id] * src.size(0), device=src.device)
        output_ids, attention_maps = [], []

        for _ in range(max_len):
            logits, dec_hidden, attn_w = self.decode_step(token, dec_hidden, enc_out)
            token = logits.argmax(dim=-1)
            output_ids.append(token.cpu().tolist())
            attention_maps.append(attn_w.cpu())
            if (token == eos_id).all():
                break

        return output_ids, torch.stack(attention_maps, dim=1)


# ── 演示 ──────────────────────────────────────────────
if __name__ == "__main__":
    device = torch.device("cpu")
    B, T_src, T_tgt = 4, 12, 10

    print("=== Bahdanau Attention 单步验证 ===")
    attn = BahdanauAttention(encoder_dim=512, decoder_dim=256, attn_dim=128)
    dec_state = torch.randn(B, 256)
    enc_outs  = torch.randn(B, T_src, 512)
    context, weights = attn(dec_state, enc_outs)
    print(f"  上下文向量：{context.shape}")         # (4, 512)
    print(f"  注意力权重：{weights.shape}")          # (4, 12)
    print(f"  权重和（≈1.0）：{weights.sum(dim=1)}")

    print("\n=== Seq2Seq + Attention 完整模型 ===")
    model = Seq2SeqWithAttention(
        src_vocab=5000, tgt_vocab=4000,
        embed_dim=128, hidden_dim=256, attn_dim=128
    )
    src = torch.randint(1, 5000, (B, T_src))
    tgt = torch.randint(1, 4000, (B, T_tgt))
    logits, attentions = model(src, tgt)
    print(f"  输出 logits：{logits.shape}")          # (4, 10, 4000)
    print(f"  注意力矩阵：{attentions.shape}")        # (4, 10, 12)
    print(f"  参数量：{sum(p.numel() for p in model.parameters()):,}")
```

---

## 七、注意力机制的演化：从 seq2seq 到 Transformer

```
Bahdanau Attention（2015）
  加性注意力：e(s,h) = vᵀ tanh(Wa·s + Ua·h)
  用于 RNN Encoder-Decoder，解决固定瓶颈
  ↓
Luong Attention（2015）
  点积/乘性注意力：e(s,h) = sᵀWh
  更简洁，速度更快
  ↓
Self-Attention（2017，Transformer）
  Q=K=V=序列自身：序列内部位置相互关注
  彻底去掉 RNN，完全并行化！
  ↓
Multi-Head Attention（2017）
  并行 h 组注意力，每组关注不同语义方面
  ↓
Cross-Attention（Transformer Decoder）
  Q 来自 Decoder，K/V 来自 Encoder
  本质上正是 Bahdanau Attention 的广义化
  ↓
Flash Attention（2022）
  IO 感知的高效注意力实现，使 Transformer 训练更快 10 倍
```

---

## 八、历史地位

| 维度 | 评价 |
|------|------|
| 问题解决 | ⭐⭐⭐⭐⭐ 彻底解决了固定瓶颈问题 |
| 可解释性 | ⭐⭐⭐⭐⭐ 注意力矩阵使翻译过程可视化 |
| 历史地位 | ⭐⭐⭐⭐⭐ Transformer 的直接前身 |
| 影响深度 | ⭐⭐⭐⭐⭐ 现代所有 LLM 的核心机制之源 |

---

## 一句话总结

> 注意力机制告诉我们，好的翻译家不是死记全文——而是翻译每个词时，**知道该看哪里**。这个简单洞见，最终演化成了 GPT 和 Claude 的核心。

---

*参考：Bahdanau, D., Cho, K., & Bengio, Y. (2014). Neural machine translation by jointly learning to align and translate. ICLR 2015.*
