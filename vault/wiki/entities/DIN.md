---
type: entity
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [推荐系统, CTR预估, 深度学习, 注意力机制, 阿里巴巴, KDD]
aliases: [DIN, Deep Interest Network, Deep Interest Network for Click-Through Rate Prediction]
relates_to:
  - {target: DeepFM, type: extends}
  - {target: CTR 预估, type: implements}
  - {target: DIEN, type: caused}
  - {target: Wide & Deep, type: compares_to}
  - {target: PNN, type: compares_to}
  - {target: MIND, type: caused}
  - {target: BST, type: caused}
  - {target: SIM, type: caused}
  - {target: 局部激活单元, type: implements}
  - {target: Dice 激活函数, type: implements}
  - {target: Mini-batch Aware Regularization, type: implements}
supersedes: null
entity_type: paper
---

# DIN

## 概述
阿里巴巴 Guorui Zhou 等于 KDD 2018 提出的 [[CTR 预估]]模型，首次将[[注意力机制（Attention Mechanism）|注意力机制]]系统性地应用于工业级推荐系统，通过[[局部激活单元]]打破固定长度用户向量的信息瓶颈。

## 关键内容

1. **核心洞察：用户兴趣是多峰分布** — 传统方法将所有历史行为等权相加（Sum/Average Pooling），假设用户兴趣是单峰分布。DIN 指出用户兴趣在向量空间中呈多峰分布，强行平均得到的向量可能落在完全不相关的位置上。
2. **[[局部激活单元]]（[[局部激活单元|Local Activation Unit]]）** — 根据候选广告自适应地为用户历史行为分配权重。输入为 $[e_i; e_a; e_i \odot e_a]$ 的拼接（历史行为、候选广告、外积交互），通过小型 MLP 输出标量权重。刻意放弃 [[Softmax]] 归一化以保留兴趣强度信息。
3. **[[Target Attention]] 机制** — 以候选商品为 Query，历史行为为 Key 和 Value，实现 target-aware 的注意力。同一用户面对不同候选广告时自动"激活"不同的历史行为，得到完全不同的兴趣表示。
4. **[[Dice 激活函数]]** — 数据自适应激活函数，通过引入输入均值和方差将分界点从固定的零移动到数据分布中心，可视为 PReLU 的泛化形式。
5. **[[Mini-batch Aware Regularization]]** — 频次感知正则化，只对当前 mini-batch 中出现的特征[[计算]]正则项，低频特征获得更强约束，解决数亿参数规模下的[[过拟合（Overfitting）|过拟合]]问题。
6. **工业级效果** — 在阿里巴巴展示广告系统中取得 CTR 提升 10.0%、RPM 提升 3.8% 的在线 A/B 测试结果。0.001 的绝对 AUC 提升在数亿流量系统中即具有显著商业价值。
7. **后续影响** — 开创了基于深度学习的用户行为序列建模方向，直接催生 DIEN（2019, GRU+辅助损失）、DSIN（2019, Session+Self-attention）、BST（2019, [[Transformer架构|Transformer]]）、MIND（2019, 胶囊网络）、SIM（2020, 长序列建模）等工作。截至 2025 年被引 4000+ 次。
8. **局限性** — 忽略行为之间的时序关系（由 DIEN 解决）；行为序列长度限制（由 SIM/SDIM 解决）；对稀疏行为用户效果有限。

## 来源
- [Deep Interest Network for Click-Through Rate Prediction (KDD 2018)](https://arxiv.org/abs/1706.06978)
- [raw/books/推荐系统/11-din.md](raw/books/推荐系统/11-din.md)

## 相关
- [[DeepFM]] — 改进的前作
- [[CTR 预估]] — 应用场景
- [[华为诺亚方舟实验室]] — DeepFM 来源机构
- [[Wide & Deep]] — Google 同期工作
- DIEN — 解决 DIN 不建模时序关系的缺陷
- [[局部激活单元]] — DIN 核心组件
- [[Dice 激活函数]] — DIN 提出的训练技巧
- [[Target Attention]] — DIN 使用的注意力类型
- MIND — 从 DIN 单向量扩展为多向量表示
- BST — 用 Transformer 替代 DIN 简单注意力
- SIM — 将 DIN 扩展到超长行为序列
- [[Guorui Zhou]] — 论文主要作者
- [[Xiaoqiang Zhu]] — 论文作者
- [[Chenru Song]] — 论文作者
- [[Ying Fan]] — 论文作者
- [[Han Zhu]] — 论文作者
- [[Xiao Ma]] — 论文作者
- [[Yanghui Yan]] — 论文作者
- [[Junqi Jin]] — 论文作者
- [[Han Li]] — 论文作者
- [[Kun Gai]] — 论文作者

## 实验效果
- 离线实验中在Amazon数据集上相比BaseModel取得了5.35%的相对AUC提升
- 在MovieLens数据集上取得了1.61%的相对AUC提升  
- 在阿里巴巴工业数据集上取得了11.65%的相对AUC提升和0.0113的绝对AUC增益
- 在线A/B测试中CTR提升10.0%，RPM提升3.8%
- 消融实验显示：Mini-batch Aware Regularization相比Dropout带来+0.0031绝对AUC提升；Dice激活函数相比PReLU带来+0.0015绝对AUC提升；局部激活单元相比Sum Pooling带来+0.0067绝对AUC提升