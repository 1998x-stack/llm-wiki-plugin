---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [paper, computer-vision, CNN, vgg, ImageNet, 机器学习]
aliases: [Simonyan & Zisserman 2014, Very Deep Convolutional Networks for Large-Scale Image Recognition]
relates_to:
  - target: "[[Karen Simonyan]]"
    type: authored_by
    confidence: 0.95
  - target: "[[Andrew Zisserman]]"
    type: authored_by
    confidence: 0.95
  - target: "[[VGGNet]]"
    type: introduced
    confidence: 0.95
  - target: "[[University of Oxford]]"
    type: affiliated_with
    confidence: 0.9
  - target: "[[ILSVRC]]"
    type: evaluated_on
    confidence: 0.9
  - target: "[[AlexNet]]"
    type: extends
    confidence: 0.9
  - target: "[[Top-5 错误率]]"
    type: measures_performance
    confidence: 0.9
  - target: "[[GoogLeNet: Inception]]"
    type: compares_to
    confidence: 0.85
supersedes: null
---

# Very Deep Convolutional Networks for Large-Scale Image Recognition (2014 论文)

## 概述
[[Karen Simonyan]] 和 [[Andrew Zisserman]] 于 2014 年发表的论文，提出了 [[VGGNet]] 架构，系统性地验证了使用统一的 3×3 [[3×3卷积核|小卷积核]]堆叠能够显著提升网络性能。该论文在 [[ILSVRC]] 2014 挑战赛中取得分类亚军和检测冠军的优异成绩，证明了网络深度对视觉识别性能的重要性。

## 关键内容

1. **统一 3×3 卷积设计**：摒弃 [[AlexNet]] 中使用的 11×11、5×5、3×3 混合卷积核，统一使用 3×3 卷积核。通过堆叠多个 3×3 卷积，既能获得更大的[[感受野]]，又能减少参数量并增加[[非线性激活]]，实现更好的性能。

2. **VGG 家族架构**：系统测试了 A-E 六种不同深度[[Configuration|配置]]（从 11 层到 19 层），其中 [[VGGNet|VGG-16]]（13 个卷积层 + 3 个全连接层）和 [[VGGNet|VGG-19]]（16 个卷积层 + 3 个全连接层）最为经典，分别具有 138M 和 144M 参数。

3. **深度与性能关系**：通过系统的[[Ablation Study|消融实验]]，论文验证了深度对性能的正向影响，但同时也发现边际效应递减现象（19层相比16层仅提升0.1%）。

4. **竞赛成果**：在 [[ILSVRC]] 2014 挑战赛中，[[VGGNet|VGG-16]] 单模型取得了 7.32% 的 [[Top-5 错误率]]，仅次于 [[GoogLeNet: Inception]] 的 6.67%，但获得了检测任务的冠军。

5. **参数效率问题**：论文架构中全连接层占据了约 89.4% 的参数（约 123.6M），这启发了后续研究者使用全局平均池化（GAP）来替代全连接层，大幅减少参数量。

## 来源
- [[raw/articles/ai-papers/foundations/paper_11_vggnet.md]] — 全文精读
- [[ai_papers_timeline.md]] — 2014 年时间线条目

## 相关
- [[Karen Simonyan]] — authored_by
- [[Andrew Zisserman]] — authored_by
- [[VGGNet]] — introduced
- [[University of Oxford]] — affiliated_with
- [[ILSVRC]] — evaluated_on
- [[AlexNet]] — extends
- [[Top-5 错误率]] — measures_performance
- [[GoogLeNet: Inception]] — compares_to
