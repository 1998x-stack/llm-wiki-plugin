---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 特征工程, 去偏, 时间偏差]
aliases: [Example Age Feature, 样本年龄特征, Freshness Bias Solution]
relates_to:
  - {target: Deep Neural Networks for YouTube Recommendations, type: implements}
  - {target: 冷启动问题, type: compares_to}
  - {target: 混合推荐系统, type: compares_to}
supersedes: null
---

# Example Age

## 概述
推荐系统中解决新鲜度偏差的[[特征工程（Feature Engineering）|特征工程]]技术：将训练样本的"年龄"作为显式输入，推理时设为零以偏好新鲜内容。

## 关键内容

1. **问题背景**：机器学习模型天然偏向"过去"。训练数据反映历史用户行为分布，老视频出现频率远高于新视频，导致模型倾向于推荐老视频。但用户实际上往往偏好新鲜内容——这种矛盾称为新鲜度偏差（Freshness Bias）。

2. **核心设计**：将训练样本的"年龄"（即训练样本的时间戳距离训练时刻的时间差）作为一个显式的输入特征传入模型。这样模型在训练过程中可以学到"样本年龄"与用户观看概率之间的关系——即用户确实偏好新鲜内容。

3. **训练-[[服务]]不对称**：在线上[[服务]]（推理）时，Example Age 特征被**设为零或略微为负**。这等价于告诉模型："现在是训练窗口的最末端，预测当前时刻用户最可能观看什么。"通过这个简单技巧，模型就能自然地倾向于推荐新上传的视频。

4. **效果验证**：加入 Example Age 特征后，模型预测的视频观看概率分布与实际分布的拟合度有了显著提升。这是 [[Deep Neural Networks for YouTube Recommendations]] 中最被人津津乐道的工程技巧之一。

5. **深远影响**：Example Age 的思想——"在训练中暴露偏差，在推理中消除偏差"——可以被看作是推荐系统中 [[因果推断]]（[[因果推断|Causal Inference]]）和去偏（Debiasing）研究的先驱。后续的 IPW（Inverse Propensity Weighting）、因果 embedding、[[反事实学习]]等方法，都是这一思路的更加理论化和系统化的延伸。

6. **局限性**：虽然 Example Age 在一定程度上缓解了新视频推荐不足的问题，但对冷启动视频（刚上传、几乎没有交互数据的视频）的处理并不充分。新视频的 embedding 在训练初期不稳定，在模型更新频率有限的情况下，很多新视频可能在获得足够曝光之前就已经"过时"。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Deep Neural Networks for YouTube Recommendations]] — 提出该技术的论文
- [[冷启动问题]] — Example Age 部分缓解但未完全解决的问题
- [[因果推断]] — Example Age 思想的理论化延伸方向
- [[两阶段推荐架构]] — Example Age 在其中的应用位置
