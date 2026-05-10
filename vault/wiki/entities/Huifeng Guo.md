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
aliases: [Huifeng Guo, 郭辉锋]
relates_to:
  - {target: DeepFM, type: authored_by}
  - {target: 华为诺亚方舟实验室, type: part_of}
  - {target: Ruiming Tang, type: collaborates_with}
  - {target: CTR 预估, type: works_on}
supersedes: null
---

# Huifeng Guo

## 概述
[[DeepFM]] 论文第一作者，[[华为诺亚方舟实验室]]研究员，与 [[Ruiming Tang]] 等人合作提出 [[DeepFM]] 模型。

## 关键内容

1. **[[DeepFM]] 第一作者**：在 IJCAI 2017 发表 "[[DeepFM]]: A Factorization-Machine based Neural Network for [[CTR 预估|CTR Prediction]]"，提出用 FM 替代 [[Wide & Deep]] 中 Wide 部分的 LR，实现无需[[手工特征工程]]的端到端 [[CTR 预估]]。
2. **[[华为诺亚方舟实验室]]**：隶属于华为 [[华为诺亚方舟实验室|Noah's Ark Research Lab]]，该实验室在推荐系统和 [[CTR 预估]]领域有持续的研究产出。
3. **合作作者**：与 [[Ruiming Tang]]、[[Yunming Ye]]（哈尔滨工业大学深圳研究生院）、[[Zhenguo Li]]、[[Xiuqiang He]] 共同完成 [[DeepFM]] 工作。
4. **主要贡献**：DeepFM模型的核心创新在于将因子分解机(FM)与深度神经网络(DNN)整合为一个端到端模型，通过共享Embedding层同时学习低阶和高阶特征交互，彻底消除了Wide&Deep模型中对手工特征工程的依赖。
5. **研究影响**：DeepFM论文在IJCAI 2017发表后引用量超过2700次（截至2026年），并在华为应用市场的在线A/B测试中相比精心调优的LR模型CTR提升超过10%，对工业界产生了显著影响。

## 来源
- [DeepFM (IJCAI 2017)](https://arxiv.org/abs/1703.04247)
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md)

## 相关
- [[DeepFM]] — 代表作
- [[Wide & Deep]] — DeepFM 改进的前作
- [[Factorization Machines]] — DeepFM 浅层模块基础
- [[华为诺亚方舟实验室]] — 工作单位
- [[Ruiming Tang]] — DeepFM论文合作者
- [[Yunming Ye]] — DeepFM论文合作者
- [[Zhenguo Li]] — DeepFM论文合作者
- [[Xiuqiang He]] — DeepFM论文合作者
- [[CTR 预估]] — 研究领域
- [[特征交叉]] — 研究重点
