---
type: concept
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 广告系统, 机器学习, 深度学习]
aliases: [CTR Prediction, Click-Through Rate Prediction, 点击率预估, 点击率预测]
relates_to:
  - {target: Factorization Machines, type: uses}
  - {target: 特征交叉, type: uses}
  - {target: 嵌入表示, type: uses}
  - {target: 逻辑回归, type: compares_to}
  - {target: DeepFM, type: uses}
  - {target: FFM, type: uses}
  - {target: Wide & Deep, type: uses}
supersedes: null
---

# CTR 预估

## 概述
预测用户点击广告或推荐内容概率的机器学习任务，是[[计算]]广告和推荐系统的核心问题，经历了从逻辑回归 + [[特征工程（Feature Engineering）|手工特征]]到自动[[特征交叉]]模型的[[规范化理论|范式]]转变。

## 关键内容

1. **任务定义**：CTR（Click-Through Rate）预估是一个二分类问题，输入为用户特征、广告/内容特征、上下文特征，输出为用户点击的概率 $p(click | user, item, context)$。广泛应用于搜索广告、展示广告、推荐系统排序等场景。
2. **[[规范化理论|范式]]转变**：在 [[Factorization Machines]] 之前，工业界 CTR 模型主要依赖"逻辑回归 + 手工构造交叉特征"的[[规范化理论|范式]]。工程师需要大量领域经验来构造有效的交叉特征（如"用户年龄段 × 广告类别"），这项工作耗时且难以迁移。FM 的提出标志着向"自动[[特征交叉]]"[[规范化理论|范式]]的转变——让模型自动学习[[特征交叉|特征交互]]。
3. **FM 的贡献**：FM 以线性复杂度建模所有二阶[[特征交叉]]，在极度稀疏的广告特征空间中仍能有效学习交互参数。其线性时间复杂度使得 CTR 预估模型可以像逻辑回归一样高效训练和推理，同时具备自动建模[[特征交叉|特征交互]]的能力。
4. **工业界采用**：美团、阿里巴巴、华为等公司在其推荐系统和广告系统中大量使用 FM 及其变体。Twitter（现 X）的广告系统在早期也采用了 FM 作为核心模型。开源工具 [[libFM]] 和 xLearn 进一步推动了 FM 在工业界的普及。
5. **后续模型谱系**：FM 直接催生了 CTR 预估模型的演进谱系——FFM（2016，场感知交叉）、FNN（2016，FM [[嵌入表示|隐向量]]初始化 DNN）、[[Wide & Deep]]（2016，记忆+泛化）、[[DeepFM]]（2017，FM+DNN 并行）、NFM（2017，FM 交互层上叠加 DNN）、x[[DeepFM]]（2018，CIN 显式高阶交叉）、AFM（2017，[[注意力机制|注意力]]加权交叉）。
6. **FM 思想在深度学习时代的延续**：[[嵌入表示|嵌入层]]（[[嵌入表示|Embedding Layer]]）是 FM [[嵌入表示|隐向量]]的自然延伸。[[DeepFM]] 在架构中保留了完整的 FM 组件作为"浅层"模块，与 DNN 并行工作。DCN 和 x[[DeepFM]] 中的 Cross Network / CIN 可看作 FM 二阶交叉向高阶的自然推广。

## 来源
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)
- [DeepFM (Guo et al. 2017)](https://arxiv.org/abs/1703.04247)

## 相关
- [[Factorization Machines]] — CTR 预估的基石模型
- [[特征交叉]] — CTR 预估的核心建模目标
- [[嵌入表示]] — CTR 预估模型的通用组件
- [[DeepFM]] — FM+DNN 的 CTR 预估模型
- FFM — 场感知 CTR 预估模型
- [[Wide & Deep]] — Google 的 CTR 预估模型
- [[libFM]] — FM 的开源实现，广泛用于 CTR 预估
