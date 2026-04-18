---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "人工智能"]
aliases: ["Frank Rosenblatt", "弗兰克·罗森布拉特"]
relates_to:
  - target: "[[感知机（Perceptron）]]"
    type: implements
    confidence: 1.0
  - target: "[[McCulloch-Pitts 神经元模型]]"
    type: extends
    confidence: 0.9
  - target: "[[The Perceptron (1958 论文)]]"
    type: implements
    confidence: 1.0
supersedes: null
---

# Frank Rosenblatt

## 概述
Frank Rosenblatt（1928–1971），美国心理学家，康奈尔大学教授，于 1958 年提出感知机模型并搭建世界第一台可学习机器 [[Mark I Perceptron]]，是人工神经网络和深度学习的直接先驱。

## 关键内容

1. **学术背景**：康奈尔大学心理学家，受 [[McCulloch-Pitts 神经元模型]]（1943）启发，提出了根本性问题："大脑是如何从经验中存储和提取信息的？"

2. **[[Mark I Perceptron]]**：1957 年在 [[Cornell University|Cornell]] 航空实验室搭建了世界第一台可学习机器——拥有 400 个光敏传感器、可识别 20×20 像素图像的物理装置，权重由数百个可手动调节的电位器实现。

3. **[[感知机学习规则]]**：提出权重通过错误自动修正的算法——错了就改，对了维持不动。这是感知机最革命性的贡献，证明了机器可以从经验中学习。

4. **收敛定理**：严格证明了若训练数据线性可分，感知机学习算法在有限步内必然收敛，为机器学习提供了首个严格的理论保证。

5. **历史影响**：1971 年在 43 岁时因船难不幸离世，未能亲眼看到深度学习的复兴。但他播下的种子在半个世纪后改变了整个人类文明的走向。

## 来源
- [[01_perceptron_1958]] — 感知机原始论文解读

## 相关
- [[感知机（Perceptron）]] — implements
- [[McCulloch-Pitts 神经元模型]] — extends
- [[The Perceptron (1958 论文)]] — implements
