# 什么是注意力掩码（Attention Mask）？在训练和推理中分别如何使用？

> Source: 注意力掩码解析
> Time: 4/16/2026, 12:38:46 AM

## Question

什么是注意力掩码（Attention Mask）？在训练和推理中分别如何使用？

## Answer

注意力掩码（Attention Mask）的作用是：控制一个 token 在计算注意力时“能看见谁、不能看见谁”。


在 Self-Attention 里，注意力分数通常是：


$$
\text{Attention}(Q,K,V)=\text{softmax}\left(\frac{QK^T}{\sqrt{d_k}} + M\right)V
$$


这里的  $M$  就可以理解为 mask。
对于不允许关注的位置，会在对应分数上加一个很小的值（如  $-\infty$ ），这样经过 softmax 后，该位置权重几乎变成 0。



1. Attention Mask 是什么


它本质上是一个约束矩阵，决定注意力矩阵中哪些位置有效、哪些位置无效。


假设序列长度为 4，某个 token 原本可以关注所有位置：


$$
[ s_1, s_2, s_3, s_4 ]
$$


如果 mask 规定第 3、4 个位置不可见，那么加上 mask 后可能变成：


$$
[ s_1, s_2, -\infty, -\infty ]
$$


softmax 后，后两个位置的权重就接近 0。



2. 常见的两类 Attention Mask


2.1 Padding Mask


用于处理补齐的无效 token。


因为一个 batch 中句子长度不同，通常要补 PAD：


句子 A: I like NLP

句子 B: I like


补齐后可能变成：


A: I like NLP

B: I like [PAD]


这里 [PAD] 不是真实内容，所以注意力不应分配到它上面。
Padding Mask 就是让模型忽略这些 PAD 位置。


作用：


不让别的 token 去关注 PAD

有时也不让 PAD 自己产生有效影响



2.2 Causal Mask / Look-Ahead Mask


用于自回归生成，防止“看到未来”。


例如序列：


I love deep learning


在预测 deep 时，模型只能看：


I love


不能偷看后面的 learning。


因此 mask 通常是一个下三角矩阵：


$$
\begin{bmatrix} 1 & 0 & 0 & 0 \ 1 & 1 & 0 & 0 \ 1 & 1 & 1 & 0 \ 1 & 1 & 1 & 1 \end{bmatrix}
$$


含义是：


第 1 个 token 只能看自己

第 2 个 token 只能看前两个

第 3 个 token 只能看前三个

…


这保证了生成过程符合“从左到右”的因果关系。



3. 在训练中如何使用


3.1 Encoder 训练


如果是 BERT 这类 双向 encoder：


一般使用 padding mask

不使用 causal mask


因为 encoder 希望每个 token 可以同时看左边和右边上下文，只是不看 PAD。



3.2 Decoder 训练


如果是 GPT 或 Transformer decoder：


使用 causal mask

同时通常还会叠加 padding mask


因为训练虽然是并行计算整个序列，但每个位置仍然必须只能看当前位置及之前的位置，不能看到未来 token。


例如训练句子：


I love NLP


虽然一次性把整句送进去，但：


预测 love 时不能看 NLP

预测 NLP 时可以看 I love


所以训练阶段必须加 causal mask，避免信息泄露。



3.3 Encoder-Decoder 结构


如原始 Transformer 做机器翻译时：


Encoder self-attention：用 padding mask

Decoder self-attention：用 causal mask + padding mask

Encoder-Decoder attention：通常对 encoder 输出使用 padding mask


因为 decoder 查询 encoder 时，不应该关注 encoder 端的 PAD 位置。



4. 在推理中如何使用


4.1 自回归推理


在 GPT 推理时，模型是逐 token 生成的：


第一步生成第 1 个 token

第二步生成第 2 个 token

第三步生成第 3 个 token


由于当前时刻本来就没有“未来 token”输入，从实现上说，因果约束天然成立。
但在模型计算逻辑里，通常仍然按 causal mask 的规则来保证一致性。


也就是说：


训练时：整段并行计算，必须靠 causal mask 防止偷看未来

推理时：一步一步生成，未来还不存在，但实现中通常仍保留相同的 mask 机制



4.2 带 KV Cache 的推理


推理时常用 KV cache 加速：


历史 token 的 K、V 缓存起来

新 token 只和过去缓存交互


这时 mask 的逻辑更简单：


新 token 只能访问历史和自己

不存在访问未来的问题


本质上仍然满足 causal mask。



4.3 Padding Mask 在推理中


如果推理是单条样本，且没有 padding，padding mask 可能不明显。
但如果是批量推理，不同样本长度不同，仍然需要 padding mask 来忽略补齐位置。



5. 训练和推理中的区别


可以概括成一句话：


训练：为了并行计算整段序列，必须显式使用 mask 防止违规关注

推理：因为是逐步生成，未来 token 不会真正输入，但仍常保留同样的 mask 规则，并在 batch 场景中继续使用 padding mask



6. 一个直观例子


句子：


我 喜欢 学习 Transformer


训练 GPT 时，预测“学习”这个位置时：


可以看：我 喜欢

不能看：Transformer


所以对应 attention 权重中，“Transformer”那一列会被 mask 掉。


如果同一个 batch 里另一个句子更短，被补成：


我 喜欢 [PAD] [PAD]


那么后两个 [PAD] 也会被 padding mask 屏蔽，不参与有效注意力计算。



7. 总结


Attention Mask 的本质是：通过屏蔽某些位置，控制注意力的可见范围。


主要作用有两种：


Padding Mask：屏蔽补齐位置，避免无效 token 干扰

Causal Mask：屏蔽未来位置，保证自回归生成不泄露未来信息


使用方式上：


训练时
encoder：主要用 padding mask

decoder/GPT：用 causal mask，通常还叠加 padding mask

推理时
自回归生成天然遵守因果顺序

batch 推理仍可能需要 padding mask

实现上通常继续沿用 causal mask 逻辑


如果你愿意，我可以继续把这个问题画成一个 4×4 attention 矩阵示意图，让你一眼看懂 mask 是怎么作用在 softmax 前的。
