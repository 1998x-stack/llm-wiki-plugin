# 推荐系统的"GPT时刻"：万亿参数生成式推荐模型 HSTU 深度解读

> 论文全称：*Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations*

---

## 1. 论文基本信息

| 项目 | 内容 |
|------|------|
| **标题** | Actions Speak Louder than Words: Trillion-Parameter Sequential Transducers for Generative Recommendations |
| **作者** | Jiaqi Zhai, Lucy Liao, Xing Liu, Yueming Wang, Rui Li, Xuan Cao, Leon Gao, Zhaojie Gong, Fangda Gu, Michael He, Yinghai Lu, Yu Shi |
| **机构** | Meta (Facebook) |
| **发表** | ICML 2024 (Proceedings of the 41st International Conference on Machine Learning, PMLR 235:58484-58509) |
| **ArXiv** | [2402.17152](https://arxiv.org/abs/2402.17152) |
| **代码** | [github.com/meta-recsys/generative-recommenders](https://github.com/meta-recsys/generative-recommenders) |
| **关键词** | 生成式推荐、序列转导、Scaling Laws、万亿参数、HSTU、M-FALCON |

本文的作者团队横跨 Meta 内部多个核心部门，包括 MRS（Machine Recommendation Systems）、PyTorch、AI Infra、Discovery 和 Instagram 团队。这不是一篇纯学术实验论文，而是一项真正在数十亿用户规模上落地的工业级研究成果。

---

## 2. 一句话总结

**将推荐问题重新定义为序列生成任务，提出专为推荐场景设计的 HSTU 架构，构建出 1.5 万亿参数的生成式推荐模型（Generative Recommender），首次在工业级推荐系统中验证了类似 LLM 的 Scaling Laws，在线 A/B 测试提升 12.4%，并成功部署于拥有数十亿用户的平台上。**

---

## 3. 时代背景与问题

### 推荐系统的"老管道"困境

过去十年，工业级推荐系统几乎都遵循一个经典范式：**多阶段级联管道（Cascading Pipeline）**。以 YouTube 2016 年那篇里程碑式的论文为蓝本，整个行业形成了"召回 - 粗排 - 精排 - 重排"的标准架构：

1. **召回（Retrieval）**：从数十亿候选物品中快速筛选出数千个候选，通常使用双塔模型或倒排索引；
2. **粗排（L1 Ranking）**：用轻量模型将候选缩减到数百个；
3. **精排（L2 Ranking）**：用复杂模型（DLRM / DCN / DeepFM 等）对候选进行精细排序；
4. **重排（L3 / Value Model）**：根据业务策略做最终调整。

这个架构的核心问题在于：**每一层都是独立优化的**。召回层找到的好候选可能被排序层忽略，排序层给出的高分可能被重排层否决。各阶段由不同团队维护，端到端优化几乎不可能。

### DLRM 的 Scaling 瓶颈

更致命的是，传统 DLRM（Deep Learning Recommendation Model）**无法通过简单增加计算量来持续提升性能**。不像 LLM 领域中"模型越大、数据越多、效果越好"的 Scaling Laws，DLRM 在约 200B 参数量级就会出现性能饱和。无论是加深网络、增加特征交叉复杂度还是扩大 embedding 表，收益都趋于平坦。这与 GPT 系列"只要规模上去效果就上去"的优雅规律形成了鲜明对比。

### LLM 的启示

2020 年以来，大语言模型的成功建立在一个关键观察之上：**Scaling Laws**。OpenAI 在 2020 年的论文中发现，模型质量随计算量呈幂律（power-law）关系增长，这一发现直接催生了 GPT-3、GPT-4 等模型。同样的规律在视觉领域（ViT、DINO）也得到了验证。

那么，一个自然的问题浮现出来：**推荐系统能否找到自己的 Scaling Laws？推荐系统的"GPT 时刻"是否已经到来？**

Meta 的研究者们用这篇论文给出了一个掷地有声的答案。

---

## 4. 核心问题定义

本文要解决的核心问题可以分解为三个层次：

**第一，范式转换**：能否将推荐问题从"多阶段分类/排序"范式转换为"端到端序列生成"范式？传统 DLRM 的本质是对大量手工特征做分类预测，而 LLM 的本质是对 token 序列做自回归生成。作者的核心假设是：如果把用户的每一次交互（浏览、点击、停留、购买）看作一个 token，推荐问题就可以被重新定义为"预测用户下一个交互 token"的序列生成任务。

**第二，架构设计**：标准的 Transformer 架构并不适合推荐场景。推荐数据有三个独特特征：(a) 超高基数（cardinality）——物品和特征的取值范围可达数十亿；(b) 非平稳性（non-stationarity）——用户兴趣和物品分布持续变化；(c) 异构性（heterogeneity）——每次交互包含多种不同类型的特征。如何设计一个针对这些特征优化的架构？

**第三，工业可行性**：如何让万亿参数的模型在生产环境中以可接受的延迟和成本运行？Meta 的推荐系统每天需要处理数百亿次用户交互，推理延迟要求在毫秒级别。

---

## 5. 核心方法详解

### 5.1 Generative Recommender（GR）：重新定义推荐

GR 的核心思想是将推荐问题建模为**序列转导（sequential transduction）任务**。具体来说：

- 用户的历史行为被表示为一个时间序列 $\{(c_1, a_1), (c_2, a_2), \ldots, (c_t, a_t)\}$，其中 $c_i$ 是内容 token（用户交互的物品），$a_i$ 是动作 token（交互类型——点击、停留、购买等）；
- **召回**被建模为预测下一个内容 token $c_{t+1}$；
- **排序**被建模为预测下一个动作 token $a_{t+1}$（给定候选内容后，预测用户会有什么样的互动行为）；
- 通过这种方式，**召回和排序被统一到一个模型中**。

这种设计的代价是序列长度翻倍（每次交互对应 2 个 token），但换来的是架构上的极大简化——不再需要独立的召回模型和排序模型。

### 5.2 HSTU 架构：为推荐而生的 Transformer

HSTU（Hierarchical Sequential Transduction Unit）是本文最核心的技术贡献。它不是简单地把标准 Transformer 用在推荐上，而是针对推荐场景的特殊性做了一系列深思熟虑的架构改造。

**HSTU 的每一层包含三个子层：**

**(1) 逐点投影（Pointwise Projection）**

输入 $X$ 通过线性变换生成四组张量：查询（Q）、键（K）、值（V）和门控（U）。与标准 Transformer 的 QKV 三元组相比，HSTU 多引入了一个 $U$ 矩阵。这个 $U$ 矩阵的作用是作为门控信号，允许模型在不同层级学习特征交互的层次结构。

**(2) 空间聚合（Spatial Aggregation）——无 Softmax 的注意力**

这是 HSTU 与标准 Transformer 最显著的区别。注意力分数的计算公式为：

$$A(X)V(X) = \phi_2(Q(X)K(X)^\top + \text{relative\_attention\_bias}) \cdot V(X)$$

其中 $\phi_2$ 是 **SiLU 激活函数**而非 Softmax。这个设计选择背后有深刻的推荐领域洞察：

- **保留强度信息**：在推荐场景中，用户与某类物品交互的次数本身就是一个强特征，反映了偏好强度。Softmax 会将注意力分数归一化到 [0, 1] 区间，从而丢失这种"强度"信息。SiLU 则不做归一化，保留了原始的数值规模。
- **适应非平稳分布**：推荐数据的词汇表（物品集合）是持续变化的——新物品不断上线，旧物品不断下架。Softmax 对这种分布漂移不够鲁棒，而逐点激活更加灵活。

为了训练稳定性，在逐点聚合之后添加了 Layer Norm。消融实验证实，将 SiLU 替换为 Softmax 会导致性能下降。

**(3) 逐点变换（Pointwise Transformation）——门控特征交互**

$$Y(X) = f_2(\text{Norm}(A(X)V(X)) \odot U(X))$$

通过 Hadamard 乘积（逐元素相乘）将注意力聚合结果与门控信号 $U$ 结合。这种门控机制让模型能够动态控制不同特征交互的贡献，类似于 LSTM 中门控机制的作用。

**其他关键设计选择：**

- **相对注意力偏置替代位置编码**：HSTU 不使用传统的绝对位置编码，而是将位置信息和时间信息（距离当前的时间间隔）作为相对注意力偏置直接注入注意力分数计算中。这既编码了序列的顺序关系，也编码了交互的时间间隔——后者在推荐中极为重要（一小时前的点击和一个月前的点击有本质不同）。
- **因果掩码（Causal Masking）**：采用单向注意力，每个位置只能关注之前的位置，确保自回归生成的合法性。
- **精简架构**：将注意力外的线性层从 6 个减少到 2 个，并激进地融合计算操作，大幅降低激活内存占用。

### 5.3 特征序列化

HSTU 将传统 DLRM 中的异构特征空间（用户画像、物品属性、上下文信息等）**全部序列化为 token 序列**。每个特征被表示为序列中的一个辅助事件。论文证明，当序列长度趋于无穷时，这种序列化表示可以逼近完整的 DLRM 特征空间。

这意味着 HSTU 不再需要复杂的手工特征工程——只需要原始的用户行为日志，每个 token 只需一个 ID 特征和少量业务属性。

### 5.4 M-FALCON：高效推理

M-FALCON（Microbatched-Fast Attention Leveraging Cacheable OperatioNs）是论文提出的高效推理算法，解决了"万亿参数模型如何在毫秒级延迟内完成推理"的工程挑战。

M-FALCON 的核心思路是：

1. **KV 缓存复用**：用户历史序列的 KV 缓存可以在编码阶段完成后缓存下来，对所有候选物品共享复用；
2. **微批处理（Micro-batching）**：将候选物品分成小批次，通过修改注意力掩码防止候选之间信息泄露，同时共享历史序列的计算；
3. **计算摊销**：通过上述设计，推理成本随候选数量线性增长而非二次增长。

最终效果：M-FALCON 使得 **285 倍复杂度的模型可以在相同的推理预算下运行**，同时实现 1.5x-2.99x 的吞吐量提升。

### 5.5 Scaling Laws

本文最令人振奋的发现之一：**推荐系统也存在 Scaling Laws**。

具体来说，GR 模型的质量（以 NDCG 等指标衡量）随训练计算量（FLOPs）呈**幂律关系增长**，跨越三个数量级，从小型模型一直扩展到 GPT-3/LLaMA-2 规模。这意味着：

- 如果你有更多的 GPU，就能训练更好的推荐模型；
- 未来模型的效果可以被提前预测——不需要每次都训练完整规模的模型来评估效果；
- 推荐系统领域的"基础模型（Foundation Model）"成为可能。

相比之下，传统 DLRM 在约 200B 参数后就出现了性能饱和，无法继续受益于更多的计算资源。

### 5.6 部署规模

论文报告的部署规模令人印象深刻：

- **模型参数**：1.5 万亿（1.5 Trillion）
- **训练数据**：1000 亿个样本
- **训练硬件**：256 块 H100 GPU 集群
- **部署平台**：Meta 旗下多个产品线（涉及数十亿用户）
- **日均处理**：数百亿次用户交互

---

## 6. 关键创新点

### 创新一：推荐系统的 Scaling Laws

这是本文最具历史意义的贡献。在此之前，推荐系统领域一直没有找到类似 NLP/CV 领域的 Scaling Laws，模型规模的增长带来的收益有限且不可预测。本文首次在工业级推荐系统中验证了幂律 Scaling Laws 的存在，这为推荐领域的"基础模型"路线提供了理论和实验基础。

### 创新二：万亿参数模型的工业部署

学术界讨论万亿参数模型并不稀奇，但真正在生产环境中部署并持续运行的万亿参数推荐模型，这是第一个。M-FALCON 算法使得这一部署在经济上可行——通过微批处理和 KV 缓存，推理成本被控制在传统 DLRM 的预算范围内。

### 创新三：用生成范式统一召回和排序

传统架构中，召回和排序是两个完全不同的任务，使用不同的模型和优化目标。GR 通过将两者都建模为"预测下一个 token"的生成任务，实现了真正的端到端统一。这不仅简化了系统架构，还消除了级联管道中各阶段之间的信息损失。

### 创新四：HSTU 针对推荐场景的架构优化

HSTU 不是简单的"Transformer + 推荐数据"，而是从注意力机制（去掉 Softmax）、位置编码（相对偏置）、门控机制（额外的 U 矩阵）等多个维度对推荐场景做了针对性设计。消融实验证明每个设计选择都是有价值的。

---

## 7. 实验与验证

### 7.1 离线实验

论文在合成数据和公开数据集上进行了广泛评估：

- **NDCG 提升**：HSTU 在公开数据集上相比基线模型提升高达 **65.8%**；
- **速度优势**：在 8192 长度序列上，HSTU 比基于 FlashAttention2 的标准 Transformer 快 **5.3x 到 15.2x**；
- **合成数据实验**：在控制变量的合成实验中，HSTU 与标准 Transformer 的性能差距高达 **44.7%**。

Scaling 曲线实验显示，在从小规模到 GPT-3/LLaMA-2 规模的三个数量级范围内，GR 模型质量始终遵循幂律增长关系，而传统 DLRM 在一定规模后趋于平坦。

### 7.2 在线 A/B 测试

在 Meta 内部多个产品线上的在线 A/B 实验结果：

- **主要参与指标（engagement metric）提升 12.4%**——这是一个在工业级推荐系统中极为惊人的提升幅度。作为参考，大多数推荐系统的模型升级如果能带来 0.5%-1% 的在线提升就被认为是显著的；
- **HR@100（召回率）**：从 29.0% 提升到 36.9%（约 27% 的相对提升）；
- 部署在拥有**数十亿用户**的平台上多个产品表面。

### 7.3 消融分析

论文进行了系统的消融实验来验证各设计选择的必要性：

- **SiLU vs Softmax**：将注意力函数从 SiLU 替换为 Softmax 导致性能下降，验证了逐点注意力对推荐场景的优越性；
- **门控机制**：移除 U 矩阵会降低模型的特征交互能力；
- **特征来源**：同时使用交互特征和内容特征效果最佳。仅用交互特征导致 2.6% 的性能下降，仅用内容特征导致 25.3% 的下降——这也呼应了论文标题"Actions Speak Louder than Words"。

---

## 8. 局限性与不足

### 8.1 计算成本

尽管 M-FALCON 大幅降低了推理成本，但 1.5 万亿参数模型的训练成本仍然是天文数字级别的。论文报告使用了 256 块 H100 GPU 的集群来训练，在 1000 亿样本上完成训练。这意味着只有少数拥有海量用户数据和顶级算力的科技巨头才能复制这一工作，中小企业几乎无法企及。

### 8.2 序列长度的二次增长

将每次交互编码为两个 token（内容 + 动作），使得用户序列长度翻倍，注意力计算的 FLOPs 增长四倍。尽管 HSTU 通过架构优化缓解了这一问题，但对于交互频率极高的用户（如每天数百次交互），序列长度仍然是一个挑战。后续工作（如 DFGR, Dual-Flow Generative Ranking Network）已经开始尝试通过双流机制来解决这个问题。

### 8.3 冷启动问题

作为一个高度依赖用户历史行为序列的模型，GR 天然面临冷启动挑战。对于新用户（没有或很少的行为历史），模型可用的序列极短，难以发挥出序列建模的优势。论文没有专门讨论冷启动场景下的解决方案。

### 8.4 可解释性

万亿参数的序列生成模型是一个典型的黑盒。与传统的基于特征的 DLRM 相比，GR 更难解释"为什么推荐了这个物品"。在合规性要求日益严格的环境下（如欧盟 DSA 法案要求解释推荐逻辑），可解释性的缺失可能成为部署障碍。

### 8.5 实验的可复现性

论文的主要实验结果基于 Meta 内部数据和系统，外部研究者难以完全复现。虽然 Meta 开源了代码，并在公开数据集上提供了部分实验，但万亿参数规模的训练和在线 A/B 实验无法在学术环境中再现。

---

## 9. 历史地位与影响

### 推荐系统的"GPT 时刻"

这篇论文被广泛认为是推荐系统领域的一个**范式转折点**。正如 GPT-3 证明了"规模就是一切"的语言模型路线，HSTU/GR 证明了推荐系统同样可以通过规模化获得持续的性能提升。Shaped.ai 的分析文章甚至直接以"Is this the ChatGPT moment for recommendation systems?"为标题来讨论这篇论文。

### 行业范式迁移

论文发表后，整个推荐系统行业开始加速向生成式推荐范式迁移。截至 2025-2026 年，Google、快手、美团、阿里巴巴、Netflix、小红书、字节跳动、腾讯、百度、京东等头部互联网公司都已开始探索或部署基于 HSTU 思想的生成式推荐系统。MLCommons 在 2026 年推出的 DLRMv3 基准测试直接将模型规模提升 20 倍（从 50GB 到 1TB），每候选计算量提升 6500 倍（从 40M FLOPs 到 260G FLOPs），明确受到了 HSTU Scaling Laws 的启发。

### 开源生态

Meta 开源了完整的 GR 代码库，NVIDIA 也在其 recsys-examples 仓库中提供了 HSTU 的工业级实现。后续工作如 HSTU-BLaIR 进一步将文本 embedding 集成到 HSTU 框架中。这些开源资源极大地降低了学术界和工业界的复现门槛。

### 对基础模型概念的拓展

Scaling Laws 的发现为推荐领域的"基础模型"铺平了道路。如果推荐模型的质量可以像 LLM 一样通过增加计算量来可预测地提升，那么训练一个通用的推荐基础模型、然后针对不同业务场景微调就变得可行——这将根本性地改变推荐系统的开发方式。

---

## 10. 现代视角审视

### 生成式推荐 vs 生成式 AI：殊途同归？

从更宏观的视角来看，HSTU/GR 代表的生成式推荐与 ChatGPT/GPT-4 代表的生成式 AI 有着惊人的相似性。两者都通过自回归序列建模来捕捉复杂的模式，都展现了 Scaling Laws，都通过统一的框架替代了此前碎片化的解决方案。

但也有关键的差异。生成式 AI 处理的是语言——一种高度结构化、语义丰富的信号。而推荐系统处理的是用户行为——一种噪声更大、非平稳性更强的信号。论文标题"Actions Speak Louder than Words"暗示了这种差异：在推荐场景中，用户的行为（actions）比文本描述（words）更能反映真实偏好。

### 规模竞赛的隐忧

万亿参数模型带来了令人瞩目的效果提升，但也引发了对算力军备竞赛的担忧。如果推荐系统的进步越来越依赖于计算规模，那么只有资源最丰富的公司才能保持竞争力，这可能加剧行业的马太效应。论文中 Scaling Laws 的另一层含义是：**碳足迹可以通过预测 Scaling 曲线来减少**——你不需要盲目地训练大模型来探索最优规模，而可以通过小规模实验预测大规模模型的表现。

### 端到端 vs 模块化

GR 的端到端设计是一把双刃剑。统一模型简化了系统架构，但也使得调试和迭代变得更加困难。传统管道中，你可以独立地改进召回层而不影响排序层。在 GR 中，任何改动都可能影响整个系统的行为。如何在端到端的优雅和模块化的灵活之间找到平衡，是这一范式面临的实际挑战。

---

## 11. 通俗类比解读

### 从流水线到智能工厂

想象你经营一家大型餐厅。传统推荐系统就像一条人工流水线：

- **采购部（召回）**：从市场上所有的食材中粗选出一批可能用得上的；
- **主厨助理（粗排）**：把食材筛选到更小的范围；
- **主厨（精排）**：精心搭配出几道菜的候选方案；
- **餐厅经理（重排）**：根据当日情况和商业考量做最终决定。

每个环节的人只看到自己负责的部分，采购部不知道主厨今天想做什么菜，主厨不知道经理最近在推什么促销活动。信息在传递中不断丢失。

**GR/HSTU 就像把整个流水线替换为一个 AI 智能工厂**。这个工厂有一个统一的大脑，它记住了每位顾客过去的每一次点餐——不仅是点了什么（内容 token），还包括吃了多少、停留了多久、是否打了好评（动作 token）。基于这些完整的记忆，它一步到位地决定应该给每位顾客推荐什么菜品。

更厉害的是，这个智能工厂有一个特性：**给它更多的计算芯片（GPU），它的推荐就会变得更精准**——而且提升幅度是可以预测的。这就像一个魔法公式：投入两倍的算力，就能获得固定比例的效果提升。传统的人工流水线做不到这一点——你加再多的人，到某个点之后效率就不再提升了。

**M-FALCON** 则像是这个智能工厂的调度系统。当它需要为一位顾客评估 1000 道候选菜品时，它不会为每道菜都从头思考一遍。相反，它先把顾客的完整用餐历史分析一次（KV 缓存），然后把 1000 道菜分成小组，共享这份分析结果来做评估。这就像主厨先了解顾客的口味画像，然后快速过一遍菜单——而不是每看一道菜都要重新回忆顾客的所有历史。

---

## 12. 金句摘录与点评

> **"Large-scale recommendation systems are characterized by their reliance on high cardinality, heterogeneous features and the need to handle tens of billions of user actions on a daily basis. Despite being trained on huge volume of data with thousands of features, most Deep Learning Recommendation Models (DLRMs) in industry fail to scale with compute."**

**点评**：开篇即直指要害——DLRM 的根本问题不是模型不够复杂或数据不够多，而是**无法通过增加计算量来持续提升**。这是整篇论文的立论基础。

---

> **"Actions Speak Louder than Words."**

**点评**：论文标题本身就是一句金句。它有双重含义：一是用户的行为（actions）比文本描述（words）更能反映其真实偏好，这是推荐系统与 NLP 的本质差异；二是模型应该直接从用户行为中学习，而非依赖于对物品的文本描述。消融实验验证了这一点——仅用内容特征会导致 25.3% 的性能下降，而仅用行为特征只下降 2.6%。

---

> **"The model quality of Generative Recommenders empirically scales as a power-law of training compute across three orders of magnitude, up to GPT-3/LLaMA-2 scale."**

**点评**：这可能是整篇论文中最重要的一句话。它意味着推荐系统终于找到了自己的 Scaling Laws。三个数量级的验证范围、与 GPT-3/LLaMA-2 的可比规模，给了这一发现足够的可信度。这句话为推荐领域的"基础模型"路线提供了关键的实证支持。

---

> **"HSTU-based Generative Recommenders, with 1.5 trillion parameters, improve metrics in online A/B tests by 12.4% and have been deployed on multiple surfaces of a large internet platform with billions of users."**

**点评**：12.4% 的在线提升在工业推荐系统中是一个近乎"异常"的数字。大多数工业团队为 0.1%-0.5% 的提升就会投入数月的工作。这个数字展示了范式转换（而非增量改进）所能带来的巨大红利。

---

> **"Through M-FALCON, we can serve 285x more complex GR models while achieving 1.50x-2.99x speedups, all with the same inference budget used by traditional DLRMs."**

**点评**：这句话解决了所有工程师心中的疑问——"万亿参数模型怎么上线？"。答案是：不仅能上线，而且在相同的推理预算下还能更快。285 倍的复杂度提升 + 吞吐量的提升，这是工程创新与算法创新结合的典范。

---

> **"We revisit fundamental design choices in recommendation systems [...] and reformulate recommendation problems as sequential transduction tasks within a generative modeling framework."**

**点评**：看似平淡的一句话，实则野心勃勃。"Revisit fundamental design choices"意味着对过去十年推荐系统架构的全面反思。"Reformulate"意味着这不是改良，而是重新定义问题本身。从多阶段分类到端到端生成，从特征工程到序列建模——这是一次彻底的范式革命。

---

**结语**：HSTU/GR 代表的不仅是一个新模型或新架构，更是推荐系统领域的一次根本性思维转变。它证明了：当我们勇于重新定义问题时，曾经被认为是行业天花板的限制可能瞬间消失。推荐系统的下一个十年，也许将由 Scaling Laws 驱动的生成式范式所主导。

---

**参考资料**：
- [论文原文 (ArXiv)](https://arxiv.org/abs/2402.17152)
- [ICML 2024 Proceedings](https://proceedings.mlr.press/v235/zhai24a.html)
- [官方开源代码 (GitHub)](https://github.com/meta-recsys/generative-recommenders)
- [NVIDIA HSTU 实现](https://github.com/NVIDIA/recsys-examples/blob/main/examples/hstu/README.md)
- [Is this the ChatGPT moment for recommendation systems? (Shaped.ai)](https://www.shaped.ai/blog/is-this-the-chatgpt-moment-for-recommendation-systems)
- [The Rise of Generative Recommenders (ML Frontiers)](https://mlfrontiers.substack.com/p/the-rise-of-generative-recommenders)
- [BaseModel vs HSTU (Synerise)](https://sair.synerise.com/basemodel-vs-meta-ais-hstu-for-sequential-recommendations/)
- [DLRMv3 Benchmark (MLCommons)](https://mlcommons.org/2026/02/dlrmv3-inference-meta/)
