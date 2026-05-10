---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "计算机视觉", "论文"]
aliases: ["Gradient-Based Learning Applied to Document Recognition", "LeCun 1998 论文", "Gradient-based learning applied to document recognition"]
relates_to:
  - target: "[[LeNet-5]]"
    type: extends
    confidence: 0.95
  - target: "[[Yann LeCun]]"
    type: relates_to
    confidence: 0.95
  - target: "[[卷积神经网络（CNN）]]"
    type: extends
    confidence: 0.95
  - target: "[[反向传播]]"
    type: uses
    confidence: 0.9
supersedes: null
---

# Gradient-Based Learning Applied to Document Recognition (1998 论文)

## 概述 (50-200字符)
LeCun、Bottou、Bengio、Haffner 于 1998 年在 Proceedings of the IEEE 发表的 46 页论文，提出 [[LeNet-5]] 架构，确立了[[卷积神经网络（CNN）|卷积神经网络]]的完整框架，在手写数字识别上实现商业部署。

## 关键内容 (≥300字符, 用[[双链]])
1. **核心动机**：传统全连接网络将 28×28 图像展平为 784 维向量，连接到 1000 神经元需 784,000 参数，且完全忽略像素的空间位置关系。论文提出图像数据具有两个重要先验——**局部性**（相邻像素高度相关，有用特征是局部的如边缘、角点）和**平移不变性**（猫在图像左边和右边都是猫），网络结构应反映这些先验知识。
2. **三大核心操作**：**卷积层**用小的卷积核（如 5×5）在整张图上滑动，同一卷积核在全图共享权重，参数从 O(H·W·N) 降到 O(k·k·N），学到的特征具有平移不变性；**池化层**对特征图做空间降采样，减少[[计算]]量并增强平移鲁棒性；**全连接层**在末端进行高级语义特征组合与分类。
3. **[[LeNet-5]] 完整架构**：输入 32×32 灰度图 → C1（6个 5×5 卷积）→ S2（2×2 平均池化）→ C3（16个 5×5 卷积，部分连接）→ S4（2×2 平均池化）→ C5（120个 5×5 卷积）→ F6（84 神经元全连接）→ Output（10 类 RBF 单元），总参数量约 60,000，在 MNIST 上达到约 99% 准确率。
4. **历史影响**：该论文是 [[卷积神经网络（CNN）]] 完整框架的奠基之作。[[LeNet-5]] 在手写识别上直接商业部署，所有现代 CNN 都是其直接祖先。14 年后 [[AlexNet]]（2012）继承了这一架构思路，用 [[ReLU激活函数]] 替代 [[Sigmoid激活函数]]、最大池化替代平均池化、GPU 替代 CPU，在 [[ImageNet]] 上取得突破。

## 来源
- LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278–2324.

## 相关
- [[LeNet-5]] — extends（论文提出的核心架构）
- [[Yann LeCun]] — relates_to（第一作者）
- [[卷积神经网络（CNN）]] — extends（确立 CNN 完整框架）
- [[反向传播]] — uses（端到端训练方法）
