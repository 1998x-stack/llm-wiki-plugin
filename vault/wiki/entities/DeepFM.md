---
type: entity
entity_type: paper
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [推荐系统, CTR预估, 深度学习, 分解模型]
aliases: [DeepFM, A Factorization-Machine based Neural Network for CTR Prediction]
relates_to:
  - {target: Factorization Machines, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: 嵌入表示, type: uses}
  - {target: CTR 预估, type: implements}
  - {target: FFM, type: compares_to}
  - {target: Wide & Deep, type: supersedes}
  - {target: 华为诺亚方舟实验室, type: part_of}
  - {target: Huifeng Guo, type: authored_by}
supersedes: null
---

# DeepFM

## 概述
DeepFM是一种基于因子分解机的神经网络模型，用于点击率预测。该论文由华为诺亚方舟实验室的郭辉锋等人在IJCAI 2017发表，将因子分解机(FM)与深度神经网络(DNN)整合为端到端模型，通过共享Embedding层同时学习低阶和高阶特征交互，终结了CTR预估中的手工特征工程。

## 关键内容

1. **并行架构**：DeepFM 由两部分并行组成——FM 部分（浅层模块）负责捕获显式的低阶（二阶）[[特征交叉|特征交互]]，DNN 部分（深层模块）负责捕获隐式的高阶非线性[[特征交叉|特征交互]]。两部分共享同一组[[嵌入表示|嵌入向量]]，[[联合训练]]。最终输出为 sigmoid(y_FM + y_DNN)。
2. **[[共享嵌入]]**：FM 和 DNN 共享类别型特征的[[嵌入表示]]，避免了分别学习导致的参数冗余和不一致性。这种"浅层 + 深层"的并行设计模式已成为推荐系统的标准架构。[[共享嵌入]]带来三重优势：参数效率、[[联合训练|联合优化]]、消除预训练。
3. **无需[[特征工程（Feature Engineering）|手工特征]]**：DeepFM 的端到端设计消除了对人工构造交叉特征的依赖，模型自动学习[[特征交叉|特征交互]]，大幅降低了[[特征工程（Feature Engineering）|特征工程]]成本。相比 [[Wide & Deep]] 的 Wide 部分需要手工 cross-product 特征，DeepFM 用 FM 完全替代。
4. **与 FM 的关系**：DeepFM 直接在架构中保留了完整的 FM 组件作为"浅层"模块，是 FM 思想在深度学习时代的自然延伸。FM 负责低阶交互的显式建模，DNN 补足高阶交互的隐式学习，两者互补。
5. **[[CTR 预估]]效果**：在 [[Criteo]] 数据集上 AUC=0.8016、LogLoss=0.44985（最优）；在华为应用市场约10亿条记录的真实数据上 AUC=0.8715。在线 A/B 测试中 DeepFM-D 相比精心调优的 LR 模型，CTR 提升超过 10%。
6. **后续影响**：DeepFM 的"浅层 + 深层"并行架构启发了后续一系列工作，包括 DCN（[[Google]] 2017，Cross Network 显式交叉）、[[xDeepFM]]（微软 2018，CIN 向量级显式交叉）、[[AutoInt]]（2019，[[多头注意力|多头自注意力]]可解释交互）等。
7. **局限性**：FM 组件仍局限于二阶交叉；DNN 高阶交互为黑盒难以解释；FM 暴力枚举所有特征对缺乏选择性；缺乏时序动态建模；DNN 学习的是维度级而非向量级交互。后续工作如 [[xDeepFM]]、[[AutoInt]]、DIN 分别针对这些局限进行了改进。
8. **架构一般性**：DeepFM 框架具有可扩展性，论文提出 DeepFM-D（Deep 部分用标准 DNN）和 DeepFM-P（Deep 部分用 PNN）两个变体，"FM + Deep [[共享嵌入]]"是可替换 Deep 部分实现的通用[[规范化理论|范式]]。
9. **核心创新**：用FM替代Wide&Deep模型中的线性模型+Cross-product，通过共享Embedding消除特征工程，实现端到端学习的整体框架，并具有架构的一般性。
10. **实验验证**：在Criteo数据集和华为应用市场真实数据集上都取得最优性能，与次优模型相比AUC提升超过0.25%-0.37%，在线A/B测试中相比精心调优的LR模型CTR提升超过10%。

## 来源
- [DeepFM: A Factorization-Machine based Neural Network for CTR Prediction (IJCAI 2017)](https://arxiv.org/abs/1703.04247) — Guo, Tang, Ye, Li, He. 华为诺亚方舟实验室
- [DeepFM 扩展版 (arXiv 2018)](https://arxiv.org/abs/1804.04950) — 补充在线 A/B 测试等内容
- [raw/books/推荐系统/09-deepfm.md](raw/books/推荐系统/09-deepfm.md) — 深度解读笔记

## 相关
- [[Factorization Machines]] — 浅层模块基础
- [[特征交叉]] — FM 部分建模目标
- [[嵌入表示]] — 共享嵌入层
- [[CTR 预估]] — 主要应用场景
- FFM — 同代 FM 扩展模型
- [[Wide & Deep]] — DeepFM 直接改进的前作
- [[xDeepFM]] — 引入 CIN 显式高阶交互的后续工作
- DCN — Cross Network 显式交叉的并行工作
- [[AutoInt]] — 多头自注意力可解释交互的后续工作
- DIN — 引入注意力建模用户兴趣序列的后续工作
- [[华为诺亚方舟实验室]] — 发表机构
- [[Huifeng Guo]] — 论文第一作者
- [[Ruiming Tang]] — 论文合作者
- [[Yunming Ye]] — 论文合作者
- [[Zhenguo Li]] — 论文合作者
- [[Xiuqiang He]] — 论文合作者
- [[共享Embedding]] — 核心技术特性
