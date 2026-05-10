---
type: paper
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["深度学习", "计算机视觉", "残差网络", "机器学习", "网络架构"]
aliases: ["Deep Residual Learning for Image Recognition", "ResNet 论文", "何恺明 2016", "ResNet Paper"]
relates_to: 
  - target: "[[残差网络（ResNet）]]"
    type: implements
    confidence: 0.95
  - target: "[[卷积神经网络（CNN）]]"
    type: extends
    confidence: 0.9
  - target: "[[ImageNet]]"
    type: tested_on
    confidence: 0.95
  - target: "[[Kaiming He]]"
    type: author
    confidence: 0.95
  - target: "[[微软亚洲研究院]]"
    type: published_by
    confidence: 0.9
  - target: "[[退化问题（Degradation Problem）]]"
    type: addresses
    confidence: 0.95
  - target: "[[残差连接（Residual Connection）]]"
    type: introduces
    confidence: 0.95
  - target: "[[跳跃连接（Skip Connection）]]"
    type: introduces
    confidence: 0.95
  - target: "[[ILSVRC 2015]]"
    type: achieves_results_on
    confidence: 0.95
  - target: "[[CVPR 2016]]"
    type: awarded
    confidence: 0.95
  - target: "[[CIFAR-10 数据集]]"
    type: tested_on
    confidence: 0.85
supersedes: null
---

# Deep Residual Learning for Image Recognition (2016 论文)

## 概述
[[Kaiming He|何恺明]]、张祥雨、任少卿、孙剑于2015年发表的开创性论文，提出了[[残差学习（Residual Learning）|残差学习]]框架和[[残差网络（ResNet）]]，通过引入[[残差连接]]解决了深度神经网络的退化问题，使网络能够训练至152层以上。该论文获得了CVPR 2016最佳论文奖，并在[[ILSVRC]] 2015竞赛中取得多项冠军。

## 关键内容
1. **[[退化问题（Degradation Problem）]]**：实验发现更深的网络（如56层）训练误差反而比浅层网络（如20层）更高，这不是[[过拟合（Overfitting）|过拟合]]而是优化问题——深层网络学不会恒等映射。在[[CIFAR-10 数据集|CIFAR-10]]数据集上，56层网络的训练误差显著高于20层网络。

2. **[[残差学习（Residual Learning）|残差学习]]公式**：将目标映射[[重构]]为 H(x) = F(x) + x，网络只需学习残差 F(x) = H(x) - x。当最优解接近恒等映射时，将权重推向零比学习恒等变换更容易。这种设计使得网络在不需要额外变换时可以轻松学习到零映射。

3. **两种残差块设计**：
   - BasicBlock（用于[[残差网络（ResNet）|ResNet]]-18/34）：包含两个3×3卷积层，结构简单。
   - Bottleneck（用于[[残差网络（ResNet）|ResNet]]-50/101/152）：采用1×1降维→3×3→1×1升维的结构，参数量比BasicBlock节省约40%（11 vs 18单位参数）。

4. **[[ImageNet|ILSVRC]] 2015 成果**：[[残差网络（ResNet）|ResNet]]-152以3.57% Top-5错误率获得冠军，首次超越人类水平（约5.1%），同时获得目标检测、图像定位等多项冠军，以及COCO 2015检测任务冠军，成为史无前例的"五冠王"。

5. **实验验证**：论文通过在[[CIFAR-10 数据集|CIFAR-10]]上的实验展示了[[残差连接]]的效果。普通网络（Plain Network）在超过一定层数后出现明显的性能退化，而残差网络即使到1202层仍可训练。实验还表明残差函数的响应普遍较小，说明网络确实学习到了接近恒等映射的小扰动。

6. **理论意义**：[[残差连接]]提供了梯度高速公路，确保梯度可以直接流向浅层，解决[[梯度消失]]问题；使深层网络更容易训练；损失曲面更加平滑，便于优化器找到全局最优解。

## 来源
- [[raw/articles/ai-papers/machine-learning/13_resnet_2015.md]] — 原始笔记文件
- [[raw/articles/ai-papers/foundations/paper_05_resnet.md]] — 论文精读 #05：残差网络 ResNet
- [[https://arxiv.org/abs/1512.03385]] — arXiv 论文原文

## 相关
- [[残差网络（ResNet）]] — implements
- [[Kaiming He]] — author
- [[微软亚洲研究院]] — published_by
- [[卷积神经网络（CNN）]] — extends
- [[ImageNet]] — tested_on
- [[退化问题（Degradation Problem）]] — addresses
- [[残差连接（Residual Connection）]] — introduces
- [[ILSVRC 2015]] — achieves_results_on
- [[CVPR 2016]] — awarded
- [[CIFAR-10 数据集]] — tested_on
