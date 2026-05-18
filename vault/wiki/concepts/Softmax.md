---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 分类, 激活函数, 概率, 机器学习]
aliases: ["Softmax", "Softmax Function", "Softmax 函数", "归一化指数函数"]
relates_to: ["交叉熵", "AlexNet", "Sigmoid激活函数", "多分类问题"]
supersedes: null
---

# Softmax

## 概述
Softmax 函数将任意实数向量转换为概率分布，各分量之和为 1，是多分类神经网络输出层的标准激活函数。

## 关键内容

1. **数学定义**：对于输入向量 z，Softmax 输出 σ(z)ᵢ = exp(zᵢ) / Σⱼ exp(zⱼ)。指数运算确保所有输出为正，归一化确保总和为 1，因此输出可以解释为类别概率。
2. **在 [[AlexNet]] 中的应用**：[[AlexNet]] 的最后全连接层（FC3）输出 1000 个类别的 logits，经过 Softmax 转换为 1000 维概率分布。预测时取概率最大的类别作为输出。
3. **与[[交叉熵]]的配合**：Softmax 输出通常与 [[交叉熵]] 损失函数配合使用。Softmax + [[交叉熵]]的组合在[[反向传播]]时有简洁的梯度形式：∂L/∂z = p - y（预测概率减去真实标签），数值稳定且[[计算]]高效。
4. **数值稳定性**：直接[[计算]] exp(zᵢ) 可能导致溢出。实践中先减去最大值：σ(z)ᵢ = exp(zᵢ - max(z)) / Σⱼ exp(zⱼ - max(z))，这在数学上等价但数值上稳定。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[AlexNet]] — used_in
- [[交叉熵]] — paired_with
- [[Sigmoid激活函数]] — generalizes_to_multiclass
- [[多分类问题]] — standard_solution
