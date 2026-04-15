# 论文精读 #09：Word2Vec
## Efficient Estimation of Word Representations in Vector Space
**作者：Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean | 2013 | Google**

---

## 🎯 一句话概括

> Word2Vec 用神经网络把每个词映射到一个稠密向量，让"国王 - 男人 + 女人 ≈ 女王"这样神奇的语义运算成为可能——它证明了语言中的语义关系可以被几何关系捕获，是整个现代 NLP（包括 BERT、GPT）的词向量基础。

---

## 🌍 时代背景：词的表示困境

### One-Hot 编码的致命缺陷

2013年前，词的标准表示是 **One-Hot 向量**：

```
词表大小 = 10000 个词

"猫" = [0, 0, 0, 1, 0, 0, ..., 0]  （第4位为1）
"狗" = [0, 0, 0, 0, 1, 0, ..., 0]  （第5位为1）
"汽车" = [0, 0, 1, 0, 0, 0, ..., 0] （第3位为1）
```

**三大缺陷：**

| 问题 | 描述 |
|------|------|
| **维度灾难** | 词表10万词 → 向量10万维，极度稀疏 |
| **语义盲区** | 猫和狗的余弦相似度 = 0，与汽车也 = 0，完全无法区分语义远近 |
| **泛化能力弱** | "猫咪"和"猫"在One-Hot里毫无关联 |

### 关键洞察：分布式假说

语言学家 Firth 在 1957 年说过：

> **"You shall know a word by the company it keeps."**（一个词由它的上下文决定）

Word2Vec 把这个语言学洞察变成了可计算的算法：**在相似上下文中出现的词，应该有相似的向量表示。**

---

## 💡 核心思想：两种训练模型

Word2Vec 提出了两种结构，本质都是"用上下文预测词，或用词预测上下文"：

### 模型一：CBOW（Continuous Bag of Words）

**用周围词预测中心词**

```
窗口大小 = 2，句子："我 喜欢 [吃] 北京 烤鸭"

输入（上下文词）：["我", "喜欢", "北京", "烤鸭"]
                      ↓ 词向量平均
                  上下文向量 h
                      ↓ 线性变换
                 输出 Softmax
                      ↓
              目标词："吃"（正确答案）
```

### 模型二：Skip-gram（跳字模型）

**用中心词预测周围词**（更常用，在小数据集上效果更好）

```
中心词："吃"
       ↓ 词向量
      v_吃
       ↓
预测窗口内每个位置的词：
  位置-2："我"
  位置-1："喜欢"
  位置+1："北京"
  位置+2："烤鸭"
```

**Skip-gram 数学目标：**

$$\max \sum_{t=1}^{T} \sum_{-c \leq j \leq c, j \neq 0} \log P(w_{t+j} | w_t)$$

$$P(w_O | w_I) = \frac{\exp(v'^{\top}_{w_O} v_{w_I})}{\sum_{w=1}^{W} \exp(v'^{\top}_w v_{w_I})}$$

---

## 🗺️ 词向量的神奇几何性质

训练完成后，词向量捕获了各种语义关系：

### 线性类比关系

```
king - man + woman ≈ queen
（国王向量 - 男人向量 + 女人向量 ≈ 女王向量）

China - Beijing + Tokyo ≈ Japan
（国家 - 首都 + 另一首都 ≈ 另一国家）

walking - walk + swim ≈ swimming
（进行时 - 原形 + 另一动词原形 ≈ 另一动词进行时）
```

**这说明词向量空间中存在规则的语义方向：**

```
向量空间中的"性别轴"：
woman - man ≈ queen - king ≈ actress - actor ≈ princess - prince

向量空间中的"时态轴"：
walking - walk ≈ swimming - swim ≈ running - run
```

### 聚类效应

```
相似的词自动聚集在一起：

动物类：cat, dog, rabbit, horse, pig...（紧密聚集）
国家类：China, USA, France, Germany...（紧密聚集）
动词类：run, walk, jump, swim...（紧密聚集）

类与类之间距离远，类内部距离近
```

---

## ⚡ 两大关键优化技术

原始 Softmax 计算所有词的概率分母，每次更新需要计算整个词表的分数（10万次乘法），极其缓慢。Word2Vec 提出两种加速方法：

### 优化一：Hierarchical Softmax（层次 Softmax）

把词表构建成一棵哈夫曼树，每次只需从根节点走到叶节点（约 $\log_2 V$ 步）：

```
              根节点
            /        \
          0.6        0.4
         /   \      /   \
       0.3   0.3  0.2   0.2
      /   \ /   \ /  \ / \
     猫   狗 人 树  车 飞机 ...
     
预测"猫"的概率 = 选左 × 选左 = 0.6 × 0.5 = 0.3
只需 log₂(10000) ≈ 13 步，而非 10000 步！
```

### 优化二：Negative Sampling（负采样）—— 最常用

不再计算所有词，每次只随机抽 k 个"负样本"（不应该出现的词），把多分类变成 k+1 个二分类：

**目标函数变为：**

$$\max \log \sigma(v'^{\top}_{w_O} v_{w_I}) + \sum_{i=1}^{k} \mathbb{E}_{w_i \sim P_n} [\log \sigma(-v'^{\top}_{w_i} v_{w_I})]$$

```
正样本："吃" 预测 "北京"  → 希望输出 1
负样本："吃" 预测 "火星"  → 希望输出 0
负样本："吃" 预测 "量子"  → 希望输出 0
负样本："吃" 预测 "宇宙"  → 希望输出 0

每次只更新 k+1 个词的参数，训练速度提升数百倍！
```

**负采样概率（高频词被多采样）：**

$$P(w_i) = \frac{f(w_i)^{3/4}}{\sum_j f(w_j)^{3/4}}$$

$3/4$ 次方是 Mikolov 经验调出来的，能平衡高频词和低频词。

---

## 🏗️ Word2Vec 的网络结构

极其简单（故意设计得轻量，以便处理海量数据）：

```
Skip-gram 网络（以 300 维向量为例）：

词表大小 V=10000，向量维度 d=300

词 w_I（中心词）
    ↓ One-Hot 查找
词向量矩阵 W_in (V×d = 10000×300)
    ↓ 得到 v_w ∈ ℝ^300
输出矩阵 W_out (d×V = 300×10000)
    ↓ 点积 v'^T · v_w
负采样输出（k+1 个二分类 Sigmoid）

参数量 = 2 × V × d = 2 × 10000 × 300 = 6,000,000
```

**关键**：输入矩阵 $W_{in}$ 的每一行就是对应词的词向量。

---

## 📊 实验结果

### 词类比测试（Semantic-Syntactic Word Relationship）

测试集包含 8869 个语义类比问题 + 10675 个语法类比问题：

| 模型 | 语义准确率 | 语法准确率 | 训练时间 |
|------|---------|---------|---------|
| NNLM | 34.3% | 64.5% | 数周 |
| RNN | 4.7% | 38.0% | 数周 |
| **Skip-gram (300d)** | **61.8%** | **61.8%** | **1天** |
| **CBOW (300d)** | **50.0%** | **53.3%** | **< 1天** |

**速度和准确率双赢！**

### 训练规模效应

```
词向量维度对准确率的影响（Skip-gram）：

维度  50: 44.9%
维度 100: 56.8%
维度 300: 61.8%  ← 论文常用
维度 600: 63.7%

更大维度：准确率更高，但训练更慢。300维是常见的工程平衡点。
```

---

## 💻 代码实现：从零到应用

### 方法一：使用 Gensim 训练中文词向量

```python
from gensim.models import Word2Vec
import jieba

# 准备语料（分词）
corpus = [
    "我喜欢吃北京烤鸭",
    "北京是中国的首都",
    "中国有很多美食",
    "烤鸭是北京的特色菜"
]

tokenized = [list(jieba.cut(sent)) for sent in corpus]

# 训练 Word2Vec
model = Word2Vec(
    sentences=tokenized,
    vector_size=100,    # 向量维度
    window=5,           # 上下文窗口
    min_count=1,        # 最低词频
    workers=4,          # 并行线程
    sg=1,               # 1=Skip-gram, 0=CBOW
    negative=10,        # 负采样数量
    epochs=100
)

# 保存模型
model.save("word2vec.model")

# 使用词向量
print(model.wv['北京'])  # 100维向量

# 找最相似的词
similar = model.wv.most_similar('北京', topn=5)
print("与'北京'最相似的词：", similar)

# 词类比：北京之于中国，东京之于？
result = model.wv.most_similar(
    positive=['东京', '中国'], 
    negative=['北京'], 
    topn=1
)
print("东京:日本 ≈ 北京:", result)
```

### 方法二：从零实现 Skip-gram + 负采样

```python
import torch
import torch.nn as nn
import numpy as np
from collections import Counter

class SkipGram(nn.Module):
    def __init__(self, vocab_size, embed_dim):
        super().__init__()
        # 中心词矩阵
        self.in_embed = nn.Embedding(vocab_size, embed_dim)
        # 上下文词矩阵
        self.out_embed = nn.Embedding(vocab_size, embed_dim)
        
        # 初始化
        nn.init.uniform_(self.in_embed.weight, -0.5/embed_dim, 0.5/embed_dim)
        nn.init.zeros_(self.out_embed.weight)
    
    def forward(self, center, context, neg_samples):
        """
        center:      (batch,) 中心词 ID
        context:     (batch,) 正样本上下文词 ID
        neg_samples: (batch, k) 负采样词 ID
        """
        # 中心词向量 (batch, dim)
        v = self.in_embed(center)
        
        # 正样本得分
        u_pos = self.out_embed(context)          # (batch, dim)
        pos_score = torch.sum(v * u_pos, dim=1)  # (batch,)
        pos_loss = -torch.log(torch.sigmoid(pos_score) + 1e-10)
        
        # 负样本得分
        u_neg = self.out_embed(neg_samples)           # (batch, k, dim)
        neg_score = torch.bmm(u_neg, v.unsqueeze(2))  # (batch, k, 1)
        neg_score = neg_score.squeeze(2)               # (batch, k)
        neg_loss = -torch.log(torch.sigmoid(-neg_score) + 1e-10).sum(dim=1)
        
        return (pos_loss + neg_loss).mean()
    
    def get_word_vector(self, word_id):
        """获取词向量（使用输入矩阵）"""
        return self.in_embed(torch.tensor(word_id)).detach().numpy()

# 训练示例
vocab_size = 10000
embed_dim = 300
model = SkipGram(vocab_size, embed_dim)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# 模拟一个 batch
center = torch.randint(0, vocab_size, (64,))
context = torch.randint(0, vocab_size, (64,))
neg = torch.randint(0, vocab_size, (64, 10))  # k=10 负样本

loss = model(center, context, neg)
optimizer.zero_grad()
loss.backward()
optimizer.step()
print(f"Loss: {loss.item():.4f}")
```

---

## 🌊 Word2Vec 的影响与遗产

### 直接影响：词向量时代

| 工作 | 改进方向 |
|------|---------|
| **GloVe (2014)** | 全局共现矩阵 + 词向量，效果更稳定 |
| **FastText (2016)** | 子词向量（字符n-gram），OOV词也能表示 |
| **Sense2Vec** | 多义词消歧词向量 |

### 间接影响：深度影响 NLP 范式

```
Word2Vec 的核心思想：
"用上下文预测目标，学习有意义的表示"

影响了：

BERT (2018)：
用 [MASK] 完形填空预训练 → 深度词表示

GPT (2018)：
用下一词预测预训练 → 生成能力

Doc2Vec / Sentence2Vec：
同样思想扩展到句子/文档级别

Node2Vec / Graph2Vec：
同样思想扩展到图节点/图结构
```

**"用上下文自监督学习表示"这个核心洞察，至今仍是大语言模型的根本原理。**

---

## 🎓 总结

| 维度 | 评价 |
|------|------|
| **历史地位** | ⭐⭐⭐⭐⭐ NLP 表示学习的里程碑 |
| **核心创新** | 高效学习稠密词向量，捕获语义关系 |
| **训练效率** | 数十亿词语料，几小时内训练完成 |
| **神奇属性** | king - man + woman = queen |
| **遗产** | BERT/GPT 等所有语言模型的词向量基础 |

> **一句话总结**：Word2Vec 把语言中每个词变成了数学空间中的一个点，让"语义距离"变得可以计算——"猫"和"狗"的向量相近，"猫"和"汽车"的向量相远，这个简单而深刻的洞察，成为了整个现代 NLP 的基石。

---
*⬇️ 下一篇：Dropout (2013) —— 最简单却最有效的正则化技巧*
