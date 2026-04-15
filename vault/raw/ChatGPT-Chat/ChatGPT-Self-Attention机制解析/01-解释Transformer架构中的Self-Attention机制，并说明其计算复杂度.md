# 解释Transformer架构中的Self-Attention机制，并说明其计算复杂度

> Source: Self-Attention机制解析
> Time: 4/12/2026, 10:30:34 AM

## Question

解释Transformer架构中的Self-Attention机制，并说明其计算复杂度

## Answer

Self-Attention 是 Transformer 的核心机制。它的作用是：让序列中的每个位置都能根据内容，动态关注序列中其他所有位置，从而获得更强的上下文表示。


一、Self-Attention 的基本过程


假设输入序列长度为  $n$ ，每个 token 的表示维度为  $d$ 。输入矩阵记为：


$$
X \in \mathbb{R}^{n \times d}
$$


Self-Attention 会先通过三组线性变换，把输入映射成：


Query（查询）矩阵  $Q$

Key（键）矩阵  $K$

Value（值）矩阵  $V$


即：


$$
Q = XW_Q,\quad K = XW_K,\quad V = XW_V
$$


其中：


$$
Q, K, V \in \mathbb{R}^{n \times d_k}
$$


或  $V$  也可写成  $n \times d_v$ 。


1. 计算注意力分数


每个 token 的 Query 与所有 token 的 Key 做点积，得到相似度分数：


$$
QK^T
$$


其结果是一个  $n \times n$  的矩阵，表示“每个位置对所有位置的关注程度”。


2. 缩放


为了避免点积值过大，通常除以  $\sqrt{d_k}$ ：


$$
\frac{QK^T}{\sqrt{d_k}}
$$


3. Softmax 归一化


对每一行做 softmax，得到注意力权重：


$$
\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)
$$


这样每个 token 对其他 token 的注意力权重之和为 1。


4. 加权求和


用注意力权重对  $V$  加权求和，得到输出：


$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$


这就是单头 Self-Attention。



二、直观理解


可以把它理解成：


Q：我想找什么信息

K：我这里有什么信息可供匹配

V：真正要取出的内容


对于某个 token，它会拿自己的 Query 去和所有 token 的 Key 比较，决定应该从哪些位置取多少信息，再对对应 Value 做加权汇总。


所以 Self-Attention 的优势在于：


能建模长距离依赖

不像 RNN 那样必须按顺序传播

每个位置都能直接看到全局上下文



三、Multi-Head Attention


Transformer 实际上通常不用单头，而是多头注意力：


$$
\text{MultiHead}(Q,K,V)=\text{Concat}(head_1,\dots,head_h)W_O
$$


每个 head 在不同子空间里学习不同类型的关系，比如：


语法依赖

指代关系

局部邻近关系

语义相关性



四、计算复杂度


设：


序列长度为  $n$

表示维度为  $d$


Self-Attention 的主要计算开销来自两部分：


1. 计算  $QK^T$


$$
(n \times d)(d \times n) \Rightarrow O(n^2 d)
$$


2. 注意力权重与  $V$  相乘


$$
(n \times n)(n \times d) \Rightarrow O(n^2 d)
$$


所以 Self-Attention 的总体时间复杂度为：


$$
\boxed{O(n^2 d)}
$$


如果只关注序列长度  $n$ ，通常简写为：


$$
\boxed{O(n^2)}
$$



五、空间复杂度


注意力矩阵大小为：


$$
n \times n
$$


所以空间复杂度主要是：


$$
\boxed{O(n^2)}
$$


这也是 Transformer 在处理超长序列时的主要瓶颈。



六、与 RNN/CNN 的对比


相比 RNN


RNN 时间步串行，难并行

Self-Attention 可并行计算所有位置

但 Self-Attention 的复杂度在长序列下更高


相比 CNN


CNN 擅长局部建模

Self-Attention 天然具备全局感受野

更容易捕捉远距离依赖



七、总结


Self-Attention 的本质是：


让每个 token 根据与其他 token 的相关性，对全序列信息进行加权聚合。


核心公式是：


$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$


其主要复杂度为：


时间复杂度：  $\boxed{O(n^2 d)}$

空间复杂度：  $\boxed{O(n^2)}$


瓶颈在于注意力矩阵随序列长度平方增长。


如果你愿意，我也可以继续给你讲一下 为什么 Self-Attention 比 RNN 更适合大模型，或者画一个更直观的矩阵计算示意。
