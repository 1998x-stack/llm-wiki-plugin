---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["机器学习", "计算机视觉", "传统方法", "范式"]
aliases: ["Feature Engineering", "特征工程", "手工特征", "手工特征工程"]
relates_to: ["SIFT（尺度不变特征变换）", "HOG（方向梯度直方图）", "Haar 小波", "AlexNet", "深度学习（Deep Learning）", "卷积神经网络（CNN）"]
supersedes: null
---

# 特征工程（Feature Engineering）

## 概述
特征工程指由领域专家手工设计和选择用于机器学习任务的特征表示。深度学习前，这是[[计算]]机视觉和 NLP 的核心方法论，2012 年后被深度学习取代。

## 关键内容

1. **传统[[规范化理论|范式]]**：在深度学习时代之前，机器学习流水线分为两个阶段：(1) 特征工程——专家手工设计特征（如 SIFT、HOG、Haar-like、[[TF-IDF]]、n-gram）；(2) 训练分类器（如 SVM、[[随机森林]]、逻辑回归）。特征工程的质量直接决定模型性能上限。
2. **经典特征**：[[计算]]机视觉领域的经典手工特征包括：[[SIFT（尺度不变特征变换）]]（尺度不变关键点）、[[HOG（方向梯度直方图）]]（梯度方向统计）、[[Haar 小波]]（矩形模式检测）。这些特征需要领域专家数年的经验设计，且为特定任务定制，无法泛化。
3. **[[AlexNet]] 的颠覆**：2012 年，[[AlexNet]] 在 [[ILSVRC]] 竞赛中以 16.4% 的 [[Top-5 错误率]]夺冠，超越传统方法（SIFT+SVM，26.2%）近 10 个百分点。这证明了深度[[卷积神经网络（CNN）]]从数据中自动学习的特征远超手工设计特征。[[AlexNet]] 的卷积核自动学到了边缘、纹理、物体部件等层次化特征。
4. **[[规范化理论|范式]]转变**：[[AlexNet]] 之后，[[计算]]机视觉从"手工特征 + 简单分类器"转向"端到端深度学习"。特征工程的角色从"手工设计"转变为"网络架构设计"——研究者设计网络结构让模型自动学习最优特征表示。

## 来源
- [raw/articles/ai-papers/foundations/paper_03_alexnet.md] — AlexNet 论文精读

## 相关
- [[SIFT（尺度不变特征变换）]] — exemplar_of
- [[HOG（方向梯度直方图）]] — exemplar_of
- [[Haar 小波]] — exemplar_of
- [[AlexNet]] — superseded_by
- [[深度学习（Deep Learning）]] — replaced_by
- [[卷积神经网络（CNN）]] — auto_feature_learning
