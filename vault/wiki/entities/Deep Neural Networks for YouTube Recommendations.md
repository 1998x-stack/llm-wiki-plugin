---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 深度学习, 工业实践, RecSys]
aliases: [YouTube DNN, YouTube Recommendations DNN, Deep Neural Networks for YouTube Recs]
relates_to:
  - {target: 两阶段推荐架构, type: implements}
  - {target: 双塔模型, type: implements}
  - {target: Example Age, type: implements}
  - {target: 期望观看时长, type: implements}
  - {target: 采样 Softmax, type: uses}
  - {target: 候选生成, type: implements}
  - {target: 近似最近邻检索, type: uses}
  - {target: offline-online gap, type: compares_to}
  - {target: YouTube, type: part_of}
  - {target: 矩阵分解, type: supersedes}
  - {target: Factorization Machines, type: compares_to}
  - {target: Wide & Deep, type: compares_to}
  - {target: DeepFM, type: compares_to}
  - {target: BPR 论文, type: compares_to}
  - {target: Neural Collaborative Filtering, type: compares_to}
supersedes: null
---

# Deep Neural Networks for YouTube Recommendations

## 概述
RecSys 2016 发表的里程碑论文，提出"[[候选生成]] + 排序"两阶段架构，将推荐建模为超大规模多分类问题，奠定十年工业推荐系统基础范式。

## 关键内容

1. **两阶段架构范式**：提出经典的"[[候选生成]]（[[候选生成|Candidate Generation]]）+ 排序（Ranking）"[[两阶段推荐架构|漏斗模型]]。[[候选生成]]从数十亿视频缩小到数百个（高召回率），排序从数百个精细化到数十个推荐结果（高精确率）。这一架构至今仍是全球推荐系统的标准[[骨骼系统|骨架]]，影响了淘宝、抖音、[[Netflix]]、[[Spotify]] 等平台。详见 [[两阶段推荐架构]]。

2. **极端多分类建模**：将推荐问题形式化为超大规模多分类问题，类别数等于视频语料库大小。使用 [[采样 Softmax]] 技术，每次只采样数千个负样本来近似完整 softmax，大幅降低计算开销。训练时每个视频对应一个 embedding（softmax 层权重），用户通过神经网络前向计算得到 embedding。

3. **[[双塔模型]] 原型**：[[候选生成]]模型中"用户塔"和"物品塔"分别产生 embedding，然后通过内积计算相似度。用户侧输入包括观看历史（取平均，借鉴 Word2Vec CBOW 思想）、搜索历史、人口统计学特征等。服务时转化为 [[近似最近邻检索]] 问题，用 [[近似最近邻检索|ANN]] 在亚线性时间内找到 Top-N 视频。

4. **[[Example Age]] 特征**：解决新鲜度偏差（Freshness Bias）的精巧设计。将训练样本的"年龄"作为显式输入特征，让模型学到用户偏好新鲜内容的倾向。推理时将 [[Example Age]] 设为零，等价于告诉模型"预测当前时刻用户最可能观看什么"。这种"训练时暴露偏差，推理时消除偏差"的思路是 [[因果推断]] 和去偏研究的先驱。

5. **[[期望观看时长]] 优化目标**：排序模型明确不优化 CTR（会鼓励标题党），而是优化[[期望观看时长]]。采用加权逻辑回归：正样本权重设为实际观看时长 T_i，负样本权重设为 1。推理时 e^{Wx+b} 近似等于 E[T]，直接作为排序得分。

6. **用户均匀采样策略**：为防止高活跃用户主导训练损失，对每个用户生成固定数量的训练样本，确保模型能为长尾用户提供合理推荐。

7. **训练-服务不对称设计**：论文多处体现"训练和服务可以且应该不同"的哲学——训练用 softmax + 采样，服务用 [[近似最近邻检索|ANN]] 检索；训练时传入实际 [[Example Age]]，推理时设为零；标签选择预测用户未来观看行为而非随机 holdout。

8. **在线 A/B 测试验证**：核心实验结论来自线上 A/B 测试而非离线实验。深度模型替换浅层模型后在线效果显著提升，增加网络深度和宽度均有收益但边际递减。论文坦诚指出离线指标与在线效果间的 [[offline-online gap]]。

9. **局限性**：冷启动视频处理不充分；用户长期兴趣建模简单（平均操作丢失时序信息）；[[特征交叉|特征交互]]依赖 MLP 隐式学习，缺乏显式[[特征交叉]]如 [[Factorization Machines]]；未讨论多目标优化和探索-利用平衡。后续工作如 [[DIN]]、[[DIEN]]、[[SASRec]] 等针对这些问题做了改进。

10. **历史地位**：RecSys 历史上被引用最多的工业论文之一（[[Google]] Scholar 约 5000-6000+ 次引用）。确立了工业推荐系统的标准架构，推动了 [[Embedding]] + [[近似最近邻检索|ANN]] 检索生态的发展（[[Faiss]]、[[ScaNN]]、Milvus 等向量数据库的兴起与此范式密切相关）。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Paul Covington]] — 第一作者
- [[Jay Adams]] — 第二作者
- [[Emre Sargin]] — 第三作者
- [[YouTube]] — 研究平台
- [[RecSys 2016]] — 发表会议
- [[两阶段推荐架构]] — 本文确立的核心架构范式
- [[双塔模型]] — 本文提出的模型原型
- [[Example Age]] — 本文提出的新鲜度偏差解决方案
- [[期望观看时长]] — 本文提出的排序优化目标
- [[采样 Softmax]] — 本文使用的训练技术
- [[近似最近邻检索]] — 本文服务时的检索方式
- [[offline-online gap]] — 本文坦诚指出的评估挑战
- [[矩阵分解]] — 本文超越的传统方法
- [[TensorFlow]] — 本文使用的训练基础设施
