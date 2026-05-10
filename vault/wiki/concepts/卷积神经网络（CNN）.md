---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "计算机视觉"]
aliases: ["LeNet-5", "LeNet", "LeNet 5", "卷积神经网络", "CNN", "Convolutional Neural Network"]
relates_to:
  - target: "[[Gradient-Based Learning Applied to Document Recognition (1998 论文)]]"
    type: extends
    confidence: 0.95
  - target: "[[Yann LeCun]]"
    type: relates_to
    confidence: 0.95
  - target: "[[反向传播]]"
    type: uses
    confidence: 0.9
  - target: "[[Sigmoid激活函数]]"
    type: uses
    confidence: 0.9
  - target: "[[梯度消失]]"
    type: relates_to
    confidence: 0.8
  - target: "[[多层感知机（MLP）]]"
    type: compares_to
    confidence: 0.85
  - target: "[[AlexNet]]"
    type: extends
    confidence: 0.95
  - target: "[[ReLU激活函数]]"
    type: uses
    confidence: 0.9
  - target: "[[最大池化（Max Pooling）]]"
    type: uses
    confidence: 0.85
  - target: "[[手工特征工程]]"
    type: supersedes
    confidence: 0.9
supersedes: null
---

# 卷积神经网络（CNN）

## 概述 (50-200字符)
卷积神经网络是一类专为网格结构数据（如图像）设计的深度神经网络，通过卷积层的局部[[感受野]]和权重共享机制，自动学习空间层次化特征，是[[计算]]机视觉领域的基石架构。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心设计原则**：CNN 基于两个图像数据先验——**局部性**（相邻像素高度相关，有用特征是局部的如边缘、角点）和**平移不变性**（目标在图像任意位置都应被识别）。[[LeNet-5]] 首次将这两个先验编码为网络结构，而非让网络从零学习。
2. **三大核心操作**：**卷积层**用[[3×3卷积核|小卷积核]]（如 5×5）在整张图上滑动，同一卷积核在全图共享权重，参数从 O(H·W·N) 降到 O(k·k·N)；**池化层**（平均池化/最大池化）对特征图做空间降采样，减少[[计算]]量并增强平移鲁棒性；**全连接层**在末端进行高级语义特征组合与分类。
3. **[[LeNet-5]] 架构**：[[LeCun et al. 1998]] 提出的完整 CNN 框架：输入 32×32 灰度图 → C1（6个 5×5 卷积）→ S2（2×2 平均池化）→ C3（16个 5×5 卷积，部分连接）→ S4（2×2 平均池化）→ C5（120个 5×5 卷积，相当于全连接）→ F6（84 神经元全连接）→ Output（10 类 RBF 单元），总参数量约 60,000。
4. **从 LeNet 到现代 CNN 的演化**：[[LeNet-5]]（1998）使用 [[Sigmoid激活函数]] + 平均池化，受限于 [[梯度消失]] 问题；[[AlexNet]]（2012）引入 [[ReLU激活函数]] + [[最大池化（Max Pooling）]] + GPU 训练，参数量从 60K 跃升至 60M，在 [[ImageNet]] 上取得突破性 [[Top-5 错误率]] 16.4%，终结了[[手工特征工程]]时代，开启了深度学习革命。
5. **与全连接网络的对比**：传统 [[多层感知机（MLP）]] 将图像展平为一维向量，完全忽略像素的空间位置关系。28×28 图像展平后 784 维，连接到 1000 神经元需 784,000 参数。CNN 通过局部连接和权重共享，用约 60K 参数实现更优性能。

## 来源
- LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278–2324.
- raw/articles/ai-papers/machine-learning/05_lenet_1998.md — 源文件
- raw/articles/ai-papers/foundations/paper_03_alexnet.md — AlexNet 论文精读（CNN 规模化验证）

## 相关
- [[LeNet-5]] — implements（LeNet-5 是 CNN 的第一个完整实现）
- [[Gradient-Based Learning Applied to Document Recognition (1998 论文)]] — extends（论文提出架构）
- [[Yann LeCun]] — relates_to（主要作者）
- [[反向传播]] — uses（端到端训练方法）
- [[Sigmoid激活函数]] — uses（LeNet-5 原始激活函数）
- [[多层感知机（MLP）]] — compares_to（对比全连接方案）
- [[梯度消失]] — relates_to（Sigmoid 导致的训练限制）
