# 现代推荐系统三驾马车：DIN · BERT4Rec · LightGCN

---

# 第一篇：DIN — Deep Interest Network (2018)

> **论文全名**：Deep Interest Network for Click-Through Rate Prediction  
> **作者**：Guorui Zhou, Xiaoqiang Zhu, Chenru Song, Ying Fan, Han Zhu, Xiao Ma, Yanghui Yan, Junqi Jin, Han Li, Kun Gai · Alibaba Group  
> **发表**：KDD 2018  
> **引用量**：~4000+  
> **实际部署**：阿里巴巴淘宝/天猫主推荐链路

---

## 一、用户兴趣是多元且动态的

在 DIN 之前，工业 CTR 模型（包括 Wide & Deep、DeepFM）处理用户行为序列的方式是：

```
用户历史行为：[鞋子, 包包, 裙子, 口红, 手表, ...]
         ↓
     Embedding + 平均池化
         ↓
   一个固定的用户向量
```

**问题**：对所有历史行为一视同仁，完全忽略了**当前候选物品与历史行为的相关性**。

**直觉上的错误**：
```
用户历史：[Nike跑鞋, Adidas运动裤, Gucci包, 香奈儿口红, 苹果手表]

当候选物品是"Adidas运动服"时：
→ 运动类行为（跑鞋、运动裤）更相关，应该重点关注

当候选物品是"Dior香水"时：
→ 奢侈品类行为（Gucci包、香奈儿口红）更相关

→ 不应该用同一个"平均用户向量"来预测这两种物品！
```

这就是 DIN 要解决的核心问题：**用户对候选物品的兴趣，应该从与该物品相关的历史行为中自适应地提取。**

---

## 二、DIN 的核心：注意力激活单元

DIN 引入了一个**局部激活单元（Local Activation Unit）**，根据候选广告自适应地计算用户历史行为的注意力权重：

$$
v_U(A) = f(V_a, e_1, e_2, ..., e_H) = \sum_{j=1}^H a(e_j, V_a) \cdot e_j = \sum_{j=1}^H w_j \cdot e_j
$$

其中：
- $V_a$：候选广告的 Embedding
- $e_j$：第 $j$ 个历史行为的 Embedding  
- $a(e_j, V_a)$：注意力分数（注意力激活单元输出）
- $w_j = a(e_j, V_a)$：第 $j$ 个历史行为对当前候选的权重

**注意力激活单元结构**：

```
[候选广告 Emb V_a] + [历史行为 Emb e_j] + [外积特征 V_a ⊗ e_j]
           ↓
     全连接层 (Concat → MLP → sigmoid)
           ↓
     注意力分数 w_j ∈ (0,1)
```

**与 Transformer Attention 的关键区别**：
- DIN 不做 softmax 归一化（保留总激活量作为用户兴趣强度信息）
- 注意力计算是非对称的（用 MLP 而非简单点积）
- 注意力网络输入了显式的外积特征 $V_a \odot e_j$

---

## 三、DIN 的训练创新

### 3.1 Mini-Batch Aware 正则化

DIN 面临的工程挑战：参数规模巨大（数亿 Embedding 参数），L2 正则化代价太高。

解决方案：只对在当前 mini-batch 中出现过的参数施加正则化：

$$
L_2(W) \approx \sum_{j=1}^K \frac{n_j}{n} \|w_j\|^2
$$

其中 $n_j$ 是参数 $j$ 在 batch 中的出现次数，$n$ 是 batch 大小。

### 3.2 数据自适应激活函数（Dice）

DIN 发现 PReLU 的固定转折点（0）对推荐数据不够自适应，提出 Dice：

$$
f(s) = p(s) \cdot s + (1-p(s)) \cdot \alpha s, \quad p(s) = \frac{1}{1+e^{-\frac{s-E[s]}{\sqrt{Var[s]+\epsilon}}}}
$$

转折点由数据的均值和方差动态决定，类似于 BatchNorm + PReLU 的组合。

---

## 四、DIN 的工业影响

DIN 在阿里巴巴主推荐链路上线后，CTR 提升显著，此后演化出一系列阿里推荐模型：

```
DIN (2018, KDD)：注意力机制 + 用户行为
  ↓
DIEN (2019, AAAI)：GRU 建模兴趣演化
  ↓
DSIN (2019, IJCAI)：Session 内行为建模
  ↓
BST (2019)：Transformer 用于行为序列
  ↓
CAN (2020)：更精细的候选感知注意力
```

---

---

# 第二篇：BERT4Rec (2019)

> **论文全名**：BERT4Rec: Sequential Recommendation with Bidirectional Encoder Representations from Transformers  
> **作者**：Fei Sun, Jun Liu, Jian Wu, Changhua Pei, Xiao Lin, Wenwu Ou, Peng Jiang · Alibaba Group  
> **发表**：CIKM 2019  
> **引用量**：~2500+

---

## 一、序列推荐的兴起

推荐系统的一个核心假设是：**用户的下一个行为，与他过去的行为序列有关。**

```
行为序列：[看了《权游》S1] → [看了《权游》S2] → [看了《冰与火之歌》] → ??? 
→ 推荐：《权游》S3，或者《魔戒》，或者《指环王》
```

序列推荐模型的演化：

```
RNN/GRU (2016): GRU4Rec，用循环网络建模序列
    ↓
SASRec (2018): 用单向Transformer（GPT风格），因果掩码
    ↓
BERT4Rec (2019): 用双向Transformer（BERT风格），Cloze任务
```

---

## 二、为什么用双向而非单向 Transformer

SASRec（2018，ICDM）已经将 Transformer 引入序列推荐，但使用的是**单向（自回归）**结构：每个位置只能看到它之前的行为。

BERT4Rec 的核心论点：

> **推荐场景不同于语言生成——我们在预测时拥有完整的历史序列，因此可以用双向注意力，充分利用上下文信息。**

对比：

| 框架 | 注意力方向 | 训练任务 | 预测时输入 |
|------|-----------|---------|-----------|
| GPT/SASRec | 单向（因果掩码） | 下一个 token 预测 | 已有序列 |
| BERT/BERT4Rec | 双向 | **Cloze（完形填空）** | 完整序列（含未来） |

---

## 三、Cloze 任务迁移到推荐

BERT 的预训练任务是 **Masked Language Model（MLM）**：随机遮住一些词，让模型预测被遮住的词。

BERT4Rec 将此改造为 **Cloze 任务用于推荐**：

```
原始序列：[Nike跑鞋, Adidas运动裤, [MASK], 苹果手表, [MASK]]
BERT4Rec 目标：预测 [MASK] 位置的物品
```

**训练时**：随机遮住序列中 15%-20% 的物品，用双向 Transformer 预测。

**测试时**：将目标预测位置替换为 `[MASK]`，模型预测最可能的物品。

---

## 四、BERT4Rec 的模型结构

```
输入序列：  v1    v2    [M]   v4    [M]
              ↓     ↓     ↓     ↓     ↓
Embedding: E(v1) E(v2) E([M]) E(v4) E([M])  ← Item Embedding
         + P(1)  P(2)  P(3)   P(4)  P(5)   ← Positional Embedding
              ↓     ↓     ↓     ↓     ↓
         [双向 Multi-Head Self-Attention × L层]
              ↓     ↓     ↓     ↓     ↓
输出：    h1    h2    h3    h4    h5
                      ↓           ↓
              预测 [M] 位置的物品（分类）
```

**关键超参数**：
- 序列长度：200（最大历史行为数）
- Embedding 维度：64
- Transformer 层数：2
- 注意力头数：2

---

## 五、BERT4Rec 的实验结果

在 MovieLens-1M、Steam、Beauty 等数据集上：

| 模型 | HR@10 | NDCG@10 |
|------|-------|---------|
| BPR-MF | 0.672 | 0.463 |
| GRU4Rec | 0.704 | 0.479 |
| SASRec | 0.745 | 0.521 |
| **BERT4Rec** | **0.774** | **0.551** |

---

## 六、BERT4Rec 的局限与后续

### 局限

1. **Cloze 任务 vs. 推荐任务的 gap**：训练时预测序列中间的物品，但推荐时是预测序列末尾的下一个物品
2. **计算开销**：双向注意力比单向更重（但双向的 NDCG 提升值得）
3. **冷启动**：新物品没有 ID Embedding

### 后续演化

```
BERT4Rec (2019)
    ↓
S3-Rec (2020): 自监督预训练，序列+内容联合
    ↓
UniSRec (2022): 文本内容的序列推荐，迁移到新场景
    ↓
LLM4Rec (2023+): 直接用大语言模型做序列推荐
```

---

---

# 第三篇：LightGCN (2020)

> **论文全名**：LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation  
> **作者**：Xiangnan He, Kelong Mao, Bing Wang, Feng Chen, Liqiang Nie, Zhaowei Chen, Tat-Seng Chua · USTC / NUS  
> **发表**：SIGIR 2020  
> **引用量**：~4000+

---

## 一、图神经网络与推荐系统的相遇

用户-物品关系天然构成一个二部图（Bipartite Graph）：

```
用户 A ─── 物品 1
用户 A ─── 物品 2
用户 B ─── 物品 2
用户 B ─── 物品 3
用户 C ─── 物品 1
用户 C ─── 物品 3
```

**图神经网络（GNN）的核心思想**：通过图上的消息传递，让节点的表示融合邻居信息。

在推荐图中：
- 与用户相连的物品节点，能提供关于用户偏好的信息
- 与物品相连的用户节点，能提供关于物品受众的信息

**关键洞察**：两跳之外的节点也携带信息（用户→物品→用户 揭示相似用户关系）。

---

## 二、NGCF：GNN 推荐的先驱与过度复杂

LightGCN 的前驱是 NGCF（Neural Graph Collaborative Filtering, SIGIR 2019），它将 GCN 引入协同过滤：

**NGCF 的传播规则**：

$$
e_u^{(k+1)} = \sigma\left(W_1 e_u^{(k)} + \sum_{i \in \mathcal{N}_u} \frac{1}{\sqrt{|\mathcal{N}_u||\mathcal{N}_i|}} (W_1 e_i^{(k)} + W_2 (e_i^{(k)} \odot e_u^{(k)}))\right)
$$

**问题**：引入了非线性激活（$\sigma$）和特征变换矩阵（$W_1, W_2$）和 element-wise 交互项，LightGCN 发现这些组件并不有效。

---

## 三、LightGCN 的核心洞察：大道至简

LightGCN 通过消融实验发现：

| 组件 | 对性能的影响 |
|------|------------|
| 非线性激活函数 | **负面**（去掉更好） |
| 特征变换矩阵 $W$ | **负面**（去掉更好） |
| Element-wise 乘积 | **负面**（去掉更好） |
| 邻居聚合（最近邻信息） | 非常重要 |
| 多层传播 | 重要 |
| 层间 Embedding 加权平均 | 重要 |

**LightGCN 的结论**：在推荐场景中，GCN 的有效性几乎完全来自于**邻域聚合（neighborhood aggregation）**，而非特征变换和非线性激活。

---

## 四、LightGCN 的极简公式

**传播规则**（去掉了所有"多余"组件）：

$$
e_u^{(k+1)} = \sum_{i \in \mathcal{N}_u} \frac{1}{\sqrt{|\mathcal{N}_u||\mathcal{N}_i|}} e_i^{(k)}
$$

$$
e_i^{(k+1)} = \sum_{u \in \mathcal{N}_i} \frac{1}{\sqrt{|\mathcal{N}_i||\mathcal{N}_u|}} e_u^{(k)}
$$

**只有归一化的邻居聚合，没有任何可学习的变换参数！**

**最终 Embedding（K 层加权平均）**：

$$
e_u = \sum_{k=0}^K \alpha_k e_u^{(k)}, \quad \alpha_k = \frac{1}{K+1}
$$

$$
e_i = \sum_{k=0}^K \alpha_k e_i^{(k)}
$$

**预测**（内积）：

$$
\hat{y}_{ui} = e_u^T e_i
$$

**训练**（BPR 损失）：

$$
\mathcal{L}_{\text{BPR}} = -\sum_{(u,i,j)\in\mathcal{O}} \ln \sigma(\hat{y}_{ui} - \hat{y}_{uj}) + \lambda \|E^{(0)}\|^2
$$

唯一需要学习的参数：**第 0 层的 Embedding 矩阵** $E^{(0)}$

---

## 五、LightGCN 的矩阵形式

LightGCN 可以用简洁的矩阵乘法表示，便于高效实现：

$$
E^{(k+1)} = \tilde{A} E^{(k)}
$$

$$
\tilde{A} = D^{-1/2} A D^{-1/2}
$$

其中：
- $A$ 是用户-物品二部图的邻接矩阵
- $D$ 是度矩阵（归一化用）

**最终 Embedding**：

$$
E = \frac{1}{K+1} \sum_{k=0}^K \tilde{A}^k E^{(0)} = \frac{1}{K+1} (I + \tilde{A} + \tilde{A}^2 + ... + \tilde{A}^K) E^{(0)}
$$

---

## 六、实验结果

在 Gowalla、Yelp2018、Amazon-Book 数据集上（K=3层）：

| 模型 | Recall@20 | NDCG@20 |
|------|-----------|---------|
| MF-BPR | 0.1547 | 0.1175 |
| NGCF | 0.1570 | 0.1327 |
| **LightGCN** | **0.1830** | **0.1554** |

LightGCN 以**更简单的模型**取得了**显著更好的性能**。

---

## 七、三篇论文的统一主题：从复杂到精准

| 论文 | 年份 | 核心洞察 | 哲学 |
|------|------|---------|------|
| DIN | 2018 | 用注意力机制聚焦相关历史行为 | 候选感知的动态用户建模 |
| BERT4Rec | 2019 | 双向序列建模捕捉全局上下文 | 序列中的上下文依赖 |
| LightGCN | 2020 | 去除 GCN 中无效组件 | 极简即是极致 |

这三篇论文代表了推荐系统研究的三个重要维度：
- **DIN**：如何更好地建模**用户行为与候选物品的交互**
- **BERT4Rec**：如何更好地建模**行为序列的时序结构**  
- **LightGCN**：如何更好地利用**用户-物品图结构**

---

*全系列完结。推荐系统30年：从"口味相似的人互相帮助"（GroupLens 1994）到"图上的轻量消息传递"（LightGCN 2020），不变的是理解用户需求的执念，变化的是工具的精妙程度。*
