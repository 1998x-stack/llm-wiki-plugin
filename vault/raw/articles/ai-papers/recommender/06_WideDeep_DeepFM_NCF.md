# 深度学习进入推荐系统：Wide & Deep · NCF · DeepFM

---

# 第一篇：Wide & Deep Learning (2016)

> **论文全名**：Wide & Deep Learning for Recommender Systems  
> **作者**：Heng-Tze Cheng et al. · Google  
> **发表**：DLRS@RecSys 2016  
> **应用**：Google Play 应用商店推荐  
> **引用量**：~8000+

---

## 一、记忆（Memorization）与泛化（Generalization）

Google 工程师们发现，推荐系统需要同时满足两种相互矛盾的需求：

### 记忆（Wide 部分的责任）

**含义**：记住哪些特征组合在历史数据中确实有效。

```
历史规律：用户安装了"鸟类识别"App后，大概率还会安装"望远镜"App
→ 这是一个具体的、强相关的规则，需要被精确记住
```

**实现**：逻辑回归（LR） + 人工特征工程的交叉特征

$$
y = w^T [x, \phi(x)] + b
$$

其中 $\phi(x)$ 是手工设计的特征交叉：

$$
\phi_k(x) = \prod_{i=1}^n x_i^{c_{ki}}, \quad c_{ki} \in \{0, 1\}
$$

**局限**：需要人工设计特征，无法发现数据中潜在的规律。

### 泛化（Deep 部分的责任）

**含义**：能够举一反三，将见过的规律推广到没见过的情况。

```
泛化能力：用户喜欢"户外活动"类 App
→ 即使这个用户从未安装过"登山路线"App，
   Deep 部分能推断出他可能喜欢（因为它与户外活动语义相关）
```

**实现**：Embedding + 多层 DNN

---

## 二、Wide & Deep 架构

```
             输出层（sigmoid/softmax）
                    ↑
          [Wide 分支] + [Deep 分支]
               ↑              ↑
          原始特征 +      Embedding 层
          交叉特征          ↓
                        [DNN 多层]
                           ↑
                       Dense 特征
```

**Wide 分支**（逻辑回归）：
- 输入：原始稀疏特征 + 手工交叉特征
- 作用：精确记忆强规则

**Deep 分支**（DNN）：
- 输入：所有特征的 Embedding（低维稠密向量）
- 结构：3层全连接（1024 → 512 → 256），ReLU 激活
- 作用：自动发现隐式特征交叉，泛化到未见组合

**联合训练（Joint Training）**：

$$
P(Y=1|x) = \sigma\left( w_{\text{wide}}^T [x, \phi(x)] + w_{\text{deep}}^T a^{(l_f)} + b \right)
$$

Wide 和 Deep 的输出共同加权，通过反向传播同时更新两套参数。

---

## 三、对 Google Play 推荐的影响

| 指标 | Wide only | Deep only | Wide & Deep |
|------|-----------|-----------|-------------|
| 获取率（App acquisitions） | 基线 | -1.0% | **+3.9%** |
| 在线实验（A/B Test） | — | — | 显著优于单独模型 |

**关键工程洞察**：
- Wide 部分特征需要领域专家设计（这是人工成本）
- Deep 部分能发现 Wide 遗漏的模式
- 两者互补，比单独任何一个都好

---

## 四、Wide & Deep 的历史地位

Wide & Deep 确立了工业推荐系统的**双塔思维**：

1. **记忆路径**（Wide/shallow）：高精度处理已知强规则
2. **泛化路径**（Deep）：从数据中自动学习隐式规律

这个框架此后演化为：

```
Wide & Deep (2016)
    ↓
DeepFM (2017): 用 FM 替换 Wide，消除手工特征
    ↓  
DCN (2017): Deep & Cross Network，显式多阶交叉
    ↓
xDeepFM (2018): Compressed Interaction Network
    ↓
AutoInt (2019): Attention-based 特征交叉
```

---

---

# 第二篇：DeepFM (2017)

> **论文全名**：DeepFM: A Factorization-Machine based Neural Network for CTR Prediction  
> **作者**：Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He · Huawei Noah's Ark Lab  
> **发表**：IJCAI 2017  
> **引用量**：~5000+

---

## 一、Wide & Deep 的缺陷

Wide & Deep 有一个明显缺陷：**Wide 部分需要人工特征工程**。

在 Google 这种有大量算法工程师的公司里还好，但对大多数团队来说，手工设计有效的特征交叉非常困难且耗时。

**DeepFM 的目标**：把 Wide & Deep 的 Wide 部分替换成 FM，从而：
- 消除手工特征工程
- 保持 Wide & Deep 的双路互补优势
- 实现端到端可训练

---

## 二、DeepFM 架构

**核心创新**：FM 和 DNN **共享同一组 Embedding**

```
         原始稀疏特征 x（one-hot/multi-hot）
                   ↓
              Embedding 层（所有字段共享）
             ↙                    ↘
    [FM 分支]                  [Deep 分支]
    FM 二阶交叉                DNN 多层网络
         ↘                    ↙
              输出层（相加 → sigmoid）
```

**FM 分支输出**：

$$
y_{\text{FM}} = w_0 + \sum_{i=1}^n w_i x_i + \sum_{i=1}^n \sum_{j=i+1}^n \langle \vec{v}_i, \vec{v}_j \rangle x_i x_j
$$

**Deep 分支输出**：

$$
y_{\text{Deep}} = \text{sigmoid}(W^{|H|} \cdot a^{|H|} + b^{|H|})
$$

**联合预测**：

$$
\hat{y} = \sigma(y_{\text{FM}} + y_{\text{Deep}})
$$

---

## 三、与 Wide & Deep 的关键区别

| 维度 | Wide & Deep | DeepFM |
|------|------------|--------|
| Wide 部分 | LR + 手工交叉特征 | FM（自动二阶交叉） |
| 特征工程 | 需要 | 不需要 |
| Embedding 共享 | 否（Wide/Deep 独立） | **是（FM/DNN 共享）** |
| 端到端训练 | 近似（Wide 独立预训练） | **完全端到端** |

Embedding 共享是 DeepFM 的一个重要优化：FM 分支训练的 Embedding，同时也被 DNN 分支使用，参数更新协同，信息流动更充分。

---

## 四、实验结果

在 Criteo（广告CTR）和公司内部数据集上：

| 模型 | AUC |
|------|-----|
| LR | 0.7751 |
| FM | 0.7890 |
| Wide & Deep | 0.7891 |
| **DeepFM** | **0.7920** |

DeepFM 在取消手工特征工程的同时，准确率还更高。

---

---

# 第三篇：NCF — Neural Collaborative Filtering (2017)

> **论文全名**：Neural Collaborative Filtering  
> **作者**：Xiangnan He, Lizi Liao, Hanwang Zhang, Liqiang Nie, Xia Hu, Tat-Seng Chua · NUS  
> **发表**：WWW 2017  
> **引用量**：~7000+

---

## 一、矩阵分解的根本局限

NCF 的出发点是对矩阵分解（MF）的一个根本性批判：

**MF 用向量内积建模用户-物品关系的假设太强。**

用一个反例说明：

```
用户向量空间（k=2维）：
  Alice = (0.7, 0.3)
  Bob   = (0.4, 0.8)
  Carol = (0.1, 0.2)

物品 i1, i2, i3 的真实偏好关系：
  Alice 最相似于 Carol
  Bob 最相似于 Carol
  Alice 和 Bob 相似性低
  
但在 2D 内积空间中，很难同时满足这三个关系——
内积空间的几何约束（三角不等式）会导致排序错误。
```

这说明：**内积（线性）无法表达用户-物品之间的复杂非线性关系。**

---

## 二、NCF 的解决方案：用 MLP 替代内积

**核心思路**：用多层感知机（MLP）学习用户向量和物品向量之间的任意非线性交互。

### 2.1 GMF（Generalized Matrix Factorization）

将内积改为 element-wise 乘积 + 线性层：

$$
\hat{y}_{ui} = \sigma(h^T (p_u \odot q_i))
$$

### 2.2 MLP 分支

将用户向量和物品向量拼接后，输入多层 MLP：

$$
z^{(1)} = \phi_1(p_u, q_i) = \begin{bmatrix} p_u \\ q_i \end{bmatrix}
$$

$$
z^{(L)} = \text{ReLU}(W^{(L)} z^{(L-1)} + b^{(L)})
$$

$$
\hat{y}_{ui}^{\text{MLP}} = \sigma(h^T z^{(L)})
$$

### 2.3 NeuMF（Neural Matrix Factorization）

将 GMF 和 MLP 结合（两个分支各自学习 Embedding）：

```
用户u ──────┬────────── 物品i
            │                │
       [GMF Emb]         [MLP Emb]
            │                │
    GMF element-wise    MLP 多层
         乘积              网络
            └────────┬───────┘
                    拼接
                     ↓
                  输出层
                     ↓
                  预测点击概率
```

$$
\hat{y}_{ui} = \sigma\left(h^T \begin{bmatrix} \phi_{\text{GMF}} \\ \phi_{\text{MLP}} \end{bmatrix}\right)
$$

---

## 三、NCF 的训练策略

### Pointwise Loss（BCE）

$$
\mathcal{L} = -\sum_{(u,i)\in\mathcal{Y}^+} \log \hat{y}_{ui} - \sum_{(u,j)\in\mathcal{Y}^-} \log(1-\hat{y}_{uj})
$$

负样本采样：每个正样本采样 4 个均匀负样本。

---

## 四、NCF 的实验与争议

### 原始实验结果

在 MovieLens 和 Pinterest 数据集上，NCF 显著优于：
- BPR + MF
- CDAE
- ItemKNN

### 后续争议（2019-2020年）

Dacrema et al. (RecSys 2019) 的复现研究发现：

> **"我们在7个数据集上复现了NCF，发现经过适当调参的传统基线（BPR-MF、P^3α、RP^3β）在多数情况下优于 NCF。"**

这引发了关于**深度学习推荐模型是否真正有效**的大讨论。

**主要争议点**：
1. 原始论文的基线实现和调参质量存疑
2. 隐式反馈数据集上的评估协议（负采样方式）影响巨大
3. 简单模型在充分调参后竞争力不弱

**NCF 的真实贡献**：
- 开创了"用神经网络替代内积"的思路，即使实验结论有争议
- 为后续 NGCF、LightGCN、BERT4Rec 等工作铺路
- 推动了推荐系统领域对**实验可复现性**的重视

---

## 五、三篇论文的统一视角

| 论文 | 时间 | 核心创新 | 工业影响 |
|------|------|---------|---------|
| Wide & Deep | 2016 | 记忆+泛化双路 | Google Play，确立双塔范式 |
| DeepFM | 2017 | FM+DNN共享Embedding | 华为，消除手工特征工程 |
| NCF | 2017 | MLP替代内积 | 启发图神经网络推荐研究 |

这三篇论文共同标志着：**推荐系统从"人工特征工程时代"全面进入"端到端深度学习时代"**。

---

*下一篇：[DIN (2018) — 阿里巴巴的注意力机制+用户行为建模]*
