---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [深度学习, 神经网络, 初始化, 优化, 概率论]
aliases: ["Xavier Initialization", "Glorot Initialization", "Xavier 初始化", "Glorot 初始化"]
relates_to:
  - target: "[[梯度消失]]"
    type: mitigates
  - target: "[[反向传播]]"
    type: supports
  - target: "[[Sigmoid激活函数]]"
    type: relates_to
supersedes: null
---

# Xavier 初始化

## 概述
Xavier 初始化（Glorot 初始化）是一种神经网络权重初始化策略，根据层的输入和输出维度缩放随机权重的方差，使信号在前向和[[反向传播]]中保持稳定。

## 关键内容
1. **为什么需要特殊初始化**：如果权重初始化过大，激活值会饱和（Sigmoid 接近 0 或 1），导致[[梯度消失]]；如果初始化过小，信号逐层衰减，网络无法学习。Xavier 初始化通过数学推导找到"刚刚好"的方差。
2. **数学原理**：W ~ N(0, 2/(n_in + n_out)) 或 Uniform(-√(6/(n_in + n_out)), √(6/(n_in + n_out)))，其中 n_in 和 n_out 分别是层的输入和输出维度。这个公式确保前向传播时各层输出的方差一致，[[反向传播]]时各层梯度的方差也一致。
3. **与激活函数的关系**：Xavier 初始化针对[[Sigmoid激活函数]]和 tanh 设计。对于[[ReLU激活函数]]，后来发展出 He 初始化（Kaiming 初始化），将方差调整为 2/n_in，因为 ReLU 会将一半的激活值置零。
4. **在代码中的体现**：1986 年原始论文尚未提出 Xavier 初始化（该方法是 2010 年 Glorot & Bengio 提出的），但现代实现中已成为标准实践。源码示例中使用 np.sqrt(2/input_size) 作为缩放因子。

## 来源
- [[paper_02_backpropagation]] — 代码实现中的权重初始化注释

## 相关
- [[梯度消失]] — mitigates
- [[反向传播]] — supports
- [[Sigmoid激活函数]] — relates_to
- [[ReLU激活函数]] — relates_to
- [[Batch Normalization]] — compares_to
