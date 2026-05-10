---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["深度学习", "权重初始化", "优化"]
aliases: ["He Initialization", "Kaiming Initialization", "何恺明初始化", "Kaiming Normal", "kaiming_normal_"]
relates_to: ["残差网络（ResNet）", "ReLU激活函数", "Xavier 初始化", "深度卷积网络"]
supersedes: null
---

# He 初始化（Kaiming Initialization）

## 概述
一种专为 ReLU 激活函数设计的权重初始化方法，由[[Kaiming He|何恺明]]等人提出，通过保持前向和[[反向传播]]的方差稳定来加速深层网络训练。

## 关键内容
1. **动机**：[[Xavier 初始化]]假设激活函数关于原点对称（如 tanh、sigmoid），但 ReLU 会将负值截断为零，导致输出方差约为输入方差的一半。He 初始化针对这一特性调整了初始化方差，使每层的输出方差保持一致。
2. **公式**：权重从均值为零、标准差为 √(2/n_in) 的[[正态分布]]中采样，其中 n_in 是输入连接数（fan-in）。[[PyTorch]] 中通过 `nn.init.kaiming_normal_(weight, mode='fan_out', nonlinearity='relu')` 实现。
3. **在[[残差网络（ResNet）]]中的应用**：[[残差网络（ResNet）|ResNet]] 的 [[PyTorch]] 实现在所有卷积层上统一使用 He 初始化，这是确保152层超深网络能够稳定训练的关键技术细节之一。没有恰当的初始化，即使有[[残差连接（Residual Connection）]]，深层网络仍可能在训练初期就陷入不良状态。
4. **与 [[Xavier 初始化]]的对比**：Xavier 使用 √(1/n_in)，He 使用 √(2/n_in)。因子 2 正是为了补偿 ReLU 截断负值造成的方差减半。对于 Leaky ReLU，He 初始化可进一步调整为 √(2/(1+a²)·n_in)，其中 a 是负斜率。
5. **mode 参数**：`fan_in` 模式保持前向传播方差稳定，`fan_out` 模式保持[[反向传播]]方差稳定。[[残差网络（ResNet）|ResNet]] 实现中使用 `fan_out` 模式，以确保梯度从深层向浅层传播时的稳定性。

## 来源
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — PyTorch 实现代码中的权重初始化部分（第322-325行）

## 相关
- [[残差网络（ResNet）]] — uses
- [[ReLU激活函数]] — depends_on（专为 ReLU 设计）
- [[Xavier 初始化]] — compares_to（前身方法）
- [[深度卷积网络]] — uses
