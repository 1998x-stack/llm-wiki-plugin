---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["深度学习", "计算机视觉", "网络架构", "机器学习"]
aliases: ["ResNet", "Residual Network", "何恺明网络", "ResNet Architecture"]
relates_to: 
  - target: "[[卷积神经网络（CNN）]]"
    type: extends
    confidence: 0.9
  - target: "[[退化问题（Degradation Problem）]]"
    type: addresses
    confidence: 0.9
  - target: "[[残差连接（Residual Connection）]]"
    type: uses
    confidence: 0.95
  - target: "[[ImageNet]]"
    type: tested_on
    confidence: 0.9
  - target: "[[Kaiming He]]"
    type: creator
    confidence: 0.9
  - target: "[[微软亚洲研究院]]"
    type: developed_at
    confidence: 0.9
  - target: "[[Deep Residual Learning for Image Recognition (2016 论文)]]"
    type: implements
    confidence: 0.95
  - target: "[[ILSVRC 2015]]"
    type: achieves_results_on
    confidence: 0.95
  - target: "[[AlexNet]]"
    type: improves_over
    confidence: 0.85
  - target: "[[VGGNet]]"
    type: improves_over
    confidence: 0.85
  - target: "[[Batch Normalization]]"
    type: uses
    confidence: 0.9
  - target: "[[PyTorch]]"
    type: implementable_in
    confidence: 0.8
  - target: "[[跳跃连接（Skip Connection）]]"
    type: uses
    confidence: 0.95
  - target: "[[He 初始化（Kaiming Initialization）]]"
    type: uses
    confidence: 0.85
supersedes: null
---

# 残差网络（ResNet）

## 概述
[[Kaiming He|何恺明]]等人于2015年在[[微软亚洲研究院]]提出的深度网络架构，通过[[残差连接]]解决退化问题，使网络可训练至152层以上。ResNet 在 [[ILSVRC 2015]] 竞赛中获得图像分类、目标检测、图像定位三项冠军，并获得 CVPR 2016 最佳论文奖，成为 AI 历史上最具有影响力的网络架构之一。

## 关键内容
1. **核心架构**：残差网络通过引入[[残差连接（Residual连接）]]（skip connection/[[残差连接（Residual Connection）|恒等捷径]]），将传统网络的直接映射 H(x) [[重构]]为 H(x) = F(x) + x，其中 F(x) 是网络学习的残差。这一设计使梯度可以通过"梯度高速公路"直接流向浅层，解决了深层网络的[[梯度消失]]问题。

2. **两种残差块**：
   - BasicBlock（用于ResNet-18/34）：Conv3×3-BN-ReLU-Conv3×3-BN结构，简单高效。
   - Bottleneck（用于ResNet-50/101/152）：1×1降维-3×3-1×1升维结构，通过1×1卷积将[[计算]]量减少约40%，使更深的网络得以实现。

3. **ResNet家族**：
   - ResNet-18（11.7M参数, ~10% Top-5错误率）
   - ResNet-34（21.8M参数, 7.73% Top-5错误率）
   - ResNet-50（25.6M参数, 6.71% Top-5错误率，最常用版本）
   - ResNet-101（44.5M参数, 6.05% Top-5错误率）
   - ResNet-152（60.2M参数, 4.49% Top-5错误率，152层的超深网络）

4. **退化问题的解决**：[[退化问题（Degradation Problem）]]指更深层网络训练误差反而更高的现象。ResNet通过[[残差学习（Residual Learning）|残差学习]]使网络在最优解接近恒等映射时只需将权重推向零，比学习恒等变换容易得多。实验表明，即使到1202层的超深网络仍能训练，这在普通网络中是不可能的。

5. **竞赛成就**：在[[ILSVRC]] 2015中获得图像分类、目标检测、图像定位三项第一，以及COCO 2015检测任务第一，同时获得CVPR 2016最佳论文奖，成为史无前例的"五冠王"。ResNet-152在[[ImageNet]]以3.57% Top-5错误率夺冠，首次超越人类图像识别水平（约5.1%）。

6. **广泛影响**：[[残差连接]]成为现代深度学习的默认[[规范化理论|范式]]，被[[Transformer]]、GPT、BERT、[[U-Net]]、神经ODE等架构广泛采用。后续衍生出DenseNet、SENet、ResNeXt、EfficientNet等变体，影响遍及[[计算]]机视觉、自然语言处理等所有深度学习领域。

7. **理论解释**：
   - 梯度高速公路：提供了∂L/∂x = ∂L/∂y · (1 + ∂F(x)/∂x)的直接路径，保证梯度不会完全消失
   - [[隐式集成]]：相当于对指数级数量浅层路径进行集成
   - [[损失景观平滑化|损失曲面平滑化]]：使优化过程更加稳定

8. **维度不匹配处理**：当输入输出维度不匹配时（如通道数翻倍、特征图尺寸减半），通过1×1投影卷积或补零操作调整[[跳跃连接（Skip Connection）|跳跃连接]]的维度。

9. **具体实验数据**：在[[CIFAR-10 数据集|CIFAR-10]]上的实验显示，普通网络（Plain Network）在56层以上开始出现退化，而残差网络（ResNet）即使到1202层仍可训练。例如，56层ResNet的错误率为6.97%，而对应的plain网络错误率为7.20%。

## 来源
- [[raw/articles/ai-papers/machine-learning/13_resnet_2015.md]] — 原始笔记文件
- [[raw/articles/ai-papers/foundations/paper_05_resnet.md]] — 全文精读
- [[https://arxiv.org/abs/1512.03385]] — arXiv 论文原文

## 相关
- [[Kaiming He]] — creator
- [[微软亚洲研究院]] — developed_at
- [[Deep Residual Learning for Image Recognition (2016 论文)]] — implements
- [[卷积神经网络（CNN）]] — extends
- [[退化问题（Degradation Problem）]] — addresses
- [[残差连接（Residual Connection）]] — uses
- [[ImageNet]] — tested_on
- [[ILSVRC 2015]] — achieves_results_on
- [[AlexNet]] — improves_over
- [[VGGNet]] — improves_over
- [[Batch Normalization]] — uses
- [[跳跃连接（Skip Connection）]] — uses
- [[He 初始化（Kaiming Initialization）]] — uses
