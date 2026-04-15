# 解释Layer Normalization的作用，以及为什么Transformer使用它而不是Batch Normalization

> Source: Self-Attention机制解析
> Time: 4/15/2026, 1:15:40 AM

## Question

解释Layer Normalization的作用，以及为什么Transformer使用它而不是Batch Normalization

## Answer

Layer Normalization（层归一化，LN）的作用是：对单个样本内部的特征维度做标准化，稳定网络中的数值分布，从而让训练更容易、更稳定。


它在 Transformer 中几乎是基础组件。要理解为什么 Transformer 用它而不是 Batch Normalization，先看它到底做了什么。


一、Layer Normalization 的作用


假设某一层输出为：


$$
x = (x_1, x_2, \dots, x_d)
$$


其中  $d$  是隐藏维度。LayerNorm 会对这个向量内部做归一化：


$$
\mu = \frac{1}{d}\sum_{i=1}^d x_i
$$


$$
\sigma^2 = \frac{1}{d}\sum_{i=1}^d (x_i-\mu)^2
$$


然后得到标准化结果：


$$
\hat{x}_i = \frac{x_i-\mu}{\sqrt{\sigma^2+\epsilon}}
$$


最后再加上可学习的缩放和平移参数：


$$
y_i = \gamma \hat{x}_i + \beta
$$


其中：


$\mu, \sigma^2$  是当前样本自身在隐藏维度上的均值和方差

$\gamma, \beta$  是可学习参数

$\epsilon$  是防止分母为 0 的小常数


直观理解


它做的事情相当于：


把每个 token 的特征值拉回到更稳定的数值范围

避免某些维度特别大、某些维度特别小

让后续层更容易处理输入

减少训练过程中的不稳定和梯度问题



二、LayerNorm 在 Transformer 里的具体作用


Transformer 很深，而且每层都包含：


Self-Attention

Feed-Forward Network

Residual Connection（残差连接）


这些结构叠加后，隐藏状态的数值分布很容易波动。LayerNorm 的作用主要体现在几个方面。


1. 稳定激活值分布


不同层输出的数值范围可能差别很大。LayerNorm 可以让每个位置上的表示保持在相对稳定的范围内，减轻内部表示分布漂移的问题。


2. 改善训练稳定性


Transformer 层数深、参数多，如果没有归一化，训练容易出现：


梯度爆炸

梯度消失

收敛慢

对初始化敏感


LayerNorm 能显著缓解这些问题。


3. 配合残差连接工作


Transformer 中常见结构是：


$$
x + \text{Sublayer}(x)
$$


残差路径会把原始输入和子层输出相加。如果两者数值尺度差异过大，训练会不稳定。LayerNorm 可以帮助控制这种尺度。


4. 提高不同 token 表示的一致性


对每个 token 独立做归一化，能让每个位置的表示都处于类似的统计范围，更利于注意力层和前馈层处理。



三、为什么 Transformer 不用 Batch Normalization


关键原因是：BatchNorm 依赖 batch 维度统计，而 Transformer 的序列建模场景更适合按 token/样本独立归一化。


先看 BatchNorm 做什么。


BatchNorm 是在一个 batch 上，对某个特征维度统计均值和方差，再做归一化。也就是说，它依赖：


同一批样本

batch 内统计量

训练时和推理时不同的处理方式


这在 CNN 里很好用，但在 Transformer 里有几个明显问题。



四、BatchNorm 不适合 Transformer 的原因


1. 序列长度可变，batch 统计不稳定


Transformer 常处理：


不同长度句子

padding 后的序列

不同任务下不规则输入


如果用 BatchNorm，不同 batch 中 token 分布变化很大，统计量容易不稳定，尤其在 NLP 中比图像更明显。


2. BatchNorm 依赖 batch size


BatchNorm 的效果通常依赖较大的 batch。
但 Transformer 在很多场景下：


长序列导致显存占用高

batch size 常常较小

小 batch 下均值和方差估计噪声大


这会影响训练稳定性。


3. 每个位置的语义不同，不适合跨样本混合统计


在文本中，不同样本、不同位置的 token 语义差异很大。
BatchNorm 会把它们放在一起统计，这未必合理。


例如：


一个 batch 里有句首 token、句尾 token、padding token

它们混在一起求统计量，可能干扰表示学习


而 LayerNorm 是对每个 token 自己的隐藏维度做归一化，不依赖别的样本，更自然。


4. 训练和推理行为不一致


BatchNorm 在训练时使用 batch 统计量，在推理时使用移动平均统计量。
这会带来额外复杂性。


LayerNorm 在训练和推理时行为基本一致，因为它始终使用当前样本自身的统计量。这对 Transformer 很重要，尤其在生成任务中更方便、更稳定。


5. 不利于自回归生成


在语言模型生成时，常常是：


一次只处理一个样本

甚至一次只增量处理一个位置


这种场景下 BatchNorm 很难自然工作，因为它需要 batch 统计。
LayerNorm 不依赖 batch，所以非常适合自回归解码。



五、两者的核心区别


可以简单记成：


BatchNorm：在batch 维度上做归一化

LayerNorm：在特征维度上做归一化


对于一个 token 表示向量：


BatchNorm 会参考“别的样本”

LayerNorm 只参考“自己内部各维度”


Transformer 更需要后者。



六、一个直观比喻


把一个 token 的隐藏向量想成一个学生的一组科目成绩。


LayerNorm：看这个学生自己各科的分布，再做标准化

BatchNorm：把一整个班同学同一科的成绩拿来一起统计


在 Transformer 里，我们更关心“当前 token 自己的表示是否稳定”，而不是强依赖同 batch 其他 token 的统计。



七、补充：Transformer 中的 Pre-LN 和 Post-LN


Transformer 中 LayerNorm 还有两种常见放置方式：


Post-LN


原始 Transformer 常写作：


$$
\text{LN}(x + \text{Sublayer}(x))
$$


Pre-LN


很多现代大模型更常用：


$$
x + \text{Sublayer}(\text{LN}(x))
$$


Pre-LN 往往在深层网络中训练更稳定，更容易优化，所以现代 LLM 里更常见。



八、总结


Layer Normalization 的核心作用是：


稳定每个 token 的表示分布

加快收敛

缓解梯度问题

提高深层 Transformer 的训练稳定性


Transformer 使用 LayerNorm 而不是 BatchNorm，主要因为：


LayerNorm 不依赖 batch size

更适合可变长度序列

训练和推理行为一致

更适合自回归生成

不会把不同样本、不同位置的统计量混在一起


一句话概括：


BatchNorm 依赖“这一批数据”，而 LayerNorm 依赖“这一个 token 自己”；Transformer 需要的是后者。


下一题如果还是 Transformer 相关，我可以继续按“定义 → 公式 → 直觉 → 为什么这么设计”的格式讲。
