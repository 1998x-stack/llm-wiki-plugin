# 解释KV Cache的原理，以及它在自回归生成中的作用

> Source: 注意力掩码解析
> Time: 4/16/2026, 12:42:19 AM

## Question

解释KV Cache的原理，以及它在自回归生成中的作用

## Answer

KV Cache 的核心思想是：


在自回归生成时，把历史 token 已经算过的 Key 和 Value 缓存起来，后续生成新 token 时直接复用，不再重复计算。


它的主要作用是：显著降低推理阶段的重复计算，提高生成速度。



1. 先看问题：为什么会有重复计算


以 GPT 这类自回归模型为例，生成过程是从左到右逐个 token 生成的。


假设已经生成了：


我 喜欢 学习


现在要继续生成下一个 token。


在普通 self-attention 里，每一步都会对当前已有序列重新做一遍注意力计算。
也就是说：


生成第 1 个 token，算一次

生成第 2 个 token，又对前 2 个 token 算一次

生成第 3 个 token，又对前 3 个 token 算一次

…


这样会导致一个很大的浪费：


前面 token 的表示其实早就算过了，但每次生成新 token 时又被重复算一遍。



2. KV Cache 到底缓存了什么


在 Attention 中，每层都会把输入隐状态投影成：


$Q$ : Query

$K$ : Key

$V$ : Value


注意力计算是：


$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V
$$


对于自回归生成里的“当前新 token”来说：


它只需要生成自己的 Query

然后拿这个 Query 去和所有历史 token 的 Key做匹配

再用注意力权重对所有历史 token 的 Value做加权求和


所以历史 token 最有价值、最适合缓存的就是：


K（Key）

V（Value）


这就是 KV Cache。



3. 它的工作原理


不使用 KV Cache


假设已经有长度为  $t$  的上下文，要生成第  $t+1$  个 token。


如果不用 cache，那么第  $t+1$  步时需要：


把前  $t$  个 token 和当前 token 一起送进模型

每一层重新计算所有这些 token 的 Q、K、V

再做完整 attention


这意味着历史部分被反复重算。



使用 KV Cache


如果用了 cache，那么在前面步骤中，每层历史 token 的 K、V 都已经保存好了。


生成第  $t+1$  个 token 时，只需要：


对新 token计算当前层的  $Q_{t+1}, K_{t+1}, V_{t+1}$

把  $K_{t+1}, V_{t+1}$  追加到缓存里

用  $Q_{t+1}$  去和缓存中的全部  $K$  计算注意力

再对缓存中的全部  $V$  加权求和


这样就避免了对前  $1 \sim t$  个 token 的重复投影和重复 attention 前处理。



4. 为什么只缓存 K 和 V，不缓存 Q


因为 Query 的作用是：


表示“当前位置正在找什么”。


每次新生成一个 token，它的 Query 都是新的，只对当前步有用。
历史 token 的 Query 在下一步基本不再需要，因为我们不会重新计算“历史 token 对别人看什么”，而只关心：


当前 token 看历史 token。


所以：


历史的 K、V 要保留

历史的 Q 一般不需要缓存



5. 在自回归生成中的作用


KV Cache 的主要作用是：


第一，减少重复计算


历史 token 的 K、V 一次算完，多次复用。


第二，显著提升推理速度


尤其是输出很长时，效果非常明显。
因为生成第 500 个 token 时，如果没有 cache，你会把前 499 个 token 又重新算很多遍。


第三，降低每步延迟


在对话系统、代码补全、实时生成里，用户感受到的“一个 token 一个 token 冒出来”的速度，和 KV Cache 强相关。



6. 复杂度上怎么理解


设生成长度为  $T$ 。


不用 KV Cache


每一步都要重新处理之前所有 token，整体重复计算很多。
总成本大致会呈现平方级累积趋势。


用 KV Cache


每一步只新增一个 token 的 K、V 计算，虽然 attention 仍要和历史长度交互，但避免了大量重复的前向计算。
所以实际推理效率会高很多。


更准确地说：


计算 K/V 投影的重复开销被消掉了

attention 与历史序列交互这件事本身没有完全消失


因此 KV Cache 不是把复杂度完全变成线性，而是显著减少常数项和重复部分，让长序列生成快很多。



7. 一个直观例子


假设序列是：


A B C


现在要生成 D。


没有 KV Cache


模型可能会重新处理：


A B C D


于是 A、B、C 在每一层的 K、V 又算了一遍。


有 KV Cache


前面生成 A、B、C 时，它们每层的 K、V 都已经存好了。
生成 D 时：


只算 D 的 Q、K、V

D 的 Q 去和 A、B、C、D 的 K 做注意力

再结合 A、B、C、D 的 V 得到输出


这样就省掉了 A、B、C 的重复计算。



8. KV Cache 在多层 Transformer 中怎么存


Transformer 不止一层，所以 KV Cache 也不是一份，而是：


每一层都有自己的 K Cache

每一层都有自己的 V Cache


如果模型有  $L$  层，那么缓存结构大致是：


Layer 1: past K, past V

Layer 2: past K, past V

...

Layer L: past K, past V


因为不同层的表示不同，不能混用。


另外在多头注意力里，缓存通常还要保留：


batch 维度

head 维度

sequence length 维度

head_dim 维度



9. 它的代价是什么


KV Cache 不是免费午餐，它用显存/内存换速度。


随着生成序列变长，缓存会越来越大，因为每生成一个新 token，每层都要多存一份 K 和 V。


所以它的代价包括：


1）显存占用增加


上下文越长、层数越多、head 越多，cache 越大。


2）长上下文时可能成为瓶颈


当上下文特别长时，虽然避免了重复计算，但缓存本身非常占显存，读取也会变慢。


3）batch 大时更明显


如果同时给很多请求做生成，每个请求都维护自己的 KV Cache，显存压力会快速上升。



10. 训练时为什么通常不用 KV Cache


因为训练和推理不一样。


训练时通常采用 teacher forcing：


整个序列一次性并行输入

每个位置同时预测下一个 token


这时重点是并行计算整段序列，而不是一步一步生成。
所以通常不会像推理那样逐 token 地维护 KV Cache。


换句话说：


KV Cache 主要是推理优化技术

不是训练阶段的核心机制



11. 和 Attention Mask 的关系


KV Cache 和 causal mask 经常一起出现，但作用不同：


causal mask：保证当前 token 不能看未来

KV cache：把过去 token 的 K/V 保存下来，避免重复计算


一个负责正确性，一个负责效率。



12. 总结


一句话概括：


KV Cache 就是在自回归生成时，把历史 token 在每层注意力中的 Key 和 Value 保存起来，新 token 生成时直接复用这些历史信息，从而避免重复计算，提升推理速度。


你可以把它理解成：


没有 KV Cache：每次生成都“全文重读”

有 KV Cache：历史内容已经做过笔记，新 token 来了只查笔记再补一条



13. 最后给一个非常精炼的面试版回答


KV Cache 是 Transformer 在自回归推理中的一种加速机制。其原理是在每一层缓存历史 token 的 Key 和 Value，后续生成新 token 时只需计算当前 token 的 Query、Key、Value，并让当前 Query 与缓存的历史 Keys 做注意力，再对缓存的 Values 加权求和。这样避免了对历史 token 的重复计算，显著提升长文本生成效率。代价是额外的显存占用。


你这组题已经形成一条完整链路了：
Self-Attention → Mask → KV Cache。


下一题如果你愿意，我可以继续讲：


6. 为什么大模型推理是 memory-bound，而不是 compute-bound？
这和 KV Cache、带宽、吞吐关系非常大。
