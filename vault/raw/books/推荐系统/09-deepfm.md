# DeepFM：用FM替代Wide，终结CTR预估中的手工特征工程

> 深度解读 DeepFM: A Factorization-Machine based Neural Network for CTR Prediction (IJCAI 2017)

---

## 1. 论文基本信息

| 项目 | 内容 |
|------|------|
| **标题** | DeepFM: A Factorization-Machine based Neural Network for CTR Prediction |
| **作者** | Huifeng Guo, Ruiming Tang, Yunming Ye, Zhenguo Li, Xiuqiang He |
| **机构** | 华为诺亚方舟实验室（Noah's Ark Research Lab, Huawei）/ 哈尔滨工业大学深圳研究生院 |
| **发表** | IJCAI 2017（第26届国际人工智能联合会议），pp. 1725-1731 |
| **arXiv** | [1703.04247](https://arxiv.org/abs/1703.04247) |
| **引用量** | 2700+ (截至2026年) |
| **扩展版** | [arXiv:1804.04950](https://arxiv.org/abs/1804.04950)（2018年扩展版，补充了在线A/B测试等内容） |

---

## 2. 一句话总结

**DeepFM将因子分解机（FM）与深度神经网络（DNN）整合为一个端到端模型，通过共享Embedding层同时学习低阶和高阶特征交互，彻底消除了Wide&Deep模型中对手工特征工程的依赖。**

这是一个极其精炼的改进思路：把Wide&Deep的"Wide"部分从需要人工设计cross-product特征的线性模型，替换为能够自动学习二阶特征交叉的FM，同时让FM和Deep共享同一套Embedding参数，实现真正的端到端训练。

---

## 3. 时代背景与问题

### 3.1 CTR预估为何重要

点击率（Click-Through Rate, CTR）预估是推荐系统和计算广告领域的核心任务。无论是搜索引擎的广告排序、电商平台的商品推荐，还是应用商店的App推荐，CTR预估的精度直接决定了平台的商业收入和用户体验。一个CTR模型AUC提升0.1%，在亿级流量的平台上可能意味着数百万美元的收入差异。

2017年前后，CTR预估领域正处于从传统机器学习向深度学习全面转型的关键时期。工业界的核心矛盾在于：**如何在不增加人工成本的前提下，让模型更好地学习特征之间的复杂交互关系**。

### 3.2 已有方案的不足

**逻辑回归（LR）**：作为最经典的CTR模型，LR的优势在于简单高效、可解释性强，但它完全依赖人工设计的特征交叉。工程师需要凭借领域经验手动构造诸如"用户安装的App x 曝光的App"这样的交叉特征，既费时又难以穷举所有有价值的组合。

**FM（Factorization Machines）**：Rendle在2010年提出的FM模型解决了特征交叉的自动化问题。通过为每个特征学习一个隐向量，FM能自动建模所有二阶特征交互。但FM的表达能力有限——它只能捕获二阶交互，对于更高阶的复杂模式无能为力。虽然理论上FM可以扩展到高阶，但计算复杂度会指数级增长，在实践中几乎不可行。

**FNN（Factorization-machine supported Neural Networks）**：FNN试图将FM与DNN结合，但采用的是"两阶段"训练策略——先用FM预训练Embedding，再将预训练好的Embedding作为DNN的初始化。这种串行方式存在两个问题：预训练阶段的FM能力受限于二阶交互，且预训练的Embedding可能不是DNN的最优初始化。

**Wide&Deep（Google, 2016）**：Google提出的Wide&Deep是一个里程碑式的工作，它将宽线性模型（Wide）和深度模型（Deep）联合训练，让模型同时具备记忆能力和泛化能力。但Wide部分依然需要人工设计cross-product特征。在Google的实践中，Wide部分的输入是"用户安装App x 曝光App"这样的手工交叉特征。这意味着Wide&Deep并没有真正解决特征工程的问题，只是将其限制在了Wide部分。

### 3.3 一个简洁的问题

所有这些方案的共同困境可以归结为一个问题：**要么依赖手工特征工程（LR、Wide&Deep），要么只能建模有限阶数的交互（FM），要么需要复杂的多阶段训练（FNN）。有没有一种模型，既不需要手工特征工程，又能同时学习低阶和高阶特征交互，还能端到端训练？**

---

## 4. 核心问题定义

DeepFM要解决的核心问题可以形式化表述为：

> **给定用户特征、物品特征和上下文特征的原始输入，如何设计一个端到端的神经网络架构，在不需要任何手工特征工程的情况下，同时有效地学习低阶（1阶、2阶）和高阶特征交互，最终输出准确的点击概率预估？**

这个问题有几个关键约束：

1. **无需手工特征工程**：模型的输入应该是原始特征，而不是人工构造的交叉特征。这是对Wide&Deep最核心的改进诉求。
2. **低阶与高阶兼顾**：模型需要同时捕获像FM那样的显式二阶交互，以及像DNN那样的隐式高阶交互。单一依赖任何一方都不够。
3. **端到端训练**：模型应该能够从原始输入到最终输出一步到位地训练，不需要FM预训练等额外步骤。
4. **工业可部署**：模型的训练效率和推理速度必须满足工业级在线服务的要求。

---

## 5. 核心方法详解

### 5.1 DeepFM整体架构

DeepFM的架构简洁而优雅，由两个并行的组件构成：

- **FM组件**：负责建模一阶特征重要性和二阶特征交互（低阶部分）
- **Deep组件**：负责建模高阶特征交互（高阶部分）

两个组件共享同一个Embedding层，最终的输出是两个组件输出的加和，经过Sigmoid函数得到CTR预估值：

$$\hat{y} = \text{sigmoid}(y_{FM} + y_{DNN})$$

这个架构的核心思想是"分而治之"：用专门擅长二阶交互的FM处理低阶部分，用擅长捕获复杂非线性关系的DNN处理高阶部分，然后通过加法融合。

### 5.2 FM组件详解

FM组件的数学形式如下：

$$y_{FM} = \langle w, x \rangle + \sum_{i=1}^{d}\sum_{j=i+1}^{d} \langle V_i, V_j \rangle \cdot x_i \cdot x_j$$

其中第一项 $\langle w, x \rangle$ 是一阶线性项，建模每个特征独立的重要性；第二项是二阶交叉项，通过隐向量的内积 $\langle V_i, V_j \rangle$ 来建模任意两个特征之间的交互强度。

FM的精妙之处在于它对二阶项的化简。直接计算所有特征对的交互复杂度为 $O(kn^2)$，但通过数学变换可以化简为 $O(kn)$：

$$\sum_{i=1}^{d}\sum_{j=i+1}^{d} \langle V_i, V_j \rangle \cdot x_i \cdot x_j = \frac{1}{2}\sum_{f=1}^{k}\left[\left(\sum_{i=1}^{n} v_{i,f} x_i\right)^2 - \sum_{i=1}^{n} v_{i,f}^2 x_i^2\right]$$

在DeepFM的实现中，FM的二阶交叉项不会被完全求和为一个标量——它保留了K维向量（K为Embedding维度），与一阶项拼接后共同构成FM组件的输出。

### 5.3 Deep组件详解

Deep组件是一个标准的前馈神经网络（MLP），用于捕获高阶特征交互。

首先，所有特征的Embedding向量被拼接成一个稠密向量 $a^{(0)} = [e_1, e_2, ..., e_m]$，作为DNN的输入。然后经过多层全连接变换：

$$a^{(l+1)} = \sigma(W^{(l)} \cdot a^{(l)} + b^{(l)})$$

其中 $\sigma$ 是ReLU激活函数，$W^{(l)}$ 和 $b^{(l)}$ 分别是第 $l$ 层的权重矩阵和偏置向量。通过多层非线性变换，DNN能够隐式地学习任意阶的特征交互模式。

论文中使用了3层隐藏层，每层400个神经元，激活函数为ReLU，dropout率为0.5。

### 5.4 共享Embedding层：DeepFM的灵魂

共享Embedding是DeepFM最核心的设计决策，也是它与Wide&Deep的根本区别。

在CTR预估场景中，输入特征通常是高维稀疏的类别特征。例如，一个用户ID可能是百万维one-hot向量中的一个。Embedding层将这些稀疏特征映射为低维稠密向量。

**DeepFM的关键创新在于：FM组件和Deep组件使用完全相同的Embedding层参数。** 也就是说，对于每个特征 $i$，它的Embedding向量 $V_i$ 同时被用于：

- FM组件中的二阶交互计算 $\langle V_i, V_j \rangle$
- Deep组件中拼接后输入DNN

这种共享设计带来了三重优势：

1. **参数效率**：Embedding层通常占据模型参数量的绝大部分（因为类别特征的维度极高），共享可以避免参数冗余。
2. **联合优化**：通过反向传播，FM的二阶交互信号和DNN的高阶交互信号可以共同优化Embedding，使得Embedding同时适配低阶和高阶学习。
3. **消除预训练**：不需要像FNN那样先用FM预训练Embedding再送入DNN，模型可以从随机初始化开始端到端训练。

### 5.5 与Wide&Deep的关键区别

将DeepFM与Wide&Deep放在一起对比，区别一目了然：

| 设计维度 | Wide&Deep | DeepFM |
|---------|-----------|--------|
| Wide部分 | LR + 手工cross-product特征 | FM（自动学习二阶交互） |
| 输入方式 | Wide和Deep各有独立输入 | FM和Deep共享Embedding输入 |
| 特征工程 | Wide部分需要手工设计交叉特征 | 完全不需要 |
| 低阶交互 | 依赖人工设计的质量 | FM自动学习所有二阶交互 |
| 训练方式 | 端到端，但Wide部分受限于手工特征 | 端到端，完全自动化 |

用一句话概括：**DeepFM = FM替代Wide中的LR + 共享Embedding消除独立输入 = 无需任何手工特征工程的Wide&Deep。**

---

## 6. 关键创新点

### 6.1 用FM替代Wide中的线性模型+Cross-product

这是DeepFM最直觉的创新。Wide&Deep的Wide部分本质上是一个线性模型，它依赖手工设计的cross-product特征来捕获记忆信息。而FM天然具备自动学习二阶交互的能力，用FM替代Wide部分后，低阶交互的学习从"人工"变成了"自动"。

这个替换看似简单，却产生了深远的影响：它使得模型对领域知识的依赖从"必须"变成了"可选"。工程师不再需要花费大量时间设计和筛选交叉特征，模型可以自动发现有价值的特征组合。

### 6.2 共享Embedding消除特征工程

共享Embedding的设计不仅仅是参数共享那么简单。它意味着FM和DNN在"看"同一个特征时，使用的是同一个表示。这使得FM学到的二阶交互信息可以通过Embedding传递给DNN，反之亦然。

更重要的是，共享Embedding使得模型的输入变得极其简单——只需要原始特征，不需要任何特征预处理或特征工程。这极大地降低了模型在工业部署中的维护成本。

### 6.3 端到端学习的整体框架

DeepFM实现了从原始特征到CTR预估的端到端学习。与FNN需要FM预训练、PNN*需要内积/外积预训练不同，DeepFM可以从随机初始化开始，通过梯度下降同时优化FM组件、Deep组件和共享Embedding的所有参数。这不仅简化了训练流程，还避免了多阶段训练中信息丢失的问题。

### 6.4 架构的一般性

DeepFM的框架具有很好的一般性。论文中提出了两个变体：

- **DeepFM-D**：Deep部分使用标准DNN
- **DeepFM-P**：Deep部分使用PNN（Product-based Neural Network）

这意味着DeepFM的"FM + Deep共享Embedding"框架可以灵活替换Deep部分的具体实现，是一个可扩展的架构范式。

---

## 7. 实验与验证

### 7.1 数据集

论文在两个数据集上进行了实验验证：

**Criteo数据集**：业界标准的CTR预估benchmark，包含4500万条用户点击记录，13个连续特征和26个类别特征。训练集和测试集按9:1比例划分。

**Company*数据集**：来自华为应用市场的真实数据，包含约10亿条记录，涵盖App特征（ID、类别、描述等）、用户特征（下载历史、设备信息等）和上下文特征（时间、网络状态等）。连续7天的数据用于训练，第8天的数据用于测试。

### 7.2 对比模型

论文与以下模型进行了全面对比：

- **LR**：逻辑回归（无特征交互）
- **FM**：因子分解机（仅二阶交互）
- **FNN**：FM预训练 + DNN
- **IPNN**：内积型PNN
- **OPNN**：外积型PNN
- **PNN***：内积+外积混合PNN
- **Wide&Deep**：Google的宽深模型（使用LR和FM两种Wide配置）

### 7.3 实验结果

DeepFM在两个数据集上都取得了最优性能：

**Criteo数据集**：
- AUC：0.8016（最优）
- LogLoss：0.44985（最优）

**Company*数据集**：
- AUC：0.8715（最优）
- LogLoss：0.02619（最优）

与次优模型相比，DeepFM在AUC上的提升超过0.25%-0.37%，所有提升的p值均小于10^-6，具有强统计显著性。

### 7.4 关键发现

论文通过消融实验得出了几个重要结论：

1. **特征交互确实重要**：不考虑特征交互的LR在所有模型中表现最差。
2. **低阶和高阶交互都不可或缺**：只考虑低阶交互的FM，或只考虑高阶交互的FNN/PNN，都不如同时考虑两者的DeepFM。
3. **共享Embedding效果显著**：与不共享Embedding的"LR & DNN"和"FM & DNN"相比，共享Embedding的DeepFM在AUC上提升了0.44%-0.48%，在LogLoss上降低了0.58%-0.80%。
4. **端到端训练优于预训练**：需要FM预训练的FNN表现不如端到端训练的DeepFM。

### 7.5 在线A/B测试

在2018年发表的扩展版论文中，作者补充了在华为应用市场（Huawei App Market）的在线A/B测试结果：**DeepFM-D相比精心调优的LR模型，在线CTR提升超过10%**。这是一个非常显著的业务收益，有力地证明了DeepFM在工业生产环境中的实用价值。

---

## 8. 局限性与不足

### 8.1 FM部分仍然只有二阶交叉

虽然DeepFM用DNN来补充高阶交互的学习，但FM组件本身仍然局限于二阶特征交叉。这意味着模型的"显式"低阶交互建模能力止步于二阶。虽然理论上FM可以扩展到更高阶，但由于计算复杂度的限制，实践中很少这样做。后续的xDeepFM（微软，2018）通过引入CIN（Compressed Interaction Network）来显式建模任意阶的向量级特征交互，正是为了解决这一局限。

### 8.2 Deep部分的隐式交叉难以解释

DNN通过多层非线性变换来学习高阶特征交互，但这种学习是完全隐式的"黑盒"过程。我们无法清楚地知道DNN究竟学到了哪些具体的高阶交互模式，也无法保证所有重要的高阶交互都被有效捕获。这对于需要可解释性的应用场景来说是一个不小的缺陷。AutoInt（2019）后来通过多头自注意力机制来解决这个问题，使得特征交互的学习过程更加透明。

### 8.3 暴力枚举所有特征对交互

FM组件会计算所有特征对之间的交互，没有选择性地关注更重要的交互。在特征数量很大时，大量不相关的特征对交互实际上是噪声，可能会稀释有价值的信号。AFM（Attentional Factorization Machines）通过引入注意力机制来为不同的特征交互赋予不同的权重，是对这一问题的改进方向。

### 8.4 缺乏时序动态建模

DeepFM将所有特征视为静态输入，没有考虑用户兴趣随时间变化的动态性。在真实推荐场景中，用户的点击行为往往受到近期行为序列的强烈影响。DIN（Deep Interest Network，阿里巴巴，2018）后来通过引入注意力机制来建模用户历史行为序列中与目标物品相关的部分，弥补了这方面的不足。

### 8.5 维度级交互而非向量级交互

DeepFM中DNN学习的是维度级（dimension-wise）的特征交互，即Embedding向量被展平后逐维度地进行全连接变换。这种方式丢失了Embedding向量内部的结构信息。xDeepFM提出的CIN在向量级（vector-wise）进行交互计算，保留了更丰富的特征信息。

---

## 9. 历史地位与影响

### 9.1 华为在推荐系统领域的代表作

DeepFM是华为诺亚方舟实验室在推荐系统领域最具影响力的工作之一。它不仅在学术界获得了广泛认可（2700+引用），更重要的是成功落地华为应用市场并取得了显著的业务收益。这使得华为在CTR预估的研究版图中占据了重要位置，与Google的Wide&Deep、阿里巴巴的DIN形成了三足鼎立之势。

### 9.2 CTR模型发展链中的关键一环

在CTR预估的模型演化史上，DeepFM扮演了承上启下的关键角色：

- **承上**：它继承了FM的自动特征交叉思想和Wide&Deep的双路并行架构
- **启下**：它开创了"自动特征交互 + DNN"的端到端范式，后续的DCN、xDeepFM、AutoInt都可以视为在这一范式上的延伸和改进

DeepFM的最大贡献不仅仅是一个具体的模型，更是一种设计理念的确立：**CTR模型应该能够自动学习特征交互，而不需要人工干预**。这个理念深刻影响了此后所有CTR模型的设计方向。

### 9.3 工业界的广泛采用

DeepFM因其简洁的架构和易于实现的特点，在工业界得到了广泛采用。许多公司的推荐系统都以DeepFM作为baseline或生产模型。开源框架如DeepCTR将DeepFM作为核心模型之一提供支持，进一步推动了它的普及。

---

## 10. 现代视角审视

### 10.1 CTR模型演化链

从历史发展的角度来看，CTR模型的演化脉络清晰可循：

```
LR (线性模型，无交互)
 |
 v
FM (2010, Rendle) -- 自动二阶交互，隐向量分解
 |
 v
FFM (2016, Juan et al.) -- 场感知，更精细的交互
 |
 v
Wide&Deep (2016, Google) -- 宽深并行，记忆+泛化
 |
 v
DeepFM (2017, Huawei) -- FM替代Wide，共享Embedding，无需特征工程  <-- 本文
 |
 +---> DCN (2017, Google) -- Cross Network显式交叉
 |
 +---> xDeepFM (2018, Microsoft) -- CIN向量级显式交叉
 |
 v
AutoInt (2019) -- 多头自注意力，可解释交互
 |
 v
DCN V2 (2020, Google) -- 矩阵核CrossNet + MoE
 |
 v
MaskNet, FinalMLP, GDCN... (2020s) -- 更多变体和改进
```

在这条演化链中，DeepFM处于一个关键的分叉点。它确立了"自动特征交互组件 + DNN"的标准范式，此后的模型主要在以下方向上进行改进：

- **交互方式**：从FM的内积交互，到DCN的Cross Network，到xDeepFM的CIN，到AutoInt的自注意力
- **交互阶数**：从DeepFM的显式二阶+隐式高阶，到DCN/xDeepFM的显式任意阶
- **可解释性**：从DNN的黑盒高阶交互，到AutoInt的可解释注意力权重

### 10.2 DeepFM在今天还有价值吗

答案是肯定的。虽然后续有许多更复杂的模型被提出，但多项独立的benchmark研究（如Zhu et al.的Open Benchmarking for CTR Prediction）发现，在标准数据集上，DNN、DeepFM、DCN和xDeepFM的性能差异实际上非常小（在Criteo数据集上AUC约为0.814左右）。这说明：

1. **简单模型往往足够好**：在充分调参和合理预处理的条件下，DeepFM这样的"较简单"模型并不比复杂模型差多少。
2. **工程实践中的性价比**：DeepFM的实现和维护成本远低于xDeepFM、AutoInt等模型，在追求稳定性和可维护性的工业场景中，DeepFM仍然是一个极具性价比的选择。
3. **作为baseline不可替代**：几乎所有CTR预估的研究论文都会将DeepFM作为必比较的baseline之一。

### 10.3 与现代大模型时代的关联

在2023-2026年大语言模型（LLM）席卷AI各领域的背景下，推荐系统也开始探索LLM的应用。但CTR预估场景的特殊性（超低延迟要求、极高吞吐量、结构化稀疏特征为主）决定了DeepFM式的轻量级模型在可预见的未来仍然是在线推理的主力。LLM更多扮演的是"特征增强器"或"冷启动辅助"的角色，而非替代传统CTR模型。

---

## 11. 通俗类比解读

### "点菜推荐员"的故事

想象你走进一家餐厅，服务员需要根据你的信息（你的口味偏好、用餐人数、时间、天气等）来推荐菜品。

**LR（逻辑回归）** 就像一个只看"单项信息"的服务员。他知道"喜欢辣的顾客倾向于点川菜"，但不会考虑"喜欢辣 + 夏天 = 可能想要冰镇酸辣粉"这样的组合信息。

**FM（因子分解机）** 像一个善于"两两联想"的服务员。他能想到"喜欢辣 + 夏天 = 酸辣冷面"，"人多 + 聚会 = 大菜"。但他的联想只停留在两两组合，不会想到"喜欢辣 + 夏天 + 女性顾客 + 朋友聚会 = 网红冰粉甜品"这样更复杂的推理。

**Wide&Deep** 像是两个服务员合作：一个经验丰富的老服务员（Wide）根据多年积累的"老顾客 + 招牌菜"固定搭配来推荐（但这些搭配需要餐厅经理手动整理），另一个年轻聪明的服务员（Deep）善于发现新规律。问题是，老服务员的"搭配清单"需要人工维护。

**DeepFM** 则是一个完美的解决方案：把老服务员换成一个自带"两两联想"能力的服务员（FM），他和那个聪明的年轻服务员（Deep）共享同一份顾客档案（共享Embedding），不需要经理手动整理任何搭配清单。FM负责发现"辣 + 夏天"这样的直觉搭配，Deep负责发现更深层的复杂模式，两人齐心协力给出最佳推荐。

**共享Embedding的精妙之处**在于：FM和Deep看到的是同一份"顾客画像"。FM在发现"这个顾客的口味偏好和季节因素有关联"时，这个认知会同步更新到Deep也在使用的画像中，反之亦然。两个组件通过共享的"认知基础"互相促进。

---

## 12. 金句摘录与点评

### 金句一：问题的精准诊断

> "Despite great progress, existing methods seem to have a strong bias towards low- or high-order interactions, or require expertise feature engineering."
>
> "尽管取得了巨大进展，现有方法似乎对低阶或高阶交互有很强的偏向性，或者需要专业的特征工程。"

**点评**：这句话精准地概括了2017年CTR预估领域的核心痛点。"strong bias"一词用得极好——不是说现有方法不行，而是说它们各有偏向。FM偏向低阶，DNN偏向高阶，Wide&Deep偏向依赖人工。DeepFM的目标就是消除这些偏向。好的研究往往始于对问题的精准诊断，DeepFM在这一点上做得非常出色。

### 金句二：架构设计的核心主张

> "Compared to the latest Wide & Deep model from Google, DeepFM has a shared input to its 'wide' and 'deep' parts, with no need of feature engineering besides raw features."
>
> "与Google最新的Wide&Deep模型相比，DeepFM的'宽'和'深'部分共享输入，除了原始特征外不需要任何特征工程。"

**点评**：这是全文最有分量的一句话。它用最简洁的语言阐明了DeepFM相对于Wide&Deep的两大核心改进：共享输入和无需特征工程。在学术写作中，能用一句话说清楚自己与最强baseline的区别，是一种很高的表达艺术。

### 金句三：实验设计的严谨性

> "DeepFM is the only model that requires no pre-training and no feature engineering, and captures both low- and high-order feature interactions."
>
> "DeepFM是唯一一个既不需要预训练也不需要特征工程，同时还能捕获低阶和高阶特征交互的模型。"

**点评**：这句话不仅是对DeepFM能力的总结，更是对所有对比模型的一次"降维打击"式定位。作者通过列举三个条件（无需预训练、无需特征工程、兼顾低高阶交互），巧妙地让其他所有模型都至少在一个维度上有所欠缺，从而凸显DeepFM的全面性。这种"设定评价维度让自己成为唯一满足者"的论证策略，值得学习。

### 金句四：工业验证的说服力

> "An online A/B test in Huawei App Market revealed that DeepFM-D leads to more than 10% improvement of click-through rate in the production environment, compared to a well-engineered LR model."
>
> "在华为应用市场的在线A/B测试中，DeepFM-D相比精心调优的LR模型，在生产环境中的点击率提升超过10%。"

**点评**：在CTR预估领域，离线AUC提升0.1%已经值得发论文，在线CTR提升1%就可以产生巨大商业价值。10%的在线CTR提升是一个极其惊人的数字，有力地证明了DeepFM不仅是学术上的创新，更是工业上的突破。这也解释了为什么DeepFM能够在工业界如此广泛地被采用。

---

## 参考资料

- [DeepFM 原始论文 (IJCAI 2017)](https://www.ijcai.org/proceedings/2017/0239.pdf)
- [DeepFM arXiv 版本](https://arxiv.org/abs/1703.04247)
- [DeepFM 扩展版 (arXiv 2018)](https://arxiv.org/abs/1804.04950)
- [Shaped: Mastering Feature Interactions - DLRM-Style Ranking Models](https://www.shaped.ai/blog/mastering-feature-interactions-a-deep-dive-into-dlrm-style-ranking-models-wide-deep-deepfm-etc)
- [Aman's AI Journal - Recommendation Systems Architectures](https://aman.ai/recsys/architectures/)
- [DeepCTR Documentation - Features & Benchmarks](https://deepctr-doc.readthedocs.io/en/latest/Features.html)
- [知乎: DeepFM原理推导](https://zhuanlan.zhihu.com/p/41439552)
- [xDeepFM: Combining Explicit and Implicit Feature Interactions (KDD 2018)](https://arxiv.org/abs/1803.05170)
