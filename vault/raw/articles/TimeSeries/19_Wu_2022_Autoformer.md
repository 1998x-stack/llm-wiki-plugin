# 第十九篇：Autoformer——自相关 × 序列分解，让 Transformer 真正理解时序结构
> **论文原名**：*Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting*  
> **作者**：Haixu Wu 等（清华大学、微软亚洲研究院）  
> **发表年份**：2021 年（预印本）/ 2022 年（NeurIPS 2021 正式收录）  
> **发表会议**：*NeurIPS 2021*

---

## 一、历史背景：Informer 之后的深入反思

Informer（2021）通过稀疏注意力解决了计算瓶颈，但它对时间序列的处理方式仍然沿袭了 NLP 的逻辑——将时序中的每个时刻看作独立的"Token"，用注意力捕捉它们之间的点对点关系。

Haixu Wu 等人提出了一个更深刻的问题：

> **时间序列与 NLP 文本的根本区别在于——时序数据有固有的时间结构：趋势、季节周期。这种结构应该被显式地嵌入模型，而非期望 Transformer 从注意力矩阵中自动发现。**

基于这一洞察，Autoformer 提出了两个核心设计：
1. **序列分解（Decomposition）**：在模型内部每一层都进行趋势-季节分解
2. **自相关机制（Auto-Correlation）**：基于序列自相关函数（而非点对点注意力）捕捉周期性依赖

---

## 二、核心创新一：渐进式序列分解

### 2.1 经典分解的局限

传统时序分解（如 STL、X-11）是预处理步骤——在建模之前先分解，之后对各成分独立处理。这种分离式处理无法让分解与预测相互反馈。

Autoformer 将分解**嵌入到 Transformer 的每一层**：每个 Encoder 和 Decoder 块在处理序列后，立即将输出分解为趋势和季节两个成分，分别向后传递。

### 2.2 序列分解块（Series Decomposition Block）

使用**移动平均（Moving Average）**提取趋势：

$$\mathbf{X}_{\text{trend}} = \text{AvgPool}(\text{Padding}(\mathbf{X}), \text{kernel size} = k)$$

$$\mathbf{X}_{\text{seasonal}} = \mathbf{X} - \mathbf{X}_{\text{trend}}$$

其中：
- AvgPool：对每个时间点取以其为中心的 $k$ 步平均（等效于低通滤波器）
- Padding：在序列两端重复端点值（保持序列长度不变）
- 季节成分 = 原序列 - 趋势（高通滤波残差）

**为什么用移动平均而非更复杂的分解？**
- 计算简单，梯度可反向传播
- 可微分，与深度学习训练框架天然兼容
- 参数 $k$ 可以作为超参数调节（或通过多尺度分解取多个 $k$）

---

## 三、核心创新二：自相关机制（Auto-Correlation）

### 3.1 时序的周期性与自相关

时间序列的周期性反映在其**自相关函数（ACF）**中——序列与自身延迟 $\tau$ 个时刻的版本的相关性：

$$R_{XX}(\tau) = \frac{1}{T} \sum_{t=1}^{T-\tau} x_t \cdot x_{t+\tau}$$

若序列有周期 $p$，则 $R_{XX}(\tau)$ 在 $\tau = p, 2p, 3p, \ldots$ 处有显著峰值。

**关键洞察**：对于有周期结构的时间序列，"时刻 $t$"与"时刻 $t - \tau$"（$\tau$ 是周期整数倍）的关系，远比与任意随机时刻的关系更重要。标准注意力平等地计算所有 Query-Key 对，忽略了这一结构。

### 3.2 自相关注意力的计算

Autoformer 将 Query、Key、Value 序列（均为 $L \times d$ 维）：

**第一步：用 FFT 计算自相关**

$$\text{AutoCorr}(\tau) = \text{IFFT}(\text{FFT}(Q) \cdot \overline{\text{FFT}(K)})$$

（利用 FFT 的卷积定理，自相关函数可以在 $O(L \log L)$ 内计算，避免了 $O(L^2)$ 的直接计算）

**第二步：选取 Top-$k$ 周期滞后**

从 $\text{AutoCorr}(\tau)$ 中找出 $k = O(\log L)$ 个最大的滞后 $\tau_1, \tau_2, \ldots, \tau_k$（对应最显著的周期）。

**第三步：聚合（Roll + Aggregate）**

$$\hat{X} = \sum_{i=1}^{k} \text{softmax}(\text{AutoCorr}(\tau_i)) \cdot \text{Roll}(V, -\tau_i)$$

其中 $\text{Roll}(V, -\tau_i)$ 是将 Value 序列循环移位 $-\tau_i$ 个时刻（对齐周期），然后按自相关强度加权求和。

**直觉**：不同于点注意力（"时刻 $t$ 关注时刻 $j$"），自相关机制是**子序列级别的聚合**（"当前时段关注历史上同一周期位置的时段"），天然匹配时序的周期性结构。

### 3.3 复杂度

- FFT/IFFT：$O(L \log L)$
- Top-$k$ 选择：$O(k \log L)$
- 聚合：$O(kL)$

总计：**$O(L \log L)$**——与 Informer 的 ProbSparse 复杂度相同，但计算方式完全不同。

---

## 四、Autoformer 的整体架构

### 4.1 编码器

**输入**：历史序列 $\mathbf{X}_{\text{en}} \in \mathbb{R}^{I \times d}$

每个编码器层：
1. **自相关注意力层**：捕捉历史序列内的周期性依赖
2. **序列分解**：将输出分解为趋势 $\mathcal{T}^l_\text{en}$ 和季节 $\mathcal{S}^l_\text{en}$
3. 前馈网络（Feed-Forward）
4. 再次序列分解

### 4.2 解码器

**输入**：历史尾段（季节初始化）+ 零填充（待预测步）

解码器对趋势和季节**分开聚合**：
- **趋势**：从每个分解步骤的趋势成分 $\mathcal{T}^l_\text{de}$ 累加
- **季节**：通过自相关注意力 + 交叉注意力从历史序列中提取周期性参考

**最终预测**：

$$\hat{\mathbf{Y}} = \mathcal{W}_{\mathcal{S}} \cdot \mathcal{S}_{\text{de}} + \mathcal{T}_{\text{de}}$$

---

## 五、实验结果

在论文提出时（2021 年），Autoformer 在 ETT（4个数据集）、Exchange-Rate、Weather、ILI（流感数据）等 6 个基准数据集上，长期预测任务（预测步长 $\geq 96$）的 MSE 相比 Informer 平均降低约 **38%**。

**相对 Informer 的改进来源**：
- 序列分解显式建模趋势和季节，减轻了注意力需要同时学习趋势和周期的负担
- 自相关机制比 ProbSparse 注意力更适合周期性时序（按周期对齐聚合，而非按点相似性）

---

## 六、与 FEDformer 的对比（2022）

几乎同期，Zhou 等人（Autoformer 的竞争对手）提出了 **FEDformer**（Frequency Enhanced Decomposed Transformer），同样结合了序列分解，但用**傅里叶/小波变换中的全局模式**替代局部点注意力：

- **FEDformer-f**（Fourier）：在频域随机采样少量频率，$O(L)$ 复杂度
- **FEDformer-w**（Wavelet）：多尺度小波变换，$O(L)$ 复杂度

FEDformer 在某些基准上略优于 Autoformer，说明"频域特征"与"自相关特征"各有侧重，二者的结合（如后续的 TimesNet）可能更强。

---

## 七、Autoformer 对时序建模思想的启示

Autoformer 的贡献超越了单一模型的性能提升：

**启示 1：时序归纳偏置是关键**  
直接套用 NLP 的 Transformer（点对点注意力 + 位置编码）并不是最优的时序建模方式。专为时序设计的归纳偏置（周期性、趋势-季节分解）可以显著提升性能。

**启示 2：分解应该是端到端的**  
将分解嵌入神经网络层（而非仅作预处理），允许分解与预测目标共同优化，效果优于两阶段方法。

**启示 3：自相关是时序的"自然语言"**  
对于有周期结构的时序，自相关比点注意力更自然——序列更应该"与自身的历史版本对话"，而非"与所有历史时刻平等地对话"。

这些思想在后续的 TimesNet（2023，将时序转化为 2D 图像处理）、FiLM（2022，用频域滤波器替代注意力）等工作中得到了进一步发展。

---

## 八、小结

Wu 等（2022）的 Autoformer 在"如何让 Transformer 理解时序结构"这一问题上迈出了重要一步：

> **将序列分解显式嵌入每一层，用基于 FFT 的自相关机制替代点注意力——让 Transformer 以时序的"母语"（周期与趋势）而非 NLP 的"方言"（Token 相似性）来处理时间序列。**

三大贡献：
1. **渐进式分解**：趋势-季节分解贯穿每一层，与预测目标端到端联合优化
2. **自相关机制**：用 FFT 计算周期性滞后关联，$O(L\log L)$ 复杂度下实现子序列级别的周期聚合
3. **思想层面**：明确区分了时序归纳偏置与 NLP 归纳偏置的不同，为后续架构设计指明了方向

---

*最后一篇：Nie et al. / Zeng et al.（2023）——PatchTST 与 DLinear，时序 Transformer 路线的新高峰与对整个范式的深刻反思。*
