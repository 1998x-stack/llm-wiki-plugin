---
type: entity
entity_type: person
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, CTR预估, 深度学习, 计算机科学]
aliases: [Ruiming Tang, 汤汝明]
relates_to:
  - {target: DeepFM, type: authored_by}
  - {target: 华为诺亚方舟实验室, type: part_of}
  - {target: Huifeng Guo, type: collaborates_with}
  - {target: CTR 预估, type: works_on}
supersedes: null
---

# Ruiming Tang

## 概述
汤汝明，[[华为诺亚方舟实验室]]研究员，IJCAI 2017论文《[[DeepFM]]: [[DeepFM|A Factorization-Machine based Neural Network for CTR Prediction]]》的重要作者之一，与[[Huifeng Guo|郭辉锋]]等人共同提出了[[DeepFM]]模型。

## 关键内容

1. **[[DeepFM]] 共同作者**：与 [[Huifeng Guo]] 等人合作，在 IJCAI 2017 发表 [[DeepFM]] 论文，设计了 FM + DNN [[共享嵌入]]的并行架构。
2. **[[华为诺亚方舟实验室]]**：与 [[Huifeng Guo]]、[[Zhenguo Li]]、[[Xiuqiang He]] 同属华为 [[华为诺亚方舟实验室|Noah's Ark Research Lab]] 团队。
3. **研究贡献**：在 [[DeepFM]] 工作中参与了模型架构设计和实验验证，包括在 [[Criteo]] 数据集和华为应用市场真实数据上的[[性能审查|性能评估]]。
4. **主要贡献**：参与设计了[[DeepFM]]模型的核心架构，即将[[Factorization Machines|因子分解机]](FM)与深度神经网络(DNN)整合为一个端到端模型，通过[[共享Embedding]]层同时学习低阶和[[高阶特征交互]]，彻底消除了Wide&Deep模型中对[[手工特征工程]]的依赖。
5. **研究影响**：[[DeepFM]]论文在IJCAI 2017发表后引用量超过2700次（截至2026年），并在华为应用市场的在线A/B测试中相比精心调优的LR模型CTR提升超过10%，对工业界产生了显著影响。

## 来源
- [DeepFM (IJCAI 2017)](https://arxiv.org/abs/1703.04247)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 代表作
- [[Huifeng Guo]] — 第一作者合作者
- [[华为诺亚方舟实验室]] — 工作单位
- [[CTR 预估]] — 研究领域
- [[Yunming Ye]] — DeepFM论文合作者
- [[Zhenguo Li]] — DeepFM论文合作者
- [[Xiuqiang He]] — DeepFM论文合作者
- [[特征交叉]] — 研究重点
- [[嵌入表示]] — 技术核心
