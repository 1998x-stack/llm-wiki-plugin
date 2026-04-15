# 第十八篇：Informer——解锁超长序列预测的 ProbSparse 注意力
> **论文原名**：*Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting*  
> **作者**：Haoyi Zhou 等（贝航、北航、清华等）  
> **发表年份**：2021 年  
> **发表会议**：*AAAI 2021（最佳论文奖 Outstanding Paper Award）*

---

## 一、历史背景：标准 Transformer 的长序列瓶颈

Transformer（2017）在 NLP 中取得了革命性成功，研究者们自然希望将其迁移到时间序列预测——尤其是**超长序列预测（Long-Sequence Time-Series Forecasting, LSTF）**：

- 电力消耗预测：用过去 720 小时（30天）数据，预测未来 720 小时
- 交通流量预测：用过去一个月，预测未来一个月
- 天气预报：用过去 2 周，预测未来 2 周

但标准 Transformer 有两个致命的性能瓶颈：

1. **注意力的 $O(L^2)$ 空间和时间复杂度**：当序列长度 $L = 720$，注意力矩阵有 $720^2 \approx 52$ 万个元素；$L = 5000$ 时更是难以承受
2. **解码器的逐步解码（Step-by-step）**：NLP 中解码器一次生成一个 token，用于预测序列则需要 $h$ 次前向传播，效率极低

Zhou 等人的 Informer 通过三个核心创新同时解决了这两个问题。

---

## 二、核心创新一：ProbSparse 自注意力（$O(L \log L)$）

### 2.1 注意力的稀疏性观察

标准注意力矩阵 $\mathbf{A} = \text{Softmax}(\mathbf{Q}\mathbf{K}^{\top}/\sqrt{d})$ 在时序数据中往往**高度稀疏**——大部分 Query 的注意力权重几乎均匀分布在所有 Key 上（接近均匀分布），只有少数"关键 Query"才有显著集中的注意力（对特定 Key 权重很高）。

这一观察的理论依据：注意力权重的分布可以用 KL 散度衡量其与均匀分布的距离（"稀疏性"）：

$$M(q_i, K) = \ln \sum_{j=1}^{L} e^{q_i k_j^{\top}/\sqrt{d}} - \frac{1}{L}\sum_{j=1}^{L} \frac{q_i k_j^{\top}}{\sqrt{d}}$$

$M$ 值大的 Query 对应"活跃"的注意力（对预测有实质贡献），$M$ 值小的对应"懒惰"的注意力（几乎等价于均匀聚合）。

### 2.2 ProbSparse 机制

**ProbSparse 注意力**只为少数"活跃 Query"计算完整注意力，其余 Query 用均匀聚合代替：

1. 对每个 Query $q_i$，**随机采样 $u = O(\ln L)$ 个 Key** 计算 $M(q_i, K)$ 的近似值
2. 选出 $M$ 值最大的前 $u = O(\ln L)$ 个 Query 为"活跃 Query"
3. 只对活跃 Query 计算完整 $L$ 个 Key 的注意力
4. 非活跃 Query 的输出直接用值（Value）的均值代替

**复杂度分析**：
- 每个 Query 采样 $O(\ln L)$ 个 Key：总计 $O(L \ln L)$ 次操作
- 对 $O(\ln L)$ 个活跃 Query 计算完整注意力：$O(L \ln L)$ 次操作
- **总计：$O(L \ln L)$ 时间和空间复杂度**（相比标准的 $O(L^2)$）

当 $L = 720$：$L^2 = 518400$，$L\ln L \approx 720 \times 6.6 \approx 4752$，约节省 **109 倍**计算量。

---

## 三、核心创新二：编码器的自注意力蒸馏（Distilling）

Informer 编码器采用**分层自注意力蒸馏**结构：每层之后对序列长度做 $1/2$ 的 MaxPool 下采样，使得：
- 第 1 层：序列长度 $L$
- 第 2 层：长度 $L/2$
- 第 3 层：长度 $L/4$
- ……

这一设计使得随着层数加深，自注意力的计算复杂度指数下降，而高层可以捕捉更长范围的依赖关系（在更短的序列上计算注意力，每个"Token"代表了更长的时间窗口）。

**总内存复杂度**（$J$ 层堆叠）：$O((2-\varepsilon)L\ln L)$——因为几何级数求和的等比性，总复杂度仍为 $O(L\ln L)$。

---

## 四、核心创新三：生成式解码器（Generative Decoding）

标准 Transformer 解码器采用"自回归"方式：每次生成一个 Token，需要 $O(h)$ 次前向传播预测 $h$ 步。

Informer 的**生成式解码器**将预测未来 $h$ 步的问题转化为**单次前向传播**：

1. 解码器输入 = [历史序列的最后 $L_\text{token}$ 步（作为上下文）] + [$h$ 步的"占位符"（全零或均值）]
2. 解码器通过稀疏注意力和交叉注意力**一次性**生成所有 $h$ 步的预测值
3. 前向传播次数从 $O(h)$ 降为 $O(1)$

这一设计将多步预测的时间复杂度从 $O(hL^2)$ 降至 $O(L\ln L)$，使得数百步的预测在毫秒级内完成。

---

## 五、整体架构对比

```
标准 Transformer 预测架构（LSTF 场景）：
  输入序列 L → 编码器（O(L²)） → 上下文 → 自回归解码器（×h 次）

Informer：
  输入序列 L → 多层蒸馏编码器（O(L log L)）→ 上下文
                                           ↓
  [历史尾段 + h步占位符] → 生成式解码器（O(L log L)，一次前向）→ h步预测
```

---

## 六、实验数据集与基准比较

Informer 在论文中引入了两个成为后续时序 Transformer 标准基准的数据集：

**ETT（Electricity Transformer Temperature）**数据集：
- **ETTh1, ETTh2**：小时级，覆盖 2016—2018 年，7 个变量（油温 + 6 个负荷）
- **ETTm1, ETTm2**：15 分钟级，同一数据的更高频版本

在 ETT 数据集上，Informer 报告的 LSTF 预测误差比 LSTM、LSTMa（带注意力）、Reformer 等方法低 **20%—50%**，同时运行时间快数倍到数十倍。

---

## 七、争议与后续再评估

Informer 荣获 AAAI 2021 最佳论文后，迅速成为时序领域最被引用的论文之一。但随后的研究揭示了一些问题：

**Zeng et al.（2023，DLinear 论文）**对 Informer 的重新评估：
- 在相同的 ETT 数据集上，一个**单层线性模型**（DLinear）可以超越 Informer 及其后继者
- Informer 的改进部分来自与 LSTM 等非 Transformer 基准的对比，若与调优的线性模型对比，优势大幅缩减

**Wu et al.（2022，Autoformer 论文）**的改进：
- 在 Informer 的稀疏注意力基础上进一步引入序列分解和自相关机制，在多个数据集上超越 Informer

这些反思的结果并非否定 Informer，而是推动了领域对以下问题的深入探讨：
- 如何设计更合理的时序预测基准？
- Transformer 在时序中应该如何使用才能发挥其优势？
- 什么样的归纳偏置对时序预测最有价值？

---

## 八、影响与遗产

无论后续争议如何，Informer 的历史贡献不可忽视：

1. **打开了长序列 Transformer 预测的研究方向**：此前工作主要关注短预测（≤48 步），Informer 将目标推至 720 步乃至更长
2. **引入了标准基准数据集**：ETT 系列数据集成为后续几乎所有时序 Transformer 论文的标准评测集
3. **激发了一波改进工作**：Autoformer（2021）、FEDformer（2022）、PatchTST（2023）等均以 Informer 为起点

---

## 九、小结

Zhou 等（2021）的 Informer 解决了将 Transformer 用于长序列时序预测的关键工程障碍：

> **ProbSparse 注意力 + 自注意力蒸馏 + 生成式解码，将时间和空间复杂度从 $O(L^2)$ 降至 $O(L \log L)$，解锁了数百步的超长序列预测。**

三大工程贡献：
1. **ProbSparse**：识别"活跃 Query"，只对关键位置做完整注意力计算
2. **分层蒸馏**：编码器逐层下采样，高效处理超长输入
3. **生成式解码**：单次前向传播直接生成全部预测步，消除自回归解码的时间代价

---

*下一篇：Wu 等（2022）——Autoformer，在 Transformer 内嵌入序列分解与自相关机制，更好地利用时序的周期性结构。*
