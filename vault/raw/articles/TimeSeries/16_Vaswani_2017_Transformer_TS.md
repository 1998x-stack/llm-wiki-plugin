# 第十六篇：Transformer——注意力机制重塑时间序列建模
> **论文原名**：*Attention Is All You Need*  
> **作者**：Ashish Vaswani 等（Google Brain / Google Research）  
> **发表年份**：2017 年  
> **发表会议**：*NeurIPS 2017*

---

## 一、历史背景：LSTM 的瓶颈

2017 年之前，序列到序列（Seq2Seq）建模几乎被 LSTM/GRU 统治。但研究者们越来越清晰地意识到几个根本局限：

1. **顺序计算的并行瓶颈**：RNN 必须按时间步顺序计算 $h_1 \to h_2 \to \cdots \to h_T$，即使在 GPU 上也无法充分并行，训练极慢
2. **固定大小的隐状态是信息瓶颈**：编码器将整个输入序列压缩为固定维度向量，长序列信息严重丢失
3. **长距离依赖仍然困难**：即使有门控，当 $T$ 达到数百时，LSTM 对早期信息的"访问"仍然间接而低效

2015 年，Bahdanau 等人提出注意力机制：**让解码器直接"看"编码器所有位置的隐状态，并按相关性加权聚合**。这一改进大幅提升了翻译质量，但仍依赖 RNN。

Google Brain 的 Vaswani 等人在 2017 年提出了一个激进的方案：**完全抛弃 RNN 和卷积，仅用自注意力机制构建序列模型**——"Attention Is All You Need"。

---

## 二、自注意力机制（Self-Attention）

### 2.1 Query-Key-Value 框架

对于序列 $\mathbf{X} = [x_1, \ldots, x_T] \in \mathbb{R}^{T \times d}$，自注意力计算如下：

将每个位置的表示投影为三个向量（**查询 Query、键 Key、值 Value**）：

$$\mathbf{Q} = \mathbf{X}\mathbf{W}^Q, \quad \mathbf{K} = \mathbf{X}\mathbf{W}^K, \quad \mathbf{V} = \mathbf{X}\mathbf{W}^V$$

其中 $\mathbf{W}^Q, \mathbf{W}^K \in \mathbb{R}^{d \times d_k}$，$\mathbf{W}^V \in \mathbb{R}^{d \times d_v}$ 是可学习权重。

**注意力权重与输出**：

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Softmax}\left(\frac{\mathbf{Q}\mathbf{K}^{\top}}{\sqrt{d_k}}\right)\mathbf{V}$$

**直觉**：
- 相似的 Query-Key 对（内积大）得到高注意力权重
- 最终输出是 Value 的加权和，权重反映"与当前位置的相关性"
- $1/\sqrt{d_k}$ 是缩放因子，防止点积过大导致 Softmax 饱和

### 2.2 多头注意力（Multi-Head Attention）

不同注意力头关注序列的不同方面（局部模式、全局结构、特定关系）：

$$\text{MultiHead}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{Concat}(\text{head}_1, \ldots, \text{head}_h)\mathbf{W}^O$$

$$\text{head}_i = \text{Attention}(\mathbf{Q}\mathbf{W}^Q_i, \mathbf{K}\mathbf{W}^K_i, \mathbf{V}\mathbf{W}^V_i)$$

$h$ 个并行的注意力头独立学习不同的 Q/K/V 投影，拼接后再线性变换。

### 2.3 位置编码（Positional Encoding）

自注意力对序列顺序**天然不敏感**（打乱顺序输出相同）。为注入位置信息，加入正弦-余弦位置编码：

$$\text{PE}(t, 2i) = \sin\left(\frac{t}{10000^{2i/d}}\right), \quad \text{PE}(t, 2i+1) = \cos\left(\frac{t}{10000^{2i/d}}\right)$$

不同频率的正弦波为每个位置生成唯一的"指纹"，且相对位置关系在点积空间中得到保持。

---

## 三、Transformer 的完整架构

Transformer 由**编码器（Encoder）**和**解码器（Decoder）**堆叠而成，每层结构相同：

**编码器层**：
1. 多头自注意力（每个位置关注所有位置）
2. 残差连接 + Layer Norm
3. 前馈神经网络（逐位置的 FFN：两层线性 + ReLU）
4. 残差连接 + Layer Norm

**解码器层**（在编码器基础上）：
1. **因果（Masked）自注意力**：只关注过去位置（防止"看未来"）
2. **交叉注意力**：Query 来自解码器，Key/Value 来自编码器输出
3. FFN

**复杂度对比**（序列长度 $T$）：

| 模型 | 每层计算量 | 最大路径长度（两端信息传播） |
|---|---|---|
| RNN | $O(T \cdot d^2)$ | $O(T)$ |
| CNN | $O(k \cdot T \cdot d^2)$ | $O(T/k)$ |
| **Self-Attention** | $O(T^2 \cdot d)$ | **$O(1)$** |

自注意力的最大路径长度为 $O(1)$——**任意两个时刻的信息可以在一层内直接交互**，这正是 Transformer 擅长长距离依赖的根本原因。代价是 $O(T^2)$ 的注意力计算，对长序列有限制。

---

## 四、Transformer 进入时间序列领域

原始 Transformer 是为 NLP 设计的，但其强大的序列建模能力迅速引发了时序预测领域的"Transformer 热"（2019—2022 年）。

### 4.1 时序 Transformer 的挑战

时间序列预测与 NLP 的关键差异：

| 维度 | NLP | 时间序列预测 |
|---|---|---|
| 输入类型 | 离散 Token（词汇表） | 连续数值 |
| 序列长度 | 通常 < 512 Token | 可达数千步（长序列预测） |
| 注意力需求 | 全局语义关联 | 局部模式 + 周期性远程关联 |
| 噪声水平 | 较低（文本结构清晰） | 高（随机噪声主导） |
| Permutation 不变性问题 | 不重要 | 时间顺序极重要 |

### 4.2 主要 TSF-Transformer 变体谱系

| 年份 | 模型 | 核心改进 |
|---|---|---|
| 2021 | **Informer** | ProbSparse 注意力 $O(L\log L)$，解锁长序列 |
| 2021 | **Autoformer** | 自相关替代注意力，嵌入序列分解 |
| 2022 | **FEDformer** | 频域注意力（Fourier/Wavelet），$O(L)$ |
| 2022 | **Pyraformer** | 金字塔注意力，层级时序结构 |
| 2023 | **PatchTST** | Patch 分词 + Channel-Independence，显著改进 |
| 2023 | **iTransformer** | 将变量（而非时间步）作为 Token |

---

## 五、注意力在时序中的真正作用

时序 Transformer 的一个重要研究问题：**注意力机制究竟学到了什么？**

实验（Zhou et al. 2021, Nie et al. 2023 等）发现：

- 时序数据的注意力权重矩阵往往高度稀疏，大部分注意力集中在少数位置
- 注意力擅长捕捉**点对点的时间关联**（如相同季节的历史时刻）
- 但对于局部平滑趋势和短期模式，简单的卷积或线性层反而更有效

这一发现在 2023 年引发了"Transformer 是否真的适合时序"的大争论（DLinear 论文，Zeng et al. 2023 的核心贡献，我们最后一篇），促使研究者更严格地设计控制实验。

---

## 六、时序 Transformer 的位置编码改进

原始正弦位置编码对时序数据的语义不足：它只编码了"第几步"，但没有编码"这个时刻是几月几号、星期几"等更丰富的时间语义。

现代时序 Transformer 通常使用**可学习的时间特征嵌入（Temporal Embedding）**：

$$\text{TemporalEmb}(t) = \text{Embed}(\text{month}_t) + \text{Embed}(\text{weekday}_t) + \text{Embed}(\text{hour}_t) + \ldots$$

或使用 **Time2Vec**（Kazemi et al. 2019）：

$$\text{t2v}(t)[i] = \begin{cases} \omega_i t + \phi_i & i = 0 \\ \sin(\omega_i t + \phi_i) & i > 0 \end{cases}$$

---

## 七、Transformer 在时序预测中的历史评价

从历史视角看，2019—2022 年的"时序 Transformer 热"留下了复杂的遗产：

**正面影响**：
- 将深度学习社区最强的架构能力引入时序领域
- 推动了大规模时序预测数据集（ETTh1/2, ETTm1/2, Traffic, Weather 等）的标准化
- 催生了 PatchTST 等真正有实质突破的工作

**反思**：
- 许多 Transformer 变体的改进主要来自更复杂的预处理（RevIN、序列分解）而非注意力本身
- Zeng et al.（2023）证明单层线性模型（DLinear）可以超越多个 Transformer 变体
- 时序预测的"归纳偏置"与 NLP 截然不同，直接移植 Transformer 并非最优

---

## 八、小结

Vaswani 等（2017）的 Transformer 是人工智能史上最具影响力的架构之一：

> **用纯注意力机制，以 $O(1)$ 的最大路径长度，并行化地建模任意序列中的全局依赖关系。**

对时间序列分析的三重影响：
1. **激发**：引发了时序 Transformer 的研究浪潮（Informer、Autoformer、PatchTST 等）
2. **反思**：使研究者深入追问"注意力在时序中究竟学到了什么"，推动了对归纳偏置的重新审视
3. **范式**：预训练 + 微调的 Transformer 范式（GPT、BERT）正在向时序领域延伸（Lag-LLaMA、TimesFM、Moirai 等时序基础模型）

---

*下一篇：Taylor & Letham（2018）——Prophet，面向业务分析师的可解释、可扩展预测工具。*
