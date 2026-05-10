---
type: entity
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["机器学习", "深度学习", "人物", "图灵奖"]
aliases: ["Yann LeCun", "杨立昆", "Yann A. LeCun"]
relates_to:
  - target: "[[LeNet-5]]"
    type: relates_to
    confidence: 0.95
  - target: "[[Gradient-Based Learning Applied to Document Recognition (1998 论文)]]"
    type: relates_to
    confidence: 0.95
  - target: "[[卷积神经网络（CNN）]]"
    type: relates_to
    confidence: 0.95
  - target: "[[反向传播]]"
    type: relates_to
    confidence: 0.85
  - target: "[[Geoffrey E. Hinton]]"
    type: relates_to
    confidence: 0.85
supersedes: null
---

# Yann LeCun

## 概述 (50-200字符)
Yann LeCun（杨立昆），法国[[计算]]机科学家，深度学习三巨头之一，[[卷积神经网络（CNN）|卷积神经网络]]之父，2018 年[[阿兰·图灵|图灵]]奖得主，现任 Meta 首席 AI 科学家。

## 关键内容 (≥300字符, 用[[双链]])
1. **[[LeNet-5]] 与 CNN 的奠基**：1990 年代在[[贝尔实验室]]工作期间，LeCun 针对美国邮政局（USPS）手写邮编识别难题，构建了端到端图像识别系统。1998 年发表 [[Gradient-Based Learning Applied to Document Recognition (1998 论文)]]，提出 [[LeNet-5]] 架构，确立了 [[卷积神经网络（CNN）]] 的完整框架——局部[[感受野]]、权重共享、池化层、端到端 [[反向传播]] 训练。这一工作证明了特征可以被自动学习，从此人工[[特征工程（Feature Engineering）|特征工程]]不再是图像识别的瓶颈。
2. **核心洞见**：LeCun 的关键贡献在于将图像数据的两个先验知识编码为网络结构——**局部性**（相邻像素高度相关，有用特征是局部的如边缘、角点）和**平移不变性**（目标在图像任意位置都应被识别）。这一思想成为所有现代 CNN 的设计基础，从 [[AlexNet]]（2012）到 [[残差网络（ResNet）|ResNet]]、EfficientNet 均沿袭此[[规范化理论|范式]]。
3. **历史地位**：与 [[Geoffrey E. Hinton]]、[[Yoshua Bengio]] 共同获得 2018 年[[阿兰·图灵|图灵]]奖，表彰他们在深度学习领域的奠基性贡献。[[LeNet-5]] 在手写识别上直接商业部署，是所有现代 CNN 的直接祖先。LeCun 后任 [[Meta|Facebook]]/[[Meta AI]] 研究副总裁，推动自监督学习（Self-Supervised Learning）和 JEPA 架构的发展。

## 来源
- LeCun, Y., Bottou, L., Bengio, Y., & Haffner, P. (1998). Gradient-based learning applied to document recognition. Proceedings of the IEEE, 86(11), 2278–2324.

## 相关
- [[LeNet-5]] — relates_to（提出的架构）
- [[Gradient-Based Learning Applied to Document Recognition (1998 论文)]] — relates_to（第一作者）
- [[卷积神经网络（CNN）]] — relates_to（奠基者）
- [[反向传播]] — relates_to（应用于端到端训练）
- [[Geoffrey E. Hinton]] — relates_to（2018 图灵奖共同获得者）
