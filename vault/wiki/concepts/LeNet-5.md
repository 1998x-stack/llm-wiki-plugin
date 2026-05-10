---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["机器学习", "深度学习", "计算机视觉", "经典架构"]
aliases: ["LeNet-5", "LeNet 5", "LeNet"]
relates_to:
  - target: "[[卷积神经网络（CNN）]]"
    type: implements
    confidence: 0.95
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
supersedes: null
---

# LeNet-5

## 概述 (50-200字符)
[[卷积神经网络（CNN）|LeNet]]-5 是 [[Yann LeCun]] 于 1998 年提出的[[卷积神经网络（CNN）|卷积神经网络]]架构，是 CNN 完整框架的奠基者，在手写数字识别（MNIST）上达到约 99% 准确率并实现商业部署。

## 关键内容 (≥300字符, 用[[双链]])
1. **历史背景**：1990 年代美国邮政局（USPS）面临海量手写邮编的机器识别难题。[[Yann LeCun]] 在[[贝尔实验室]]构建了端到端图像识别系统——不依赖人工[[特征工程（Feature Engineering）|特征工程]]，让网络直接从像素学习特征，并用 [[反向传播]] 训练整个流水线。该论文长达 46 页，既是学术杰作也是工程蓝图。
2. **网络架构**：输入 32×32 灰度图像（MNIST 28×28 填充到 32×32）→ C1（6个 5×5 卷积核，156 参数）→ Sigmoid → S2（2×2 平均池化，6×14×14）→ C3（16个 5×5 卷积核，部分连接，1516 参数）→ Sigmoid → S4（2×2 平均池化，16×5×5）→ C5（120个 5×5 卷积核，48120 参数）→ Sigmoid → F6（全连接 84 神经元，10164 参数）→ Sigmoid → Output（10 类 RBF 单元，840 参数）。总参数量约 60,000。
3. **五大技术贡献**：**局部[[感受野]]**（每个神经元只看局部区域，成为 CNN 基础）；**权重共享**（同一特征全图通用，参数效率的关键）；**池化层**（降采样增强平移鲁棒性，后演化为 MaxPool）；**端到端训练**（特征提取+分类器共同 BP，确立深度学习[[规范化理论|范式]]）；**梯度学习**（整个流水线用同一损失优化，所有现代网络沿用此思路）。
4. **[[卷积神经网络（CNN）|LeNet]] → [[AlexNet]] 的 14 年演化**：[[卷积神经网络（CNN）|LeNet]]-5（1998）层数 5，Sigmoid 激活，平均池化，CPU 训练，MNIST 60K 数据，60K 参数，~99% 精度；[[AlexNet]]（2012）层数 8（5 卷积+3 全连接），ReLU 激活解决 [[梯度消失]]，最大池化，双 GPU（GTX 580）训练，[[ImageNet]] 1.2M 数据，60M 参数，[[Top-5 错误率]] 15.3%。
5. **历史地位**：首创性 ⭐⭐⭐⭐⭐（CNN 完整框架的奠基者）；工程完整性 ⭐⭐⭐⭐⭐（46 页论文涵盖架构+训练+应用）；实用性 ⭐⭐⭐⭐（在手写识别上直接商业部署）；历史影响 ⭐⭐⭐⭐⭐（所有现代 CNN 的直接祖先）。证明了特征可以被自动学习——从此人工[[特征工程（Feature Engineering）|特征工程]]不再是图像识别的瓶颈。

## 来源
- LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278–2324.
- raw/articles/ai-papers/machine-learning/05_lenet_1998.md — 源文件

## 相关
- [[卷积神经网络（CNN）]] — implements（LeNet-5 是 CNN 的第一个完整实现）
- [[Gradient-Based Learning Applied to Document Recognition (1998 论文)]] — extends（论文提出架构）
- [[Yann LeCun]] — relates_to（主要作者）
- [[反向传播]] — uses（端到端训练方法）
- [[Sigmoid激活函数]] — uses（原始激活函数）
- [[梯度消失]] — relates_to（Sigmoid 导致的训练限制）
